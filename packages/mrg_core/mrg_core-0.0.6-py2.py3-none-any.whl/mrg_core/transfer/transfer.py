#   --------------------------------------------------------------------------
#   Copyright 2016 SRE-F, ESA (European Space Agency)
#       Hans Smit <Hans.Smit@esa.int>
#
#   This is restricted software and is only to be used with permission
#   from the author, or from ESA.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#   --------------------------------------------------------------------------
""" New MRG data archive transferring tool. """
from __future__ import print_function

import logging
import os
import sys
import time
import glob
import shutil
import socket

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64

import zipfile
import gzip
import tarfile

from future.utils import raise_with_traceback

try:
    import pysftp
    from pysftp import paramiko

except ImportError as _exc:
    print(_exc)
    print('to install: pip install pysftp')

from mrg_core.util.template import TemplateEngine

LOGGER = logging  # use the root logger


class SFTPConnectionException(Exception):
    """ This exception is raised when any exception is raised in the
    SFTPConnection class. """


class ArchiveFileException(Exception):
    """ Any exceptions thrown in the ArchiveFile class are rerouted to this
    exception class. """


class NotifierException(Exception):
    """ Exception emanating from the Notifier class. """


class SFTPConnection(object):
    """ High level FTP connection and commanding class. """

    def __init__(self, host, username, password, port=22, timeout=None):
        self._conn = None
        LOGGER.debug('SFTPConnection: %s:%d, %s, %s, %f', host, port, username, password, timeout)
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            self._conn = pysftp.Connection(host=host,
                                           username=username,
                                           password=password,
                                           port=port,
                                           cnopts=cnopts)
            if timeout > 0:
                self._conn.timeout = timeout

        except pysftp.SSHException as exc:
            LOGGER.error('sftp error: %s', str(exc))
            if self._conn:
                self._conn.close()
            raise SFTPConnectionException(exc)

    @staticmethod
    def progress(transferred, total):
        """ File downloader progress callback function. """
        percentage = 100.0 * float(transferred) / float(total)
        transferred_mb = float(transferred) / (1024.0*1024.0)
        total_mb = float(total) / (1024.0*1024.0)
        sys.stdout.write("%d%% (%0.1f of %0.1fMB) " %
                         (percentage, transferred_mb, total_mb) + "\b" * 40)

    def close(self):
        """ Close the SFTP connection. """
        if self._conn:
            self._conn.close()

    def set_cwd(self, directory):
        """ Set current working directory on the remote FTP server.

        :param str directory: the directory to set.
        """
        LOGGER.info('Setting current working directory to: %s', directory)
        self._conn.cwd(directory)

    def get_listing(self, field=None):
        """ Set current working directory on the remote FTP server.

        :param str field: list of fields to return. May be one of the following,

                * filename
                * size
                * atime
                * mtime
                * mode
                * uid
                * gid

        :return: a list of file names, or list file attributes, or
            list files + field tuples
        :rtype: list
        """
        if field is None:
            files = self._conn.listdir_attr()
        elif field == 'filename':
            files = self._conn.listdir()
        else:
            files = []
            files_attr = self._conn.listdir_attr()
            for attr in files_attr:
                att = getattr(attr, 'st_' + field)
                files.append((attr.filename, att))

        LOGGER.info('Getting listing. Found %d entries', len(files))

        return files

    def remove_file(self, remote_file):
        """ Delete the specified file from the current working directory.

        :param str remote_file: the remote file name
        """
        try:
            self._conn.remove(remote_file)

        except IOError as exc:
            LOGGER.error('Caught IOError: %s', str(exc))
            sftp_exc = SFTPConnectionException('failed to remove %s due to IOError' % remote_file)
            raise_with_traceback(sftp_exc)

        except pysftp.SSHException as exc:
            LOGGER.error('Caught SSHException: %s', str(exc))
            sftp_exc = SFTPConnectionException('failed to remove %s due to SSHException'
                                               % remote_file)
            raise_with_traceback(sftp_exc)

    def put_file(self, local_file):
        """ This method uploads the local file to the current working directory
        of the remote FTP server. It requires the CWD to be set before calling
        this method.

        :param str local_file:
        """
        try:
            file_name = os.path.basename(local_file)
            file_size = os.path.getsize(local_file) / (1024.0*1024.0)
            LOGGER.info("Uploading %s (%0.1f MB)", local_file, file_size)

        except OSError as exc:
            file_name = None
            LOGGER.error('Caught OSError: %s', str(exc))
            sftp_exc = SFTPConnectionException('failed to get file size for: %s' % local_file)
            raise_with_traceback(sftp_exc)

        try:
            self._conn.put(local_file, file_name, self.progress, confirm=True, preserve_mtime=False)
            # LOGGER.info("Finished uploading %0.2fMB to sftp server" % sz)

        except paramiko.SFTPError as exc:
            LOGGER.error('Caught SFTPError: %s', str(exc))
            sftp_exc = SFTPConnectionException('failed to put %s due to SFTPError' % local_file)
            raise_with_traceback(sftp_exc)

        except pysftp.SSHException as exc:
            LOGGER.error('Caught SSHException: %s', str(exc))
            sftp_exc = SFTPConnectionException('failed to put %s due to SSHException' % local_file)
            raise_with_traceback(sftp_exc)

    def get_file(self, directory, file_name, local_directory, expected_size=0):
        """ Download the remote file to the local file system.
        """
        remote_path = directory.replace('\\', '/') + '/' + file_name
        remote_path = remote_path.replace('//', '/')
        local_path = os.path.abspath(os.path.join(local_directory, file_name))

        if expected_size > 0:
            expected_size_str = '(%0.1f MB)' % (expected_size/1024.0/1024.0)
        else:
            expected_size_str = ''
        LOGGER.info('Downloading %s to %s %s', remote_path, local_directory, expected_size_str)

        try:
            self._conn.get(remote_path, local_path, callback=self.progress, preserve_mtime=False)
            # LOGGER.info('Finished downloading: %s', remote_path)
            if expected_size > 0:
                download_size = os.path.getsize(local_path)
                if expected_size != download_size:
                    LOGGER.error('Expected file size different from downloaded file.')
                    LOGGER.error('Expected %d bytes, got %d bytes.', expected_size, download_size)

        except paramiko.SFTPError as exc:
            LOGGER.error('Caught SFTPError: %s', str(exc))
            sft_exc = SFTPConnectionException('failed to get %s due to SFTPError' % remote_path)
            raise_with_traceback(sft_exc)

        except pysftp.SSHException as exc:
            LOGGER.error('Caught SSHException: %s', str(exc))
            sft_exc = SFTPConnectionException('failed to get %s due to SSHException' % remote_path)
            raise_with_traceback(sft_exc)

        except socket.error as exc:
            LOGGER.error('Caught socket.error: %s', str(exc))
            sft_exc = SFTPConnectionException('failed to get %s due to socket.error' % remote_path)
            raise_with_traceback(sft_exc)


