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
This module generates an MML schema from the METREC log and INF astrometry files.
The output may be XML or JSON.
"""
from __future__ import print_function

import os
import copy
import json
import logging
import time
import subprocess
from collections import OrderedDict
from io import open

from mrg_core.mml import metlog
from mrg_core.mml import inflog
from mrg_core.util.convert import evaluate
from mrg_core.util.convert import to_file_system_case
from mrg_core.util.diriter import SystemSessionIterator

JSON_SESSION_ORDERED = {
    'cam_session': OrderedDict([
        ('system_code', '"{SystemCode}"'),
        ('observer_code', '"{reporter}"'),
        ('version', '"MML-Python-V1.0"'),
        ('location_lon', '{Longitude}'),
        ('location_lat', '{Latitude}'),
        ('location_height', '{Altitude}'),
        ('software_code', '"{Software}"'),
        ('fov_vertical', '"{FrameSize}"'),
        ('file', [
            {'path': '"{MetrecLog}"',
             'comments': '"Logfile of the session"'},
            {'path': '"{ReferenceStarsFileName}"',
             'comments': '"Reference stars used"'},
            {'path': '"{ConfigFile}"',
             'comments': '"Configuration of the system"'},
        ]),
        ('period', OrderedDict([
            ('start', '"%d-%02d-%02dT%02d:%02d:%02d.000" % tuple({start_of_observation})[0:6]'),
            ('stop', '"%d-%02d-%02dT%02d:%02d:%02d.000" % tuple({end_of_observation})[0:6]'),
            # teff: Effective time in decimal hours
            ('teff', '{teff}'),
            # fov_guided_flag: {Operation mode} => True: 'guided', False: 'unguided'
            ('fov_guided_flag', False),
            # fov_alt: {Center of plate Alt}
            ('fov_alt', '{fov_alt}'),
            # fov_az: {Center of plate Az}
            ('fov_az', '{fov_az}'),
            ('meteor', [])  # JSON_METEOR list goes here
            ])
        )
    ])
}

JSON_METEOR_ORDERED = OrderedDict([
    # time: in format '2016-02-15T20:18:09.331'
    ('time', '"{Timestamp}"'),
    ('shower_code', '"{shower}"'),
    # begin_ra: is in degrees = (hours/24)*360
    ('begin_ra', '360.0*{FovEquatorial}[0][0]/24.0'),
    ('begin_dec', '{FovEquatorial}[0][1]'),
    ('end_ra', '360.0*{FovEquatorial}[1][0]/24.0'),
    ('end_dec', '{FovEquatorial}[1][1]'),
    ('in_fov', '"{InFov}"'),
    ('duration', '{dur}'),
    ('speed', '{vel}'),
    ('mag', '{bright}'),
    ('exposures', '{frames}'),
    ('comments', '"{Comments}"'),
    ('e_begin_ra', '(max({acc},{RefPosMSQE})/3600.0)**0.5'),
    ('e_begin_dec', '(max({acc},{RefPosMSQE})/3600.0)**0.5'),
    ('e_end_ra', '(max({acc},{RefPosMSQE})/3600.0)**0.5'),
    ('e_end_dec', '(max({acc},{RefPosMSQE})/3600.0)**0.5'),
    ('e_mag', '{DeltaMagnitude}'),
    # e_duration: Variance value of duration, assuming all MetRec observations are taken in 1/25s
    ('e_duration', '0.02'),
    ('file', [
        {'path': '"{Time}.bmp"', 'comments': '"Sum image"'},
        {'path': '"{Time}.bnd"', 'comments': '"Animation"'},
        {'path': '"{Time}.inf"', 'comments': '"Astrometry"'},
        ]),
    ('pos', [
        # JSON_POS list goes here
        ])
])

JSON_POS_ORDERED = OrderedDict([
    ('pos_no', '{pos_no}'),
    ('time', '"{timestamp}"'),
    ('mag', '{bright}'),
    ('pos_x', '{x}'),
    ('pos_y', '{y}'),
    ('pos_ra', '{alpha}/24.0*360.0'),
    ('pos_dec', '{delta}'),
    ('correction_flag', False),
    ('outlier_flag', 'not {use}'),
    ('e_pos_ra', '(max({acc},{RefPosMSQE})/3600.0)**0.5'),
    ('e_pos_dec', '(max({acc},{RefPosMSQE})/3600.0)**0.5'),
    ('e_mag', '{DeltaMagnitude}'),
])


FORMATS = {
    'software_code': lambda val: val.replace(' ', '-').upper(),
    'time': lambda val: val.replace('/', '-').replace(' ', 'T'),
    'teff': '%0.4f',
    'location_lon': '%0.6f',
    'lotitude_lon': '%0.6f',
    'fov_guided_flag': lambda val: str(val).lower(),
    'fov_alt': '%0.6f',
    'fov_az': '%0.6f',
    'begin_ra': '%0.4f',
    'begin_dec': '%0.2f',
    'end_ra': '%0.4f',
    'end_dec': '%0.2f',
    'e_begin_ra': '%0.2E',
    'e_begin_dec': '%0.2E',
    'e_end_ra': '%0.2E',
    'e_end_dec': '%0.2E',
    'e_mag': '%0.2E',
    'pos_x': '%0.3f',
    'pos_y': '%0.3f',
    'pos_ra': '%0.4f',
    'pos_dec': '%0.2f',
    # 'pos_dec': '%0.3f',
    'correction_flag': lambda val: str(val).lower(),
    'outlier_flag': lambda val: str(val).lower(),
    'e_pos_ra': '%0.2E',
    'e_pos_dec': '%0.2E',
    'mag': '%0.1f',
    'speed': '%0.1f',
    'duration': '%0.2f',
}


class MML(object):
    """ The Meteor Markup Language (MML) generator class. """

    def __init__(self, metrec_log_file, reporter):
        """
        :param str metrec_log_file:
        :param str reporter:
        """
        self._path = os.path.realpath(metrec_log_file)
        self._dir = os.path.dirname(metrec_log_file)
        self._metrec = metlog.MetLogFile(metrec_log_file)
        self._metrec.header['reporter'] = reporter
        self._session_json = MML.evaluate_json(JSON_SESSION_ORDERED, self._metrec.header)
        self._remove_non_existing_file_nodes(self._session_json['cam_session']['file'])
        self._remove_optional_session_nodes(self._session_json['cam_session'])

        meteor_list = self._session_json['cam_session']['period']['meteor']

        for i, meteor in enumerate(self._metrec.meteors):
            meteor_json = MML.evaluate_json(JSON_METEOR_ORDERED, meteor)
            self._remove_non_existing_file_nodes(meteor_json['file'])
            if not meteor_json['comments']:
                del meteor_json['comments']

            # if '05:11:54' in meteor_json['time']:
            #     pass

            inf_file = os.path.join(self._dir, meteor['InfFile'])
            inf_file = to_file_system_case(inf_file)
            try:
                inf = inflog.InfFile(inf_file)
            except IOError:
                inf = inflog.InfFile()

            self._remove_multi_timestamps_nodes(i, meteor, meteor_json, inf)

            if '.' not in meteor_json['time']:
                meteor_json['time'] += '.000'

            meteor_list.append(meteor_json)

            if 'pos' in meteor_json:
                positioned_list = meteor_json['pos']
                for pos_index, position in enumerate(inf.bright_positions):
                    position['pos_no'] = pos_index + 1
                    position['acc'] = meteor['acc']
                    position['DeltaMagnitude'] = meteor['DeltaMagnitude']
                    position['RefPosMSQE'] = meteor['RefPosMSQE']
                    result = MML.evaluate_json(JSON_POS_ORDERED, position)
                    positioned_list.append(result)
                    if pos_index == 0:
                        meteor_json['time'] = result['time']

    def _remove_non_existing_file_nodes(self, file_list):
        """ Removes any non-exist path entries in the file list.

        :param list file_list: reference to the list of files in the
            session or meteor dictionary node.
        """
        for i, file_entry in reversed(list(enumerate(file_list))):
            path = os.path.join(self._dir, file_entry['path'])
            if os.path.splitext(path)[1].lower() == '.ref' \
                    and 'FoundRefFile' in self._metrec.header:
                # ignore reference stars files, they are sometimes located in
                # sibling directories
                path = self._metrec.header['FoundRefFile']
            else:
                path = to_file_system_case(path)

            if not os.path.exists(path):
                del file_list[i]

            # check that the extension case-sensitivity is saved
            file_name = os.path.basename(path)
            if file_entry['path'] != file_name:
                file_entry['path'] = file_name

    def _remove_optional_session_nodes(self, cam_session_json):
        """ Remove the nodes from the 'cam_session' that are not defined and
        deemed optional. These are the following tags,

            * fov_vertical
            * location_lat
            * location_lon
            * location_height
            * fov_alt
            * fov_az

        :param OrderedDict cam_session_json: the 'cam_session' reference node.
        """
        if cam_session_json['fov_vertical'] == 0:
            del cam_session_json['fov_vertical']
        if self._metrec.version >= 5.0:
            del cam_session_json['fov_vertical']

        if cam_session_json['location_lat'] is None:
            del cam_session_json['location_lat']

        if cam_session_json['location_lon'] is None:
            del cam_session_json['location_lon']

        if cam_session_json['location_height'] is None:
            del cam_session_json['location_height']

        if cam_session_json['period']['fov_alt'] is None:
            del cam_session_json['period']['fov_alt']

        if cam_session_json['period']['fov_az'] is None:
            del cam_session_json['period']['fov_az']

    def _remove_multi_timestamps_nodes(self, index, meteor, meteor_json, inf):
        """ Determines which meteor get's the INF file in the situation when
        multiple meteors have the same timestamp. The 'pos' and 'file' nodes will
        be removed if the INF does not correspond to the current meteor instance.

        :param int index:
        :param dict meteor:
        :param dict meteor_json:
        :param InfLog inf:
        """
        if 'HasInf' not in meteor:
            # Search the next few meteors and collect a list of
            # meteors with the same timestamp
            same_inf_list = []
            if not len(same_inf_list):
                for meteor_next in self._metrec.meteors[index+1:]:
                    if meteor['InfFile'] != meteor_next['InfFile']:
                        break
                    same_inf_list.append(meteor_next)

            # If there are meteors with the same timestamp, then
            # figure out which one of them has the same relative FOV
            # as the INF file.
            if len(same_inf_list):
                meteor['HasInf'] = True
                for meteor_next in same_inf_list:
                    meteor_next['HasInf'] = False
                    if inf.fov_position == meteor_next['FovRelative']:
                        meteor_next['HasInf'] = True
                        meteor['HasInf'] = False

        # if multiple meteors share the same INF file, then
        # remove the 'file' and 'pos' keys from the meteors
        # that do not match
        if 'HasInf' in meteor and not meteor['HasInf']:
            del meteor_json['file']
            del meteor_json['pos']

    @property
    def metlog(self):
        """ Retrieve a reference to the :class:`MetLogFile` object.

        :return: the reference to the loaded metrec log file object.
        :rtype: MetLogFile
        """
        return self._metrec

    @property
    def path(self):
        """ Retrieve the absolute path to the metrec log file"""
        return self._path

    @property
    def session(self):
        """ Retrieve the root session node. This reference may
        be used to access all the meteor and position entries.
        For instance::

            camera = mml_obj['system_code']
            meteor_list = mml_obj['period']['meteor']

        :return: the session reference.
        :rtype: OrderedDict
        """
        return self._session_json['cam_session']

    def get_json(self, format_values=True):
        """
        :param bool format_values: if True then the numeric values will be returned
            as formatted string. If False then the numeric values remain numeric
            types (int or float).
        :return: the JSON object that contains the METREC session data.
        :rtype: OrderedDict
        """
        if self._metrec.version <= 3.5:  # NOTE: the version # is to be determined
            FORMATS['pos_dec'] = '%0.2f'
        else:
            FORMATS['pos_dec'] = '%0.3f'

        if format_values:
            return MML.format_json(self._session_json, FORMATS)
        else:
            return self._session_json

    def get_json_string(self, format_values=True):
        """
        :param bool format_values: if True then the numeric values will be returned
            as formatted string. If False then the numeric values remain numeric
            types (int or float).
        :return: the JSON formatted string.
        :rtype: str
        """
        json_obj = self.get_json(format_values)
        return json.dumps(json_obj, ensure_ascii=False, indent=4)

    @staticmethod
    def transform_to_java_format(xml):
        """ Translate the JSON xml formatted string to an XML format that
        is identical to the metrec2mml JAVA version. This is only needed
        for validation and testing.

        :param str xml:
        :return: the new XML string that is equivalent to the JAVA version.
        :rtype: str
        """
        result = ''
        # make the <file> tag a one liner by removing newline and tab characters
        # from child elements.
        for part in xml.split('file>'):
            if part.endswith('</'):
                part = part.replace('\n', '').replace('\t', '')
            if part.endswith('/vmo>\n'):
                result += part
            else:
                result += part + 'file>'

        # add a new line after the <e_duration> tag.
        result = result.replace('</e_duration>\n\t\t\t<file>',
                                '</e_duration>\n\n\t\t\t<file>')
        result = result.replace('</e_duration>\n\t\t</meteor>',
                                '</e_duration>\n\n\t\t</meteor>')
        # add a new line at the last <file> tag.
        result = result.replace('</file>\n\t\t\t<pos>',
                                '</file>\n\n\t\t\t<pos>')
        # add namespace info to location tags
        result = result.replace('<location_lon>',
                                '<location_lon xmlns=\'http://vmo.imo.net\'>')
        result = result.replace('<location_lat>',
                                '<location_lat xmlns=\'http://vmo.imo.net\'>')
        result = result.replace('<location_height>',
                                '<location_height xmlns=\'http://vmo.imo.net\'>')
        return result

    def get_xml_string(self, format_values=True):
        """
        :param bool format_values: if True then the numeric values will be returned
            as formatted string. If False then the numeric values remain numeric
            types (int or float).
        :return: the XML formatted string.
        :rtype: str
        """
        result = '<?xml version="1.0" encoding="UTF-8"?>\n'
        result += '<vmo version="1.0" xmlns="http://www.imo.net">\n'
        result += MML.json_to_xml(self.get_json(format_values))
        result += '\n</vmo>\n'
        return self.transform_to_java_format(result)

    @staticmethod
    def format_json(node, formats, deep_copy=True):
        """
        :param dict node: may be a dict or list object
        :param dict formats: the formatting specifiers for each JSON key.
        :param bool deep_copy: make a deep mempry copy of the node argument before
            processing. This is needed when templates are passed as the initial
            argument.
        :return: the JSON object with it's key values in a formatted representation.
        :rtype: dict
        """
        if deep_copy:
            node = copy.deepcopy(node)

        for key in node:
            value = node[key]
            if isinstance(value, dict):
                MML.format_json(value, formats, False)
            elif isinstance(value, list):
                for item in value:
                    MML.format_json(item, formats, False)
            else:
                if key in formats and value is not None:
                    formatter = formats[key]
                    if callable(formatter):
                        value = formatter(value)
                    else:
                        value = formatter % value
                        if formatter.endswith('E'):
                            # work around for the single exponent (in java metrec2mml format)
                            # only needed for validation purposes at the moment
                            value = value.replace('E-0', 'E-').replace('E+0', 'E+')
                            if value.endswith('E+0'):
                                value = value.replace('E+0', 'E0')
                node[key] = value

        return node

    @staticmethod
    def evaluate_json(template, values, deep_copy=True):
        """
        :param dict template:
        :param dict values:
        :param bool deep_copy:
        :return: the template argument or a copy of it.
        :rtype: dict
        :raises ValueError: is raised when the node value evaluation fails.
        """
        if deep_copy:
            template = copy.deepcopy(template)

        for key in template:
            value = template[key]
            if isinstance(value, dict):
                MML.evaluate_json(value, values, False)
            elif isinstance(value, list):
                for item in value:
                    MML.evaluate_json(item, values, False)
            elif isinstance(value, str):
                value = value.format(**values)
                try:
                    template[key] = evaluate(value)
                except (SyntaxError, TypeError) as exc:
                    msg = 'Failed to evaluate value: %s, key: %s' % (value, key)
                    logging.error(msg)
                    logging.exception(exc)
                except ValueError:
                    raise

            else:
                template[key] = value

        return template

    @staticmethod
    def json_to_xml(json_obj, line_padding='', list_key=''):
        """
        :param dict json_obj:
        :param str line_padding:
        :param str list_key:
        :return: the XML formatted string.
        :rtype: str
        """
        result_list = list()
        if isinstance(json_obj, list):
            for sub_elem in json_obj:
                if list_key:
                    result_list.append('%s<%s>' % (line_padding, list_key))
                result_list.append(MML.json_to_xml(sub_elem, '\t' + line_padding))
                if list_key:
                    result_list.append('%s</%s>' % (line_padding, list_key))
            return '\n'.join(result_list)

        if isinstance(json_obj, dict):
            for tag_name in json_obj:
                sub_obj = json_obj[tag_name]
                if isinstance(sub_obj, list):
                    lines = MML.json_to_xml(sub_obj, line_padding, tag_name)
                    result_list.append(lines)
                elif isinstance(sub_obj, dict):
                    result_list.append('%s<%s>' % (line_padding, tag_name))
                    lines = MML.json_to_xml(sub_obj, "\t" + line_padding)
                    result_list.append(lines)
                    result_list.append('%s</%s>' % (line_padding, tag_name))
                else:
                    sub_obj = repr(sub_obj).strip('"').strip("'")
                    result_list.append('%s<%s>%s</%s>'
                                       % (line_padding, tag_name, sub_obj, tag_name))

            return '\n'.join(result_list)

        return '%s%s' % (line_padding, json_obj)


class MMLJava(object):
    """ This class calls the metrec2mml.jar java application.
    WARNING: This will eventually be deprecated in favour of the MML class.
    """

    def __init__(self, path, reporter):
        """
        :param str path: the metrec log file
        :param str reporter:
        :raises IOError:
        """
        if not os.path.exists(path):
            raise IOError('File does not exist: %s' % repr(path))

        if not os.path.isfile(path):
            raise IOError('Path is not a file: %s' % repr(path))

        self._path = path
        self._warnings = []
        self._errors = []
        self._xml = ''

        cwd = os.path.dirname(os.path.realpath(__file__))
        app_path = os.path.abspath(os.path.join(cwd, 'metrec2mml.jar'))
        if not os.path.exists(app_path):
            raise IOError('File does not exist: %s' % repr(app_path))

        iterator = SystemSessionIterator(os.path.dirname(path))
        result = next(iterator)  # (path, yyyy, yyyymmdd, sys_code)
        directory = result[0]
        system_code = result[3]
        output_dir = directory
        if len(output_dir) > 2 and output_dir[1] == ':':
            if output_dir[0].lower() != 'c':
                sub_dir = output_dir[2:]
                sub_dir = sub_dir.strip('/').strip('\\')
                sub_dir = sub_dir.replace('/', '_').replace('\\', '_').replace(' ', '_')
                output_dir = 'c:/tmp/' + sub_dir
                try:
                    os.makedirs(output_dir)
                except OSError:
                    pass

        self._args = {
            'app_path': app_path,
            'reporter': reporter,
            'directory': directory,
            'system': system_code,
            'output': output_dir,
        }
        self.invoke_command_line()
        if output_dir.startswith('c:/tmp'):
            try:
                os.rmdir(output_dir)
            except OSError:
                pass

    def invoke_command_line(self):
        """ Execute the metrec.jar application."""
        mml_cmdline = 'java -jar "{app_path}" "{directory}" {system} {reporter} "{output}"'
        dir_path = self._args['output']
        feedback_file = os.path.join(dir_path, 'vmo_feedback.txt')
        vmo_xml_file = os.path.join(dir_path, 'vmo_data.xml')

        cmd_line = mml_cmdline.format(**self._args)

        time_0 = time.time()
        logging.info('metrec2mml.jar process: %s', cmd_line)
        process = subprocess.Popen(args=cmd_line,
                                   shell=True,
                                   # stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        if process.pid == 0:
            raise IOError('Failed to start metrec2mml.jar conversion')

        line = process.stderr.readline()
        while line:
            logging.error('metrec2mml.jar stderr: ' + line.strip())
            line = process.stderr.readline()
        process.stderr.close()

        line = process.stdout.readline()
        while line:
            line = line.decode('utf-8')
            if not line.startswith('PARSING OK'):
                logging.info('metrec2mml.jar stdout: ' + line.strip())
            line = process.stdout.readline()

            logging.info('Finished metrec2mml.jar conversion in %0.2fsec', time.time() - time_0)
        process.stdout.close()

        if not os.path.exists(feedback_file):
            raise IOError('File does not exist: %s' % repr(feedback_file))

        with open(feedback_file, 'r', encoding='utf-8') as file_obj:
            for line in file_obj.readlines():
                msg = line.strip()
                # msg = "metrec2mml (%s): %s " % (feedback_file, line.strip())
                if "warning" in line.lower():
                    self._warnings.append(msg)
                else:
                    self._errors.append(msg)

        # remove the temporary output files
        os.remove(feedback_file)

#        if len(self.warnings):
#            logging.warning('metrec2mml.jar warnings:\n' + '\n'.join(self.warnings))
#        if len(self.errors):
#            logging.error('metrec2mml.jar errors:\n' + '\n'.join(self.errors))

        if not os.path.exists(vmo_xml_file):
            raise IOError('File does not exist: %s' % repr(vmo_xml_file))

        with open(vmo_xml_file, 'r', encoding='utf-8') as file_obj:
            self._xml = file_obj.read()

        os.remove(vmo_xml_file)

    def get_xml_string(self):
        """ Retrieve the contents of the vmo_data.xml file.
        :return: the XML as a string
        :rtype: str
        """
        return self._xml

    @property
    def errors(self):
        """
        :return: the list of error messages from the
            VMO metrec2mml.jar application
        :rtype: list
        """
        return self._errors

    @property
    def warnings(self):
        """
        :return: the list of warning messages from the
            VMO metrec2mml.jar application
        :rtype: list
        """
        return self._warnings
