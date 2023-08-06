"""
   JPL SPICE kernels downloader module.
"""
from __future__ import print_function
import os
from ftplib import FTP
import logging


class MKFile(object):
    """
    JPL SPICE kernels downloader class.

    This class will analyse a given meta-kernel file passed as input
    parameter in the instance initialization, extract the kernel names,
    check if there is a local copy in the path given in the meta-kernel, and
    if there is no such copy, download them, and place them in the $KERNELS
    local directory.

    If a kernel file already exists, it will be skipped.  In this case, it is
    assumed that the local and the remote files are the same.  There is no
    checksum check made.

    The expected format for the SPICE meta-kernel is::

        \\begindata

           PATH_SYMBOLS    = ( 'KERNELS' )
           PATH_VALUES     = ( '/data/spice/generic'  )

           KERNELS_TO_LOAD = (

                 '$KERNELS/fk/planets/earth_assoc_itrf93.tf',
                 '$KERNELS/lsk/naif0012.tls',
                 '$KERNELS/pck/de-403-masses.tpc',
                 '$KERNELS/pck/gm_de431.tpc',
                 '$KERNELS/pck/pck00010.tpc',
                 '$KERNELS/pck/earth_070425_370426_predict.bpc',
                 '$KERNELS/pck/earth_720101_070426.bpc',
                 '$KERNELS/spk/de432.bsp'

                              )
        \\begintext

    This class logs two information messages, one when the local and
    remote repositories are synchronised and another upon completion of a
    transfer of a file.  Use the standard logging library in order to capture
    these information messages.

    Parameters
    ----------
    path: str
       Full path of the input ``meta-kernel``

    Examples
    --------
    >>> MKFile('/data/spice/mrg/mk/mots_orbit.mk')

    """

    def __init__(self, path=None):
        self._path = path
        self._local_files = []
        self._remote_files = []
        self._host = 'naif.jpl.nasa.gov'
        self._remote = '/pub/naif/generic_kernels'
        self._local = ''
        self._key_values = {}

        self._parse()
        self._evaluate()
        self._load()

    def _parse(self):
        """ Parse the *.mk file, and save it's key/value pairs.
        Comma-delimited values will be saved as a list. """
        lines = []
        found_begin_data = False

        with open(self._path, 'r') as file_obj:
            for line in file_obj.readlines():
                line = line.strip()
                if line == r'\begindata':
                    found_begin_data = True
                elif line and found_begin_data:
                    lines.append(line)

        lines = ''.join(lines).replace(')', ')\n').strip().split('\n')
        for line in lines:
            key, value = [part.strip('() \'"') for part in line.split('=', 1)]
            if ',' in value:
                value = [part.strip(' \'"') for part in value.split(',')]
            self._key_values[key] = value

    def _evaluate(self):
        """ Evaluate the local and remote path lists. """
        root_key = self._key_values['PATH_SYMBOLS']
        root_dir = self._key_values['PATH_VALUES']
        self._local = root_dir
        self._files = self._key_values['KERNELS_TO_LOAD']

        for file_path in self._files:
            loc_file = file_path.replace('$' + root_key, root_dir)
            loc_file = os.path.abspath(loc_file)
            self._local_files.append(loc_file)
            rem_file = file_path.replace('$' + root_key + '/', '')
            self._remote_files.append(rem_file)

    def _load(self):
        """ Synchronise the local directory with that of the remote
        directory. Any existing local files will be skipped.
        """
        ftp = FTP(self._host)
        ftp.login()
        ftp.cwd(self._remote)
        ftp.set_pasv(False)

        loc_rem_files = zip(self._local_files, self._remote_files)
        for local_file, remote_file in loc_rem_files:
            if os.path.exists(local_file) and os.path.getsize(local_file):
                # skip existing entry
                continue

            try:
                os.makedirs(os.path.dirname(local_file))
            except OSError:
                pass

            # Find the remote file in the FTP server
            path = os.path.dirname(remote_file)
            name = os.path.basename(remote_file)
            ftp_listing = ftp.nlst(path)
            if name not in ftp_listing:
                for directory in ftp_listing:
                    for remote in ftp.nlst(directory):
                        if os.path.basename(remote) == name:
                            remote_file = remote
                            break

            # Transfer the file. Text files have a .tAA extension
            # while binary ones have a .bAA extension.
            if '.t' in name:
                with open(local_file, 'wt') as file_obj:
                    # Retrieve the lines of the ASCII file and write them to a
                    # file with the correct EOL character.  The lambda
                    # function takes as input the FTPed line and adds the EOL
                    # character from the os.linesep OS interface.
                    ftp.retrlines('RETR %s' % remote_file,
                                  lambda line: file_obj.write('{}{}'.format(
                                      line,
                                      os.linesep)))
            else:
                with open(local_file, 'wb') as file_obj:
                    ftp.retrbinary('RETR %s' % remote_file, file_obj.write)

            logging.info('MKFile: %s file successfully downloaded.', name)

        logging.info('MKFile: Local and remote directories are fully '
                     'synchronised')