class ArchiveFile(object):
    """ This class encapsulates the zip/unzip routines for directory
    tree archiving. """

    def __init__(self, archive_file):
        self._archive_file = archive_file
        self._include_exts = []
        self._exclude_exts = []
        self._exclude_dirs = []

    def decompress(self, out_dir):
        """ Unzip the archive file into the specified directory.
        The directory will be automatically created if it does not
        already exist.

        :param str out_dir: the directory to populate.
        :raises ArchiveFileException: is raised when an I/O error occurs
        """

        archive_file = self._archive_file

        if not os.path.exists(archive_file):
            raise ArchiveFileException('Could not locate zipped file: %s' % self._archive_file)

        if os.path.getsize(archive_file) == 0:
            raise ArchiveFileException('Zip file is empty: %s' % self._archive_file)

        ext = os.path.splitext(archive_file)[1]
        if ext == '.gz':
            archive_file = self._ungz(archive_file)
            ext = os.path.splitext(archive_file)[1]

        if ext == '.tar':
            self._untar(archive_file, out_dir)

        elif ext == '.zip':
            try:
                self._unzip(archive_file, out_dir)
            except zipfile.BadZipfile as exc:
                LOGGER.exception(exc)
                raise ArchiveFileException(exc)

    def _can_add_file(self, file_path):
        """ test the file path passed for inclusion of the specified filters """
        if len(self._include_exts):
            ext = os.path.splitext(file_path)[1]
            if not ext:
                return False
            if ext not in self._include_exts:
                return False

        if len(self._exclude_exts):
            ext = os.path.splitext(file_path)[1]
            if ext in self._exclude_exts:
                return False

        if len(self._exclude_dirs):
            dirs = set(file_path.split(os.path.sep))
            res = self._exclude_dirs.intersection(dirs)
            if len(res):
                return False

        return True

    def set_inclusion_rules(self, include_exts='', exclude_exts='', exclude_dirs=''):
        """
        :param str include_exts: comma separated list of file extensions to include.
        :param str exclude_exts: comma separated list of file extensions to ignore.
        :param str exclude_dirs: comma separated list of directories to ignore
        """
        self._include_exts = set(include_exts.split(",") if include_exts else [])
        self._exclude_exts = set(exclude_exts.split(",") if exclude_exts else [])
        self._exclude_dirs = set(exclude_dirs.split(",") if exclude_dirs else [])

    @staticmethod
    def trim_path(file_path, in_dir, include_dir_in_zip):
        """ Removes the root directory path information from the
        specified file path.

        :param str file_path:
        :param str in_dir:
        :param str include_dir_in_zip:
        :return: the archive entry file and relative path.
        :rtype: str
        """

        root_dir, dir_to_zip = os.path.split(in_dir)

        # file_path    : c:\cilbo\data\LIC1\20160216\0400back.bmp
        # in_dir       : c:\cilbo\data\LIC1\20160216
        # root_dir     : c:\cilbo\data\LIC1
        # dir_to_zip   : 20160216
        # archive_path : \20160216\0400back.bmp

        # remove the root directory from the file path
        # c:\cilbo\data\ICC7\20160620\123456.bmp => \20160216\123456.bmp
        archive_path = file_path.replace(root_dir, '', 1)

        if root_dir:
            # Strip any leading (or trailing path separators
            # \20160216\123456.bmp => 20160216\123456.bmp
            archive_path = archive_path.strip(os.path.sep)

        if not include_dir_in_zip:
            # remove the directory name being zipped
            # 20160216\123456.bmp => 123456.bmp
            archive_path = archive_path.replace(dir_to_zip + os.path.sep, '', 1)

        # remove any double slashes, and make slashes O/S specific
        archive_name = os.path.normcase(archive_path)
        return archive_name

    def compress(self, in_dir, include_empty_dir=False, include_dir_in_zip=True):
        """ Zip an entire directory.

        Reference,
            http://stackoverflow.com/questions/458436/adding-folders-to-a-zip-file-using-python
            Author: Peter Lyons

        The original code was updated to enable filtering.
        """
        in_dir = os.path.normpath(in_dir)
        if not os.path.isdir(in_dir):
            raise OSError('in_dir argument must point to a directory. \'%s\' does not.', in_dir)

        archive_file = self._archive_file
        if not archive_file:
            archive_file = in_dir + ".zip"

        archive_dir = os.path.dirname(os.path.normpath(archive_file))
        if not os.path.exists(archive_dir):
            LOGGER.debug('Creating directories: %s', archive_dir)
            os.makedirs(archive_dir)

        with zipfile.ZipFile(archive_file, 'w', zipfile.ZIP_DEFLATED) as file_obj:
            counter = 0
            for (current_dir, dir_names, file_names) in os.walk(in_dir):
                LOGGER.info('Zipping %d in %s', len(file_names), current_dir)
                for file_name in file_names:
                    file_path = os.path.normpath(os.path.join(current_dir, file_name))
                    if self._can_add_file(file_path):
                        counter += 1
                        LOGGER.debug('zipping: %d %s', counter, repr(file_name))

                        # prepare the proper archive path
                        archive_name = self.trim_path(file_path, in_dir, include_dir_in_zip)
                        file_obj.write(file_path, archive_name)

                # Make sure we get empty directories as well
                if len(file_names) == 0 and len(dir_names) == 0:
                    if include_empty_dir:
                        LOGGER.debug('zipping: empty directory')
                        archive_name = self.trim_path(current_dir, in_dir, include_dir_in_zip)
                        zip_info = zipfile.ZipInfo(archive_name + '/')
                        # there is some discussion on how to do this properly.
                        # please refer to the web reference. This seems to work as well.
                        file_obj.writestr(zip_info, "")

    @staticmethod
    def _unzip(archive_file, out_dir):
        """ unzip directory
        reference: http://bytes.com/topic/python/answers/606630-extract-zip-files

        :param str archive_file: the file to unpack.
        :param str out_dir: the directory to unpack the archive file to.
        """
        # handle .zip type of archives
        zipped = zipfile.ZipFile(archive_file, 'r')
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        dest = os.path.abspath(out_dir + '/')
        items = zipped.namelist()
        LOGGER.info('Extracting %d entries from file: %s to %s',
                    len(items), archive_file, out_dir)
        for file_name in items:
            abs_file_path = os.path.join(dest, file_name)
            abs_dir_path = os.path.join(dest, os.path.dirname(file_name))
            if file_name.endswith('/'):
                if os.path.exists(abs_file_path):
                    pass
                else:
                    os.makedirs(abs_file_path)
            else:
                dentry = os.path.normpath(abs_dir_path)
                fentry = os.path.normpath(abs_file_path)

                if not os.path.exists(dentry):
                    os.makedirs(dentry)

                if os.path.exists(fentry):
                    # NOTE: a file size check comparison should be done as well!!!
                    LOGGER.debug('File already exists. Skipping file: %s', file_name)
                    continue

                byte_stream = zipped.read(file_name)
                LOGGER.debug('Unzipping file: %s with %d bytes...', file_name, len(byte_stream))
                with open(fentry, 'wb') as file_obj:
                    file_obj.write(zipped.read(file_name))
                access_time = time.time()
                date_time = zipped.getinfo(file_name).date_time
                # date_time   => (yyyy, mm, dd, HH, MM, SS)
                # struct_time => (yyyy, mm, dd, HH, MM, SS, wday, yday, isdst)
                date_time += (0, 0, 0)  # turn it into a 9-tuple
                modified_time = time.mktime(date_time)
                os.utime(fentry, (access_time, modified_time))

        zipped.close()

    @staticmethod
    def _ungz(archive_file):
        """ Unzip the *gz file.

        :param str archive_file:
        :return: the *.tar file name
        :rtype: str
        """

        # first the file must be uncompressed
        out_tar_file = archive_file.replace('.gz', '')
        if os.path.exists(out_tar_file):
            if os.path.getsize(out_tar_file) == 0:
                LOGGER.debug('Removing empty tar file: %s', out_tar_file)
                os.remove(out_tar_file)

        if not os.path.exists(out_tar_file):
            LOGGER.debug('Unzipping gzip file to: %s...', out_tar_file)
            with open(out_tar_file, 'wb') as file_obj:
                with gzip.open(archive_file, 'rb') as zip_obj:
                    chunk_size = 1024*1024
                    buf = zip_obj.read(chunk_size)
                    while buf:
                        file_obj.write(buf)
                        buf = zip_obj.read(chunk_size)

        return out_tar_file

    @staticmethod
    def _untar(archive_file, out_dir):
        """ Unpack the archive *.tar file.

        :param str archive_file: the file to unpack.
        :param str out_dir: the directory to unpack the archive file to.
        """
        overwrite = True  # NOTE: this should be a passed parameter

        LOGGER.debug('Extracting tar file: %s, to %s', archive_file, out_dir)
        tar = tarfile.open(archive_file)
        LOGGER.info('tar file has %d entries', len(tar.getmembers()))
        for tar_info in tar:
            entry_path = os.path.abspath(os.path.join(out_dir, tar_info.name))
            if tar_info.isreg():
                if os.path.exists(entry_path):
                    if not overwrite:
                        LOGGER.debug('Skipping file: %s', tar_info.name)
                        continue

                LOGGER.debug('Unzipping file: %s with %d bytes...', tar_info.name, tar_info.size)
                tar.extract(tar_info, path=out_dir)

            elif tar_info.isdir():
                if not os.path.exists(entry_path):
                    os.makedirs(entry_path)


