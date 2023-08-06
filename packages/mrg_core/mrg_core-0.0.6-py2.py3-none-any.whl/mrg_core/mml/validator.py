#!/usr/bin/env python
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
"""
This module implements the :class:`Validator` class that is used to test whether
or not the metrec2mml.jar Java version is equivalent to the Python metrec2mml.py
version.
"""
from __future__ import print_function

import os
import sys
import logging
from time import time

from mrg_core.mml.mml import MML
from mrg_core.mml.mml import MMLJava
from mrg_core.mml import metlog

from mrg_core.util.convert import evaluate
from mrg_core.util.convert import is_close
from mrg_core.util.convert import to_file_system_case
from mrg_core.util.diriter import SystemSessionIterator
from mrg_core.util.diriter import SystemSessionYearIterator


class ValidatorError(Exception):
    """ Exception class for all Validator class errors. """


class Validator(object):
    """ This class implements a comparison test between the
    original metrec2mml.jar Java program and the new
    metrec2mml.py Python script."""

    def __init__(self, reporter, continue_from=None,
                 ignore_errors=True, save_files=False, display_progress=True):
        """
        :param str reporter: default value is 'ANON' (anonymous).
        :param str continue_from:
        :param bool ignore_errors:
        :param bool save_files: save the XML files for post processing comparison.
        :param bool display_progress: display the progress indicator
        """
        self._reporter = reporter
        self._count = 0
        self._continue_from = continue_from
        self._ignore_errors = ignore_errors
        self._save_files = save_files
        self._display_progress = display_progress

    def validate_directory(self, directory):
        """ Validate all subdirectory sessions in the directory specified.

        :param str directory:
        """
        year_str = os.path.basename(directory)
        year = 0
        try:
            year = int(year_str)
        except ValueError:
            pass

        if 1900 < year < 2100:
            self._validate_year_sessions(directory)
        else:
            self._validate_directory_sessions(directory)

    def validate_session(self, metrec_log_file):
        """ Validate a single session metrec log file.

        :param str metrec_log_file:
        :raises ValidatorError:
        """
        self._count += 1
        time_0 = time()
        version = 0.0
        try:
            metrec_log_file = to_file_system_case(metrec_log_file)
            if self._display_progress:
                version = self._validate_json_with_java(metrec_log_file)
                msg = '#%04d %5.2fs Validated: "%s". (MetRec V%0.1f)' \
                      % (self._count, time()-time_0, metrec_log_file, version)
                msg += ' ' * 20
                sys.stdout.write(msg + '\b' * len(msg))
            return
        except SyntaxError as exc:
            msg = '#%04d %5.2fs Mismatch : "%s". ' \
                  '(%s) (MetRec V%0.1f)' \
                  % (self._count, time()-time_0, metrec_log_file, str(exc), version)
        except (IOError, KeyError) as exc:
            msg = '#%04d %5.2fs Error    : "%s". ' \
                  '(%s) (MetRec V%0.1f)' \
                  % (self._count, time()-time_0, metrec_log_file, repr(exc), version)
        raise ValidatorError(msg)

    def _validate_directory_sessions(self, directory):
        """ Validate a session directory that may contain wildcards
        for batch processing.

        :param str directory: a directory path in one of the following forms,

            * {imo-data-root-dir}/yyyy/yyyymmdd
            * {imo-data-root-dir}/yyyy/yyyymmdd/camera
            * {imo-data-root-dir}/camera/yyyymmdd

        The /dd/ may contain wildcard characters, such as /??/. Example,

            * {imo-data-root-dir}/2016/201601??

        would process all dates for Jan 2016.

            * {imo-data-root-dir}/2016/2016????/ICC?

        would process all ICC cameras for the year 2016.

        """

        can_process = True
        if self._continue_from:
            can_process = False
        # list of: (path, yyyy, yyyymmdd, sys_code)
        sessions = SystemSessionIterator(directory).sorted()
        for session in sessions:
            session_path = session[0]
            session_name = session[2]
            metrec_log_file = os.path.join(session_path, session_name + '.log')
            if not can_process:
                if self._continue_from in metrec_log_file:
                    can_process = True

            if can_process:
                try:
                    self.validate_session(metrec_log_file)
                except ValidatorError as exc:
                    print(str(exc))
                    if not self._ignore_errors:
                        break

    def _validate_year_sessions(self, directory):
        """ Validate a year directory by iterating over each month separately.

        :param str directory: a directory path in the form::

            {imo-data-root-dir}/yyyy
        """
        sessions = SystemSessionYearIterator(directory, self._continue_from)
        for session in sessions:
            session_path = session[0]
            session_name = session[2]
            metrec_log_file = os.path.join(session_path, session_name + '.log')
            try:
                self.validate_session(metrec_log_file)
            except ValidatorError as exc:
                print(str(exc))
            if not self._ignore_errors:
                break

    @staticmethod
    def _test_line_equivalence(line_num, line_json, line_java, skip_tags):
        """
        :param int line_num:
        :param str line_json:
        :param str line_java:
        :param list skip_tags:
        :raises SyntaxError:
        """
        if skip_tags is None:
            skip_tags = ['version', 'fov_alt', 'fov_az', 'pos_dec']

        if line_json != line_java:
            mismatch = True
            for skip_tag in skip_tags:
                if '<%s>' % skip_tag in line_json or '</%s>' % skip_tag in line_json:
                    mismatch = False
                    break

            nums_json = metlog.RE_ALL_NUMBERS.findall(line_json)
            nums_java = metlog.RE_ALL_NUMBERS.findall(line_java)
            nums = list(zip(nums_json, nums_java))
            for num_json, num_java in nums:
                try:
                    num_json = evaluate(num_json)
                except ValueError:
                    continue
                try:
                    num_java = evaluate(num_java)
                except ValueError:
                    continue

                if is_close(num_json, num_java, rel_tol=1e-06):
                    mismatch = False

            if mismatch:
                raise SyntaxError('Line mismatch at line: %d.'
                                  '\nJSON line:\n%s\nJAVA line:\n%s'
                                  % (line_num, line_json, line_java))

    @staticmethod
    def _save_xml_files(mml_obj, json_str, java_str):
        """
        :param MML mml_obj:
        :param str json_str:
        :param str java_str:
        :return:
        """
        camera = mml_obj.session['system_code']
        basename = os.path.splitext(os.path.basename(mml_obj.path))[0]
        try:
            os.mkdir('validation_results')
        except OSError:
            pass
        path = os.path.join('validation_results', basename + '_' + camera + '_json.xml')
        path = os.path.abspath(path)
        with open(path, 'w') as file_obj:
            file_obj.write(json_str)

        path = os.path.join('validation_results', basename + '_' + camera + '_java.xml')
        with open(path, 'w') as file_obj:
            file_obj.write(java_str)

    @staticmethod
    def _strip_elements(xml_str, element_names):
        """ Remove specified XML element nodes from the XML content.

        :param str xml_str:
        :param list element_names:
        :return: the list of lines
        :rtype: str
        """
        lines = []
        for line in xml_str.split('\n'):
            if len(line.strip()):
                found_it = False
                for key in element_names:
                    if key in line:
                        found_it = True
                        break
                if not found_it:
                    lines.append(line)
        return lines

    def _validate_json_with_java(self, metrec_log_file, skip_tags=None):
        """ This routine generates the XML MML file using both the
        Java and Python versions. The Java version has been thoroughly
        validated over the past several years, so it is used to check
        if the new Python equivalent is indeed equivalent.


        :param str metrec_log_file:
        :param list skip_tags: default is None which sets the
            skipped tags to ['version']
        :return: the MetRec Version number
        :rtype: float
        :raises SyntaxError: when a line mismatch is found.
        """
        logging.info('MML Validating: %s', metrec_log_file)
        time_0 = time()
        xml_java = MMLJava(metrec_log_file, self._reporter).get_xml_string()
        logging.info('Timed: %0.2fs MML JAVA parser', time() - time_0)

        time_0 = time()
        mml_json = MML(metrec_log_file, self._reporter)
        xml_json = mml_json.get_xml_string()
        xml_json = MML.transform_to_java_format(xml_json)
        logging.info('Timed: %0.2fs MML JSON parser', time() - time_0)

        if self._save_files:
            self._save_xml_files(mml_json, xml_json, xml_java)

        if xml_json.count('.REF</path>') == 1 and xml_java.count('.REF</path>') == 0:
            print('WARNING: JSON has reference file, JAVA does not. File: %s' % metrec_log_file)

        to_remove = ['location_lon',
                     'location_lat',
                     'location_height',
                     'fov_alt',
                     'fov_az',
                     'pos_dec',
                     '<comments>Reference stars used</comments>']

        lines_json = self._strip_elements(xml_json, to_remove)
        lines_java = self._strip_elements(xml_json, to_remove)

        xml_json = '\n'.join(lines_json)
        xml_java = '\n'.join(lines_java)

        if xml_json.count('<meteor>') != xml_java.count('<meteor>'):
            self._save_xml_files(mml_json, xml_json, xml_java)
            raise SyntaxError('Meteor count mismatch. JSON count: %d, '
                              'JAVA count: %d. '
                              'MetRec Version: %0.1f'
                              % (xml_json.count('<meteor>'),
                                 xml_java.count('<meteor>'),
                                 mml_json.metlog.version))

        if xml_json.count('<file>') != xml_java.count('<file>'):
            self._save_xml_files(mml_json, xml_json, xml_java)
            raise SyntaxError('File count mismatch. JSON count: %d, '
                              'JAVA count: %d. '
                              'MetRec Version: %0.1f'
                              % (xml_json.count('<file>'),
                                 xml_java.count('<file>'),
                                 mml_json.metlog.version))

        # The java version does not look for reference files outside
        # of session directory. Test for this case.
        line_count_dif = len(lines_json) - len(lines_java)

        if line_count_dif:
            self._save_xml_files(mml_json, '\n'.join(lines_json), '\n'.join(lines_java))
            raise SyntaxError('Line count mismatch. '
                              'JSON len: %d, JAVA len: %d. MetRec Version: %0.1f'
                              % (len(lines_json), len(lines_java), mml_json.metlog.version))

        for i, (line_json, line_java) in enumerate(list(zip(lines_json, lines_java))):
            try:
                self._test_line_equivalence(i+1, line_json, line_java, skip_tags)
            except SyntaxError as exc:
                self._save_xml_files(mml_json, '\n'.join(lines_json), '\n'.join(lines_java))
                raise SyntaxError(str(exc) + '. MetRec Version: %0.1f' % mml_json.metlog.version)

        return mml_json.metlog.version
