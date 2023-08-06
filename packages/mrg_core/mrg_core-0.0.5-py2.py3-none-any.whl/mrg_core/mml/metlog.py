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
This module implements the METREC log parser.
"""
# from __future__ import print_function
import re
import os
import logging
import glob

from datetime import datetime
from datetime import timedelta
from collections import OrderedDict

from mrg_core.util.fileparser import FileParser
from mrg_core.util.convert import equ2hor
from mrg_core.util.convert import hour_to_deg
from mrg_core.util.convert import evaluate
from mrg_core.util.convert import to_file_system_case
from mrg_core.util.diriter import SystemSessionIterator
from mrg_core.mml.reffile import RefFile

# this extracts a decimal (-123.45) or integer (12345)
RE_ALL_NUMBERS = re.compile(r'([-+]?[0-9]*\.?[0-9]+)')
RE_ALL_INTEGERS = re.compile(r'([-+]?[0-9]*[0-9]+)')
RE_STARTING_WITH_NUMBER = re.compile(r'^([-+]?[0-9]*\.?[0-9]+)')
RE_OBS_TIME = re.compile(r'^(\d{2}):(\d{2}):(\d{2}).*')
RE_SHORT_DATE = re.compile(r'^(\d{4})(\d{2})(\d{2}).*')

METREC_HEADER_DEFAULT = {
    'FrameSize': 0,
    'Altitude': None,
}

METREC_HEADERS = {
    'Software': None,
    'Date': None,
    'Time': None,
    'MaximumSolarAltitude': RE_STARTING_WITH_NUMBER,
    'MinimumLunarDistance': RE_STARTING_WITH_NUMBER,
    'MaximumMeteorVelocity': RE_STARTING_WITH_NUMBER,
    'CameraName': None,  # >=v5.3
    'FrameSize': RE_STARTING_WITH_NUMBER,   # <=v5.0
    'ReferenceStars': os.path.basename,
    'Operation mode': None,  # >v3.1
    # 'OperationMode': None,  # <=v3.1
    'Reference date': RE_ALL_INTEGERS,
    # 'ReferenceDate': lambda val: [int(part) for part in val.split('.')],  # <=v3.1
    'Reference time': RE_ALL_INTEGERS,
    # 'ReferenceTime': RE_ALL_NUMBERS,  # <=v3.1
    'Site code': None,
    'Longitude': RE_STARTING_WITH_NUMBER,
    'Latitude': RE_STARTING_WITH_NUMBER,
    'Altitude': RE_STARTING_WITH_NUMBER,
    'Center of plate RA':  RE_STARTING_WITH_NUMBER,
    'Center of plate DE':  RE_STARTING_WITH_NUMBER,
    'Center of plate Alt': RE_STARTING_WITH_NUMBER,
    'Center of plate Az': RE_STARTING_WITH_NUMBER,
    'Mean Squared O-C': RE_ALL_NUMBERS,
    # 'Mean Square O-C': RE_ALL_NUMBERS,  # <=v3.1
    'start of observation': RE_ALL_NUMBERS,
    'end of observation': RE_ALL_NUMBERS,
    'effective observing time': RE_ALL_NUMBERS,
}

METREC_HEADERS_VERSION = {
    '{version}<=5.4': {
        'ReferenceDate': 'Reference date',
        'ReferenceTime': 'Reference time',  # <=v3.1
        'OperationMode': 'Operation mode',  # <=v3.1
    },
    '{version}<=3.2': {
        'ReferenceDate': 'Reference date',
        'ReferenceTime': 'Reference time',  # <=v3.1
        'OperationMode': 'Operation mode',  # <=v3.1
    },
}


class MetLogFile(FileParser):
    """ Class to parse a METREC log file. """

    def __init__(self, path):
        """
        :param str path: the metrec log file path.
        :raises IOError: if the metrec log file does not exist.
        """
        # self._header = OrderedDict(METREC_HEADER_DEFAULT)
        self._meteors = []
        self._session_dates = ['', '']  # night, morning
        self._json = {}
        self._version = 0.0
        self._version_header_map = {}
        try:
            path_yyyy_yyyymmdd_system = next(SystemSessionIterator(os.path.dirname(path)))
            self._sys_code = path_yyyy_yyyymmdd_system[3]
            self._night = path_yyyy_yyyymmdd_system[2]
        except StopIteration:
            # This occurs if the metrec log file path does not
            # include the expected yyyy/yyyymmdd/system
            self._sys_code = None
            self._night = os.path.splitext(os.path.basename(path))[0]

        # parse the file...
        super(MetLogFile, self).__init__(path)

        # Update the system code headers in the case that the metrec log
        # file path does not include yyyy/yyyymmdd/system information
        if not self._sys_code and 'CameraName' in self._header:
            system = self._header['CameraName']
            self._header['SystemCode'] = system
            self._sys_code = system

    @property
    def version(self):
        """
        :return: the metrec version number.
        :rtype: float
        """
        return self._version

    @property
    def meteors(self):
        """
        :return: the list of ordered dictionary meteor detection events.
        :rtype: list
        """
        return self._meteors

    def _set_mean_square_oc(self):
        """ Parse the 'Mean_Squared_O-C' key and set the evening
        and morning session dates.
        """
        date = RE_SHORT_DATE.findall(os.path.basename(self._path))
        if len(date):
            date = [int(val) for val in date[0]]
            evening_date = datetime(*date)
        else:
            evening_date = datetime.strptime(self._header['Date'], '%Y/%m/%d')
        morning_date = evening_date + timedelta(days=1)
        self._session_dates[0] = evening_date.strftime('%Y-%m-%dT')
        self._session_dates[1] = morning_date.strftime('%Y-%m-%dT')
        values = self._header['Mean_Squared_O-C']  # values => [0:msqe, 1:1, 2:l1o, 3:mag]
        self._header['DeltaCoordinate'] = values[0]  # msqe
        self._header['RefPosMSQE'] = values[2]  # l1o
        self._header['DeltaMagnitude'] = values[3] ** 0.5  # sqrt(mag)

    def _set_effective_obs_time_fields(self):
        """ Set the 'teff' and 'yyyymmdd' based on the 'effective_observing_time'
        and 'Date' header values.
        """
        if 'effective_observing_time' in self._header:
            hh_mm_ss = self._header['effective_observing_time']
            hh_mm_ss.extend([0, 0, 0])  # ensure there are at least 3 values
            hours, minutes, seconds = hh_mm_ss[0:3]
            self._header['teff'] = float(hours) + float(minutes) / 60.0 + float(seconds) / 3600.0
        else:
            self._header['teff'] = 0.0
        self._header['yyyymmdd'] = self._header['Date'].replace('/', '')

    def _set_fov_fields(self):
        """ Calculates and sets the 'fov_alt' and 'fov_az' header key values.
        """
        if 'Longitude' not in self._header:
            self._header['fov_alt'] = None
            self._header['fov_az'] = None
            self._header['Longitude'] = None
            self._header['Latitude'] = None
            return

        if self._header['Operation_mode'] == 'unguided':
            date_list = self._header['Reference_date']
            time_list = self._header['Reference_time']
            ref_time = tuple(date_list) + tuple(time_list)
        else:
            # Figure out the middle of the period
            start = self._header['start_of_observation']
            stop = self._header['end_of_observation']
            start = datetime(*start)
            stop = datetime(*stop)
            ref_time = start + (stop - start) / 2
            ref_time = tuple(ref_time.timetuple()[0:6])
        longitude = self._header['Longitude']
        latitude = self._header['Latitude']
        rac = hour_to_deg(self._header['Center_of_plate_RA'])
        dec = self._header['Center_of_plate_DE']
        alt, azm = equ2hor(ref_time, longitude, latitude, rac, dec)
        self._header['fov_alt'] = alt
        self._header['fov_az'] = azm

    @staticmethod
    def _parse_meteor_line(line):
        """
        :param str line: the complete meteor event specification line.
        :return:
        :rtype: OrderedDict
        """

        # NOTE: @ => degrees
        # 01:09:37 Meteor #26 at (0.328,0.205)->(0.268,0.226) frames=3 dur=0.14s pixel=2 dir=161@
        #          vel=16.0@/s snr=1.1
        #          shower=SPO bright=3.7mag (6.569h,27.72@) -> (6.638h,26.05@) acc=3.0'
        # 01:09:37 Skip saving meteor #26 as the previous one is not yet saved!
        # or,
        # 01:09:37 Meteor #25 at (0.331,0.206)->(0.268,0.226) frames=3 dur=0.14s pixel=5 dir=162@
        #          vel=16.9@/s snr=1.1
        #          shower=SPO bright=3.7mag (6.567h,27.78@) -> (6.639h,26.00@) acc=5.8'
        # 01:09:37 Saving meteor data of #25 ... ok!
        result = OrderedDict()

        # remove spaces after '=' characters
        line = line.replace('= ', '=').replace('= ', '=')
        # replace the FOV begin -> end equatorial coordinates
        line = line.replace(' -> ', '>>')
        # replace the FOV begin -> end relative coordinates
        line = line.replace('->', ',')
        line = line.replace(u'\xf8', '').strip()
        # line = line.encode('ascii', errors='ignore')
        logging.debug('Parsing meteor line: %s', line)
        # Example:
        #     20:38:12 Meteor #6 at (0.391,0.832)->(0.346,0.795) ...
        parts = line.split()

        result['Timestamp'] = datetime.strptime(parts[0], '%Y-%m-%dT%H:%M:%S')
        result['Time'] = result['Timestamp'].strftime('%H%M%S')
        result['InfFile'] = result['Time'] + '.inf'
        result['FovRelative'] = evaluate(parts[4])  # '(0.639,0.380),(0.574,0.280)'

        # IN_FOV: Determine if the meteor was inside/outside the field of view
        # We do this by retrieving the X/Y coordinates of the begin and end point of
        # the meteor
        # The 'in_fov'-attribute is a string with one of these 4 values:
        # 11: meteor began and ended inside the FOV
        # 10: meteor began inside FOV, ended outside FOV
        # 01: meteor began outside FOV, ended inside FOV
        # 00: meteor began and ended outside FOV (i.e. very close to the border!)
        (x_0, y_0), (x_1, y_1) = result['FovRelative']
        in_fov_0 = 0.05 <= x_0 <= 0.95 and 0.05 <= y_0 <= 0.95
        in_fov_1 = 0.05 <= x_1 <= 0.95 and 0.05 <= y_1 <= 0.95
        result['InFov'] = str(int(in_fov_0)) + str(int(in_fov_1))

        for part in parts:
            if '=' in part:
                key, value = [elem.strip() for elem in part.split('=', 1)]
                if key in result:
                    # logging.warning('key: %s, already exists in line: %s', key, line)
                    continue
                number = RE_STARTING_WITH_NUMBER.findall(value)
                if len(number) == 1:
                    result[key] = evaluate(number[0])
                else:
                    result[key] = value
            elif '>>' in part:
                # Transform: '(1.822h,37.96)=>(1.676h,35.40)'
                x_0, y_0, x_1, y_1 = [float(val) for val in RE_ALL_NUMBERS.findall(part)]
                # Evaluated: '(1.822,37.96),(1.676,35.40)'
                result['FovEquatorial'] = (x_0, y_0), (x_1, y_1)

        logging.debug('Meteor result: %s', repr(result))
        return result

    def _set_header(self, key, line, re_expr=None):
        """ Convert the header line into a key value pair and save it
        to the internal header dictionary.

        :param str key: a key in from the METREC_HEADERS dictionary.
        :param str line: the associated metrec.log header line
        :param object re_expr: this argument may be one of 3 types,
            * regular expression that Matches whatever regex is inside the parentheses.
            * callable function that takes a single (header value) argument.
            * `None` to leave the header value unchanged.
        """
        value = line.split(':', 1)[1].strip()
        if re_expr:
            if callable(re_expr):
                value = re_expr(value)
            else:
                # NOTE: this needs to be a function
                # lstrip('0') => '09' to '9' which can be evaluated
                try:
                    value = [evaluate(val) for val in re_expr.findall(value)]
                except ValueError as exc:
                    logging.error('error in %s. Exc: %s', line.strip(), str(exc))
                if len(value) == 1:
                    value = value.pop()

        # special handling for 'Reference date'. The old METREC version
        # used "3.1.2000" format. New format is "2000-01-03".
        if key == 'Reference date':
            if value[2] > 1900:
                value[0], value[2] = value[2], value[0]

        self._header[key.replace(' ', '_')] = value

    def _parse_header_line(self, line):
        """
        :param str line: the header information line specification.
        """
        # special handling for "start of observation" (in early versions of metrec)
        if line.startswith('start of observation'):
            line = line.replace('.', ':')

        # special handling for "effective observing time" (in early versions of metrec)
        if line.startswith('Effective observing time'):
            # example: 20050512/FINEXCAM/20050512.LOG
            line = line.replace('Effective', 'effective')

        key = line.split(':', 1)[0].strip().strip('.')
        if key in METREC_HEADERS:
            re_expr = METREC_HEADERS[key]
            self._set_header(key, line, re_expr)

        elif key in self._version_header_map:
            key_new = self._version_header_map[key]
            re_expr = METREC_HEADERS[key_new]
            self._set_header(key_new, line, re_expr)

    def _load_software_version(self):
        """ Locate the 'Software: MetRecV#.#' line and extract the
        version information as a floating point number.
        """
        for i, line in enumerate(self._lines):
            if line.startswith('Software'):
                software = line.split(':', 1)[1].strip()
                self._version = float(RE_ALL_NUMBERS.findall(software)[0])
            if line.startswith('Mean Square O-C'):
                self._lines[i] = line.replace('Square', 'Squared')

    def _get_reference_file(self):
        """ Get the absolute path to the METREC log's reference stars file.

        :return: the *.ref file path, or None if the file could not be located.
        :rtype: str
        """

        for line in self._lines:
            if line.startswith('ReferenceStars'):
                # first check if the REF file is located in the session directory
                # NOTE: on Linux systems the '\' must be converted to '/' for os.path
                # routines to work properly.
                ref_file_name = line.split(':', 1)[1].strip().replace('\\', '/')
                ref_file_name = os.path.basename(ref_file_name)

                # WARNING: it's been observed that the *.ref file in the session directory
                # is different from the ReferenceStars entry in the metrec log file.
                # The ReferenceStarsFileName is the base name of the one set in the metrec
                # log file. This enforces compatibility with the original Java code.
                self._header['ReferenceStarsFileName'] = ref_file_name.lower()
                ref_file = os.path.join(os.path.dirname(self._path), ref_file_name)
                ref_file = to_file_system_case(ref_file)
                if os.path.exists(ref_file):
                    return ref_file

                # Now check if the REF file is located in sibling directory
                ref_file = os.path.join(os.path.dirname(self._path), ref_file_name)
                ref_base_name = os.path.splitext(ref_file_name)[0]
                ref_file = ref_file.replace(self._night, ref_base_name)
                if self._night[0:4] != ref_base_name[0:4]:
                    # modify the year directory as well.
                    ref_file = ref_file.replace(self._night[0:4], ref_base_name[0:4])
                ref_file = to_file_system_case(ref_file)
                if os.path.exists(ref_file):
                    return ref_file

                # Find the first *.ref file in the session directory
                # sometimes strange names are used, i.e. 17oct00.ref, etc
                ref_files = glob.glob(os.path.join(os.path.dirname(self._path), '*.[rR][eE][fF]'))
                if ref_files and len(ref_files) >= 1:
                    return ref_files[0]

                logging.warning('WARNING: reference file not found. Line: %s. File: %s', line.strip(), self._path)
                return

    def _load_header_defaults(self):
        """ Pre-load REF file header info and default values.
        """
        self._header = OrderedDict(METREC_HEADER_DEFAULT)
        key_map = {}
        for version_key in METREC_HEADERS_VERSION:
            include = evaluate(version_key.format(version=self._version))
            if include:
                key_map = METREC_HEADERS_VERSION[version_key]
                self._version_header_map = key_map

        ref_file = self._get_reference_file()
        if ref_file:
            self._header['FoundRefFile'] = ref_file
            ref_obj = RefFile(ref_file)
            for ref_key in ref_obj.header:
                value = ref_obj.header[ref_key]
                key = key_map.get(ref_key, ref_key)
                if key in METREC_HEADERS:
                    self._lines.insert(0, '%s : %s' % (ref_key, value))

        log_path = to_file_system_case(os.path.splitext(self._path)[0] + '.log')
        night = RE_SHORT_DATE.findall(os.path.basename(self._path))
        if len(night):
            self._header['Date'] = '%s/%s/%s' % night[0]  # i.e. for "pav36" night=[('2014', '10', '14')]

        self._header['MetrecLog'] = os.path.basename(log_path)  # i.e. 20010102.LOG
        self._header['CameraName'] = self._sys_code
        self._header['SystemCode'] = self._sys_code
        result = glob.glob(os.path.join(os.path.dirname(self._path), '*.[cC][fF][gG]'))
        if result:
            if len(result) == 1:
                self._header['ConfigFile'] = os.path.basename(result[0])  # i.e. 20010102.CFG
            else:
                self._header['ConfigFile'] = 'multi CFG file not allowed'
        else:
            self._header['ConfigFile'] = 'no config file'

    def parse(self):
        """ Parse the entire METREC log file content."""
        self._load_software_version()
        self._load_header_defaults()
        in_header = True
        iterator = self._lines.__iter__()
        for line in iterator:
            # RE_OBS_TIME will return in form: [('20', '08', '34')]
            hhmmss = RE_OBS_TIME.findall(line)
            in_meteor = ' Meteor #' in line
            if in_header and len(hhmmss):
                in_header = False
                self._set_mean_square_oc()

            if in_meteor and len(hhmmss):
                comment = ''
                # in observation
                # the 2nd line contains more meteor analysis
                line = line.strip()
                line += next(iterator)
                # the 3rd line contains state info
                state_line = next(iterator)
                if 'Comment:' in state_line:
                    comment = state_line.split('Comment:')[1].strip()
                    state_line = next(iterator)

                if 'Restart recognition' in line:
                    # However, on occasion a recognition restart occurs and the line
                    # format becomes (20150410/pav36):
                    #     19:42:37 Restart recognition19:58:43 Meteor #1 at (0.503,0.774)->....
                    #
                    #      snr=3.5
                    #              shower=SPO bright=0.8mag ....
                    #     20:38:12 Meteor #6 at ....
                    # discard the restart part and collect the next few lines.
                    logging.warning('WARNING: mixed meteor and restart recognition line.')
                    line = line.split('Restart recognition')[1]
                    if 'shower' not in line:
                        line += next(iterator)

                line = self._session_dates[int(hhmmss[0][0]) < 10] + line  # prepend date string
                try:
                    meteor_dict = self._parse_meteor_line(line)
                    meteor_dict['DeltaMagnitude'] = self._header['DeltaMagnitude']
                    meteor_dict['RefPosMSQE'] = self._header['RefPosMSQE']
                    meteor_dict['Comments'] = comment
                    if 'Skip saving meteor #' in state_line:
                        meteor_dict['Skipped'] = True
                except SyntaxError as exc:
                    logging.error('error parsing meteor line: %s', line)
                    logging.exception(exc)
                    raise
                self._meteors.append(meteor_dict)
            else:
                self._parse_header_line(line)

        self._set_effective_obs_time_fields()
        self._set_fov_fields()