class TransferCommand(object):
    """ Base directory for archive command classes,

        * :class:`Downloader`
        * :class:`Uploader`
        * :class:`Compressor`
        * :class:`Decompressor`

    This base class contains the common code for these classes.
    """

    def __init__(self, opts):
        self._ignore_errors = opts.ignoreErrors
        self._overwrite = opts.overwrite
        self._has_error = False

        local_archive_dir = os.path.abspath(os.path.join(opts.dir_archive, opts.camera))
        if not os.path.exists(local_archive_dir):
            LOGGER.info('Creating archive directory: %s', local_archive_dir)
            os.makedirs(local_archive_dir)

        local_camera_dir = os.path.abspath(os.path.join(opts.dir_data, opts.camera))
        if not os.path.exists(local_camera_dir):
            LOGGER.info('Creating camera directory: %s', local_camera_dir)
            os.makedirs(local_camera_dir)


class Uploader(TransferCommand):
    """ High level class to facilitate batch uploading. """

    def __init__(self, opts):
        super(Uploader, self).__init__(opts)
        self._remote_dir = opts.ftp_cwd + '/' + opts.camera  # MUST use '/' separator
        self._local_dir = os.path.abspath(os.path.join(opts.dir_archive, opts.camera))
        # self._local_dir = os.path.join(self._local_dir, opts.night + '.zip')
        self._night = opts.night
        self._conn_args = (opts.ftp_host,
                           opts.ftp_usr,
                           opts.ftp_pwd,
                           opts.ftp_port,
                           opts.ftp_timeout)

    def get_local_files(self):
        """ Retrieve a list of local files based on night archive files.
        The night attribute may include wildcard '?' and '*' characters.

        :return: list of absolute paths
        :rtype: list
        """
        local_zips = os.path.join(self._local_dir, self._night + '.zip')
        local_files = glob.glob(local_zips)
        return local_files

    def remove_remote_files(self):
        """ Deletes the remote files that are retrieved from
        the :func:`get_local_files`. This is useful for cleaning
        up a remote directory after running the unittests.

        WARNING: be careful with calling this routine, you could
        inadvertently delete all the data on the server.
        """
        local_files = self.get_local_files()
        file_names = [os.path.basename(path) for path in local_files]
        try:
            sftp_conn = SFTPConnection(*self._conn_args)
            sftp_conn.set_cwd(self._remote_dir)
            for file_name in file_names:
                try:
                    sftp_conn.remove_file(file_name)
                except SFTPConnectionException:
                    pass  # ignore files that may not exist
        except SFTPConnectionException as exc:
            LOGGER.error(exc)
            raise

    def run(self):
        """ Run the uploader. """
        self._upload()

    def _upload(self):
        """ Execute the actual transfer of local files to the
        remote FTP server current working directory"""
        try:
            sftp_conn = SFTPConnection(*self._conn_args)
            sftp_conn.set_cwd(self._remote_dir)
        except SFTPConnectionException as exc:
            LOGGER.error(exc)
            raise

        self._has_error = False
        listing = dict(sftp_conn.get_listing(field='size'))
        local_files = self.get_local_files()
        for local_file in local_files:
            file_name = os.path.split(local_file)[1]
            if file_name in listing:
                local_size = os.path.getsize(local_file)
                remote_size = listing[file_name]
                if local_size == remote_size and not self._overwrite:
                    continue

            sftp_conn.put_file(local_file)


class Downloader(TransferCommand):
    """ High level class to facilitate batch downloading. """

    def __init__(self, opts):
        super(Downloader, self).__init__(opts)
        self._remote_dir = opts.ftp_cwd + '/' + opts.camera  # MUST use '/' separator
        self._local_dir = os.path.abspath(os.path.join(opts.dir_archive, opts.camera))
        self._night = opts.night
        self._retries = opts.retries
        self._conn_args = (opts.ftp_host,
                           opts.ftp_usr,
                           opts.ftp_pwd,
                           opts.ftp_port,
                           opts.ftp_timeout)
        if self._retries < -1:
            self._retries = 10000

    def run(self):
        """ Download the remote directory. """
        retries = self._retries
        retries += 1
        while retries:
            self._download()
            if self._has_error:
                retries -= 1
                if retries:
                    # make sure not to over write successful downloads
                    self._overwrite = False
                    retry_count = self._retries - retries + 1
                    LOGGER.info('Retrying to failed downloads: #%d', retry_count)
            else:
                break

    def _download(self):
        """ Execute the batch transfer of remote files on the FTP server to the
        local file system. """
        sftp_conn = None
        try:
            sftp_conn = SFTPConnection(*self._conn_args)
        except SFTPConnectionException as exc:
            sftp_exc = SFTPConnectionException('SFTP connection failed. args: %s'
                                               % repr(self._conn_args))
            raise_with_traceback(sftp_exc)

        try:
            sftp_conn.set_cwd(self._remote_dir)
        except SFTPConnectionException as exc:
            sftp_exc = SFTPConnectionException('SFTP CWD failed. Remote dir: %s' % self._remote_dir)
            raise_with_traceback(sftp_exc)

        self._has_error = False

        # first find which files require downloading
        night = self._night
        night = night.rstrip('?*')
        files = []
        for file_attr in sftp_conn.get_listing():
            # check that the night patteren matches the remote file name
            if night in file_attr.filename:
                local_file = os.path.join(self._local_dir, file_attr.filename)
                if self._overwrite:
                    # if the over write switch is on, then force a re-download
                    files.append(file_attr)

                elif not os.path.exists(local_file):
                    # if the file does not exist locally, then download it
                    files.append(file_attr)

                else:
                    # check if the remote and local files sizes match
                    # if not, then download it.
                    expected_size = file_attr.st_size
                    download_size = os.path.getsize(local_file)
                    if expected_size == download_size:
                        LOGGER.debug('Skipping %s.', file_attr.filename)
                    else:
                        files.append(file_attr)

        LOGGER.info('Downloading %d archive files...', len(files))
        for file_attr in files:
            expected_size = file_attr.st_size
            try:
                sftp_conn.get_file(self._remote_dir,
                                   file_attr.filename,
                                   self._local_dir,
                                   expected_size)
            except SFTPConnectionException as exc:
                LOGGER.error(exc)
                self._has_error = True
                if not self._ignore_errors:
                    raise


class Decompressor(TransferCommand):
    """ Unzip the archive file. """

    def __init__(self, opts):
        super(Decompressor, self).__init__(opts)
        self._local_dir = os.path.abspath(os.path.join(opts.dir_data, opts.camera))
        self._zip_file = os.path.abspath(os.path.join(opts.dir_archive,
                                                      opts.camera,
                                                      opts.night+'.zip'))

    def run(self):
        """ Execute the batch unzipping of archive files. """
        zip_files = glob.glob(self._zip_file)
        if len(zip_files) == 0:
            LOGGER.warning('Input file does not exist: %s', self._zip_file)

        for zip_entry in zip_files:
            if self._overwrite:
                night_dir_name = os.path.splitext(os.path.split(zip_entry)[1])[0]
                local_night_dir = os.path.join(self._local_dir, night_dir_name)
                if os.path.exists(local_night_dir):
                    LOGGER.debug('Deleting existing directory: %s', local_night_dir)
                    shutil.rmtree(local_night_dir, ignore_errors=True)
            try:
                archiver = ArchiveFile(zip_entry)
                archiver.decompress(self._local_dir)
                LOGGER.debug('Unpack complete. File: %s, size: %s bytes',
                             zip_entry, os.path.getsize(zip_entry))
            except ArchiveFileException:  # as exc:
                # LOGGER.exception(exc)
                if not self._ignore_errors:
                    raise


class Compressor(TransferCommand):
    """ Zip the camera/night data directory(s) """
    def __init__(self, opts):
        super(Compressor, self).__init__(opts)
        self._local_dir = os.path.abspath(os.path.join(opts.dir_data, opts.camera, opts.night))
        self._zip_file_template = os.path.abspath(os.path.join(opts.dir_archive,
                                                               opts.camera,
                                                               '{}.zip'))

    def run(self):
        """ Execute the zipping of local data directory(s) """
        local_dirs = glob.glob(self._local_dir)
        for local_entry in local_dirs:
            night_dir_name = os.path.splitext(os.path.split(local_entry)[1])[0]
            zip_file = self._zip_file_template.format(night_dir_name)
            if os.path.exists(zip_file):
                if self._overwrite:
                    LOGGER.debug('Deleting existing archive file: %s', zip_file)
                    os.remove(zip_file)
                else:
                    LOGGER.debug('Archive file exists. Skipping file: %s', zip_file)
                    continue
            try:
                archiver = ArchiveFile(zip_file)
                archiver.compress(local_entry, include_empty_dir=True, include_dir_in_zip=True)
                LOGGER.debug('Pack complete. File: %s, size: %s bytes',
                             zip_file, os.path.getsize(zip_file))
            except ArchiveFileException:
                # LOGGER.exception(exc)
                if not self._ignore_errors:
                    raise


class Notifier(object):
    """ Email notification class. """

    def __init__(self, opts):
        self._smtp_debug = 0
        self._mail_subject = opts.email_subject
        self._mail_from = opts.email_from
        self._mail_to = opts.email_to
        self._mail_body = ''
        self._mail_attach = []
        self._template = TemplateEngine(
            parameters=opts.email_translation,
            template_file=opts.email_template)
        self._conn_args = (opts.smtp_host,
                           opts.smtp_port,
                           socket.getfqdn(),
                           opts.smtp_timeout)
        self._user_args = (opts.smtp_usr,
                           opts.smtp_pwd)

    def send(self):
        """ Send the email via SMTP. """
        msg = MIMEMultipart()
        msg['Subject'] = self._mail_subject
        msg['From'] = self._mail_from
        msg['To'] = self._mail_to
        msg.attach(MIMEText(self._mail_body))

        # add the file attachment
        for file_path in self._mail_attach:
            if os.path.exists(file_path):
                with open(file_path, "rb") as file_object:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(file_object.read())
                    part.add_header(
                        "Content-Disposition",
                        "attachment; filename=\"%s\"" % os.path.basename(file_path)
                    )
                    encode_base64(part)
                    msg.attach(part)

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        conn = None
        try:
            conn = smtplib.SMTP(*self._conn_args)
            conn.set_debuglevel(self._smtp_debug)  # log data exchange with server
            if self._user_args and len(self._user_args) == 2:
                conn.starttls()
                conn.login(*self._user_args)
            mail_to = self._mail_to.split(";")

            conn.sendmail(self._mail_from, mail_to, msg.as_string())
            conn.quit()

        except smtplib.SMTPException as exc:
            nexc = NotifierException('Failed to send message. ex: %s' % str(exc))
            raise_with_traceback(nexc)
        finally:
            if conn:
                conn.close()

    def run(self):
        """ Send the email notification.
        """
        self._template.run()
        self._mail_body = self._template.body
        if 'Subject' in self._template.headers:
            self._mail_subject = self._template.headers['Subject'][0]
        if 'Attach' in self._template.headers:
            self._mail_attach = self._template.headers['Attach']
        self.send()
