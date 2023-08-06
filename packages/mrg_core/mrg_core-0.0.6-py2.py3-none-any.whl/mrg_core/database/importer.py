#!/usr/bin/env python
#   --------------------------------------------------------------------------
#   Copyright 2013 SRE-F, ESA (European Space Agency)
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
VMO data directory import into MySQL utility program.
"""
from __future__ import print_function

import os
import sys
import time
import subprocess
import logging
import mimetypes
import shlex
import platform
import shutil
import unicodedata
from math import pi

from future.builtins import input

import ephem

try:
    from lxml import etree
except ImportError as imp_exc:
    print('WARNING: pip install lxml')

from mrg_core.util import diriter
from mrg_core.util.database import DatabaseConnection
from mrg_core.util.database import DatabaseConnectionException

from mrg_core.mml.mml import MML

VMO_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/..')

NAMESPACE = {
    "imo": "http://www.imo.net",
    "vmo": "http://vmo.imo.net"
}

FAST_IMPORT = False
CONTINUE_PROCESSING = True

logging.NOTICE = 60
logging.addLevelName(logging.NOTICE, "NOTICE")

log = None


# this is specific to Python 2.6 which lacks a check_output function
if "check_output" not in dir(subprocess):  # duck punch it in!
    def _check_output_impl(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout arg not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, _ = process.communicate()  # _ = err (unused)
        ret_code = process.poll()
        if ret_code:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(ret_code, cmd)
        return output
    subprocess.check_output = _check_output_impl


class Counters(object):
    """ Counters to keep trak of error and warning and other user defined
    events. """

    def __init__(self):
        # self._err_count = 0
        # self._warn_count = 0
        self._counters = {}
        self._iter_index = -1
        self.init_counter('warning')
        self.init_counter('error')
        self.init_counter('inserted')
        self.init_counter('select')

    def __iter__(self):
        self._iter_index = -1
        return self

    def __next__(self):
        """ Python 3 compatibility fix for iterator class """
        return self.next()

    def next(self):
        """
        :return: the next counter key in the iterator.
        :rtype: str
        :raises StopIteration:
        """
        self._iter_index += 1
        if self._iter_index >= len(self._counters):
            raise StopIteration
        return list(self._counters.keys())[self._iter_index]

    def __getitem__(self, key):
        return self._counters[key]

    def __add__(self, counter):
        for key in counter:
            if key in self._counters:
                self._counters[key] += counter[key]
            else:
                self._counters[key] = counter[key]
        return self

    def init_counter(self, name):
        """
        :param str name:
        """
        self._counters[name] = 0

    def increment_counter(self, name):
        """
        :param str name:
        """
        self._counters[name] += 1

    def reset_counters(self):
        """ Rest all the counters. """
        for name in self._counters:
            self._counters[name] = 0

    def get_count(self, name):
        """
        :param str name:
        :return:
        :rtype: int
        """
        return self._counters[name]

    def get_counters(self):
        """
        :return:
        :rtype: dict
        """
        return self._counters


class Logger(object):
    """ A progress reporting class that aids in configuring the logging
    and keeps track of several counters related to errors and warnings.
    User defined counters can also be defined such as records inserted
    into database / table.
    """

    def __init__(self, log_file, level):
        dir_name = os.path.dirname(log_file)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)

        self._log = logging.root
        if len(logging.root.handlers) == 0:
            formatter = logging.Formatter("%(asctime)s %(levelname)-7s %(message)s")
            log_cout = logging.StreamHandler(sys.stdout)
            log_cout.setFormatter(formatter)
            log_fout = logging.FileHandler(log_file)
            log_fout.setFormatter(formatter)
            self._log.setLevel(level)
            self._log.addHandler(log_cout)
            self._log.addHandler(log_fout)
        elif len(logging.root.handlers) == 1:
            log_fout = logging.FileHandler(log_file)
            log_fout.setFormatter(logging.root.handlers[0].formatter)
            self._log.addHandler(log_fout)

        self._log.debug_org = logging.debug
        self._log.info_org = logging.info
        self._log.warning_org = logging.warning
        self._log.error_org = logging.error
        self._log.exception_org = logging.exception

        logging.debug = self.debug
        logging.info = self.info
        logging.warning = self.warning
        logging.error = self.error
        logging.exception = self.exception

        self._counters = Counters()

    @property
    def counters(self):
        """
        :return: the Counters dictionary
        :rtype: Counters
        """
        return self._counters

    def print_progress(self):
        """ Print the counters to the stdout stream.
        """
        msg = repr(self._counters.get_counters())
        sys.stdout.write(msg + '\b' * len(msg))

    def set_level(self, level):
        """
        :param int level:
        """
        level = logging.getLevelName(level)
        self._log.setLevel(level)

    def _update_counters(self, *args):
        """
        :param list args:
        """
        if 'SQL: ' in args[0]:
            for arg in args:
                if isinstance(arg, str):
                    if arg.startswith('SELECT'):
                        self._counters.increment_counter('select')
                    elif arg.startswith('INSERT'):
                        self._counters.increment_counter('inserted')

    def debug(self, *args):
        """ Log debug message.
        :param list args:
        """
        self._update_counters(*args)
        self._log.debug_org(*args)

    def info(self, *args):
        """ Log debug message.
        :param list args:
        """
        self._update_counters(*args)
        self._log.info_org(*args)

    def warning(self, *args):
        """ Log debug message and warning error counter.
        :param list args:
        """
        self._counters.increment_counter('warning')
        self._log.warning_org(*args)

    def error(self, *args):
        """ Log error message and increment error counter.
        :param list args:
        """
        self._counters.increment_counter('error')
        self._log.error_org(*args)

    def exception(self, exc):
        """ Log exception and increment error counter.
        :param Exception exc:
        """
        self._counters.increment_counter('error')
        self._log.error_org(exc, exc_info=1)

    def notice(self, *args):
        """ Log notice message.
        :param list args:
        """
        self._update_counters(*args)
        self._log.log(logging.NOTICE, *args)


class VMOXMLValidator(object):
    """ This class checks whether the night being imported has already been imported by
    looking for duplicate entries. """

    def __init__(self, mml_source):
        """
        :param MMLDataSource mml_source:
        """
        self._xml_conn = mml_source.xml
        self._db_conn = mml_source.dbconn

        log.counters.init_counter('sessions')
        log.counters.init_counter('periods')
        log.counters.init_counter('meteors')
        log.counters.init_counter('positions')

    def get_summary(self):
        """
        :return: the summary report
        :rtype: str
        """
        system_code = get_node_text(self._xml_conn, "//imo:system_code")
        period_start = get_node_text(self._xml_conn, "//imo:start")
        period_stop = get_node_text(self._xml_conn, "//imo:stop")

        counters = ['sessions', 'periods', 'meteors', 'positions']
        date = period_start[0:10]
        time0 = period_start[12:19]
        time1 = period_stop[12:19]
        msg = "%-10s %s from %s to %s, validated:" \
              % (system_code, date, time0, time1)
        for name in counters:
            # sessions and periods are always 1, only display multiple
            # entry counts
            if name == 'sessions' and log.counters.get_count(name) == 1:
                continue

            if name == 'periods' and log.counters.get_count(name) == 1:
                continue

            msg += " %3d %s," % (log.counters.get_count(name), name)

        msg += " %3d errors" % (log.counters.get_count('error'))
        msg += " %3d warnings" % (log.counters.get_count('warning'))
        return msg.strip(',')

    def validate(self):
        """ Validates the times and codes
        """
        self.check_times()
        self.check_codes()

    def check_times(self):
        """ Check the chronological order of periods and and positions.
        """
        # Run over the sessions
        sessions = self._xml_conn.xpath("/imo:vmo/imo:cam_session", namespaces=NAMESPACE)
        for session in sessions:
            log.counters.increment_counter('sessions')
            location_info = {}
            self.check_location_code(session, location_info)

            # Check the period times
            periods = session.xpath("imo:period", namespaces=NAMESPACE)
            previous_period_stop = ["0"]
            for period in periods:
                log.counters.increment_counter('periods')
                self.check_period_times(period, previous_period_stop)

                self.check_duplicate_times(period)

                self.check_solar_altitude(period, location_info)

                # Check the meteor times
                meteors = period.xpath("imo:meteor", namespaces=NAMESPACE)
                previous_meteor_time = ["0"]
                for meteor in meteors:
                    log.counters.increment_counter('meteors')
                    self.check_meteor_times(meteor, previous_meteor_time)

                    # Check the position times and numbers
                    positions = meteor.xpath("imo:pos", namespaces=NAMESPACE)
                    previous_position_time_and_num = ["0", 0]
                    # previous_position_no = 0
                    for position in positions:
                        log.counters.increment_counter('positions')
                        # log.print_progress()
                        self.check_position_times(position,
                                                  previous_position_time_and_num)

    def check_codes(self):
        """ Checks if the the codes in the XML document reside in
        the database.
        """
        warning_type = 1
        error_type = 2

        table_column = [
            ('observer', 'observer_code', error_type),
            ('location', 'location_code', error_type),
            ('cam_system', 'system_code', warning_type),
            ('cam_lens', 'lens_code', warning_type),
            ('cam_prism', 'prism_code', warning_type),
            ('cam_intensifier', 'intensifier_code', warning_type),
            ('cam_camera', 'camera_code', warning_type),
            ('cam_digitizer', 'digitizer_code', warning_type),
            ('cam_software', 'software_code', warning_type),
        ]

        for table, column, msg_type in table_column:
            xpath_select = "//imo:%s" % column
            codes = self._xml_conn.xpath(xpath_select, namespaces=NAMESPACE)
            for code in codes:
                code = code.text
                sql_select = "SELECT %s FROM %s WHERE %s = '%s'" \
                             % (column, table, column, code)
                row = self._db_conn.execute_get_row(sql_select)
                if row is None:
                    if msg_type == error_type:
                        log.error("%s '%s' needs to be registered in the "
                                  "database first." % (column, code))
                    else:
                        log.warning("%s '%s' is not registered in the database yet. "
                                    "Don't worry, auto-registration applies."
                                    % (column, code))
                else:
                    log.debug("found '%s' %s in database" % (code, column))

    def check_duplicate_times(self, period_node):
        """
        :param Node period_node:
        """
        system_code = get_node_text(period_node.getparent(), "imo:system_code")
        period_start = get_node_text(period_node, "imo:start")
        period_stop = get_node_text(period_node, "imo:stop")

        # Duplicate obervations: this period cannot be covered by another
        # session in the database
        sql_select = "SELECT entry_code FROM entry WHERE"
        sql_select += " ("
        sql_select += "(start >= '{time}' AND stop <= '{time}')".format(time=period_start)
        sql_select += " OR "
        sql_select += "(start >= '{time}' AND stop <= '{time}')".format(time=period_stop)
        sql_select += " OR "
        sql_select += "(start > '{start_time}' AND stop < '{stop_time}')"\
            .format(start_time=period_start, stop_time=period_stop)
        sql_select += ")"
        sql_select += " AND entry_code LIKE '%%-%s'" % system_code

        row = self._db_conn.execute_get_row(sql_select)
        if row is not None:
            duplicate_code = row['entry_code']
            # raise ImportException("The database already contains an observation
            # from the same system at the same time: %s." % duplicateCode)
            log.warning("The database already contains an observation from the "
                        "same system at the same time: %s." % duplicate_code)

    def check_solar_altitude(self, period_node, location_info):
        """
        :param Node period_node:
        :param dict location_info:
        """

        def shared_solalt(latitude, longitude, period):
            """

            :param float latitude:
            :param float longitude:
            :param str period:
            :return:
            :rtype: float
            """
            sun = ephem.Sun(ephem.Date(period.replace('T', ' ')))
            sun.compute()

            obs = ephem.Observer()
            obs.date = ephem.Date(period.replace('T', ' '))
            obs.long = ephem.degrees(longitude) * pi / 180.0  # radians
            obs.lat = ephem.degrees(latitude) * pi / 180.0  # radians

            sun.compute(obs)
            return sun.alt * 180 / pi

        def shared_solalt2(location_code, period):
            """

            :param str location_code:
            :param str period:
            :return:
            :rtype: float
            """
            row = self._db_conn.execute_get_row("SELECT lon, lat, height FROM location "
                                                "WHERE location_code='{}'".format(location_code))
            if row:
                return shared_solalt(float(row['lat']), float(row['lon']), period)
            else:
                log.error("solalt not found")

        period_start = get_node_text(period_node, "imo:start")
        period_stop = get_node_text(period_node, "imo:stop")

        location_code = location_info['location_code']
        latitude = float(location_info['location_lat'])
        longitude = float(location_info['location_lon'])

        if location_code:
            start_alt = shared_solalt2(location_code, period_start)
            stop_alt = shared_solalt2(location_code, period_stop)
        else:
            start_alt = shared_solalt(latitude, longitude, period_start)
            stop_alt = shared_solalt(latitude, longitude, period_stop)

        if start_alt > -6:
            log.warning("the sun was above -6 degrees altitude at the beginning of the "
                        "period (time: '%s')." % period_start)
        if stop_alt > -6:
            log.warning("the sun was above -6 degrees altitude at the end of the "
                        "period (time: '%s')." % period_stop)

    def check_location_code(self, session, location_dict_out=None):
        """
        :param Node session:
        :param dict location_dict_out:
        :raises LocationException:
        """
        # Get the location code for later use (to check solar altitude)
        location_code = get_node_text(session, "imo:location_code")
        if location_code is None:
            # If no location code is given, there should be coordinates
            # defined -- give a notice
            longitude = get_node_text(session, "vmo:location_lon")
            latitude = get_node_text(session, "vmo:location_lat")
            height = get_node_text(session, "vmo:location_height")
            if latitude is None and longitude is None:
                raise LocationException()

            if height is not None:
                sql_select = "SELECT location_code FROM location " \
                             "WHERE lon = %s AND lat = %s AND height = %s" \
                             % (longitude, latitude, height)
            else:
                sql_select = "SELECT location_code FROM location " \
                             "WHERE lon = %s AND lat = %s" \
                             % (longitude, latitude)

            row = self._db_conn.execute_get_row(sql_select)
            if row is not None:
                location_code = row['location_code']
            else:
                log.warning("The coordinates have not been registered as an observing "
                            "location in the database yet. "
                            "Don't worry, auto-registration applies.")
        else:
            longitude = ''
            latitude = ''
            # height = ''

        location_dict_out['location_code'] = location_code
        location_dict_out['location_lon'] = longitude
        location_dict_out['location_lat'] = latitude

    def check_period_times(self, period_node, previous_period_stop):
        """
        :param Node period_node:
        :param Node previous_period_stop:
        """
        # Period start should come before period stop
        period_start = get_node_text(period_node, "imo:start")
        period_stop = get_node_text(period_node, "imo:stop")
        log.debug("validating period '%s' to '%s" % (period_start, period_stop))

        if period_stop < period_start:
            log.error("chronology error. Period ended before it began. "
                      "(Period start: '%s'. Period stop: '%s')." % (period_start, period_stop))

        # Periods should be chronological
        if period_start < previous_period_stop[0]:
            log.error("chronology error. Period started before the preceeding ended. "
                      "(Period start: '%s')." % period_start)

        previous_period_stop[0] = period_stop

    def check_meteor_times(self, meteor_node, previous_meteor_time):
        """
        :param Node meteor_node:
        :param list previous_meteor_time: used as a return placeholder
          using a list with a single element of type str.
        """
        period_start = get_node_text(meteor_node.getparent(), "imo:start")
        period_stop = get_node_text(meteor_node.getparent(), "imo:stop")
        meteor_time = get_node_text(meteor_node, "imo:time")
        log.debug("validating meteor at time '%s'" % (meteor_time))
        # Meteor times should be chronological
        if meteor_time < previous_meteor_time[0]:
            log.warning("chronology warning. Meteor at '%s' is not in chronological "
                        "order with the preceeding meteor at '%s'."
                        % (meteor_time, previous_meteor_time))

        # Meteor times should be withing the period bounds
        if meteor_time < period_start or meteor_time > period_stop:
            log.error("chronology error. Meteor at time '%s' is outside the period "
                      "interval. (Period start: '%s'. Period stop: '%s'.)"
                      % (meteor_time, period_start, period_stop))

        previous_meteor_time[0] = meteor_time

    def check_position_times(self, position_node, previous_position_time_and_num):
        """
        :param Node position_node:
        :param list previous_position_time_and_num:
        """
        # Position times should be chronological
        position_time = get_node_text(position_node, "imo:time")
        msg = "validating position at time '%s'" % (position_time)
        sys.stdout.write(msg + '\b' * len(msg))

        prev_time = previous_position_time_and_num[0]
        if position_time < prev_time:
            log.warning("chronology warning. Position at time '%s' is not in "
                        "chronological order with the preceding position." % position_time)

        # Position numbers should be sequential
        position_num = int(get_node_text(position_node, "imo:pos_no"))
        prev_num = previous_position_time_and_num[1] + 1
        if position_num != prev_num:
            log.warning("sequence problem. Position number '%d' at time '%s' is "
                        "not in sequence with the preceding position number."
                        % (position_num, position_time))

        previous_position_time_and_num[0] = position_time
        previous_position_time_and_num[1] = position_num


class VMOXMLImporter(object):
    """ XML to database importer class. """

    def __init__(self, mml_source, remove_empty_position=False):
        """
        :param MMLDataSource mml_source:
        """
        self._date = mml_source.night
        self._xml_conn = mml_source.xml
        self._db_conn = mml_source.dbconn
        self._directory = mml_source.get_dest_url()
        self._cursor = None
        self._session = {}
        self._remove_empty_position = remove_empty_position

    def import_into_db(self, commit=True):
        """
        :param bool commit:
        """
        try:
            # self._cursor = self._con.cursor()
            # self._cursor.execute("BEGIN;")
            self._call_import()
            if commit:
                log.info("Committing import changes to database. %s", repr(log.counters.get_counters()))
                self._db_conn.commit()
            else:
                log.info("Rolling back database import changes.")
                self._db_conn.rollback()

        except Exception as ex:
            log.exception(ex)
            log.notice("Rolling back database import changes due to exception.")
            self._db_conn.rollback()

    def _import_file(self, file_node):
        """
        :param Node file_node:
        :return: the file path
        :rtype: str
        """

        directory = self._directory

        # Determine path
        file_name = get_node_text(file_node, "imo:path")
        if directory:
            file_path = os.path.join(directory, file_name)
        else:
            file_path = file_name

        # force Linux path separators
        file_path = file_path.replace('\\', '/')

        sql_select = "SELECT * FROM files WHERE path = '%s';" % file_path
        row = self._db_conn.execute_get_row(sql_select)
        if row is None:
            file_type = mimetypes.guess_type(file_path)[0]
            if file_type is None:
                file_type = 'text/plain'

            new_row = {
                'path': file_path,
                'comments': get_node_text(file_node, 'imo:comments'),
                'time_created': 'NOW()',
                'file_type': file_type,
            }
            self._db_conn.execute_insert('files', new_row)

        return file_path

    def _import_file_entries(self, context_node, table_name, new_row):
        """
        :param Node context_node:
        :param str table_name:
        :param dict new_row:
        """
        if FAST_IMPORT:
            return

        files = context_node.xpath("imo:file", namespaces=NAMESPACE)
        for file_node in files:
            # Register the path in the "shared.files" table
            new_row['path'] = self._import_file(file_node)
            # Link to table entry
            self._db_conn.execute_insert(table_name, new_row)

    def _import_cam_period(self, period_node, entry_code):
        """

        :param Node period_node:
        :param str entry_code:
        """
        def shared_add_period(entry_code):
            """

            :param str entry_code:
            :return: the period code
            :rtype: str
            """
            sql_select = "SELECT period_number FROM period " \
                         "WHERE entry_code='%s' ORDER BY period_number DESC" % entry_code
            row = self._db_conn.execute_get_row(sql_select)
            if row is None:
                row = [0]
            period_num = row[0] + 1
            values_dict = {
                'period_code': entry_code + '-P%03d' % period_num,
                'entry_code': entry_code,
                'period_number': period_num,
            }
            self._db_conn.execute_insert('period', values_dict)

            return values_dict['period_code']

        # Insert into period table
        period_code = shared_add_period(entry_code)

        # Insert into cam_period table
        cam_period = {}
        fields = self._db_conn.get_column_names("cam_period")
        for field in fields:
            cam_period[field] = get_node_text(period_node, "imo:%s" % field)
        cam_period['period_code'] = period_code
        cam_period['entry_code'] = entry_code

        self._db_conn.execute_insert('cam_period', cam_period)

        # Link files to period
        new_row = {
            'period_code': period_code
        }
        self._import_file_entries(period_node, 'period_file', new_row)

        # Run over the meteors
        meteors = period_node.xpath("imo:meteor", namespaces=NAMESPACE)
        for meteor_node in meteors:
            if self._remove_empty_position:
                if len(meteor_node.xpath("imo:pos", namespaces=NAMESPACE)) == 0:
                    timestamp = get_node_text(meteor_node, "imo:%s" % 'time')
                    log.info('Ignoring meteor at time %s, no positions found.', timestamp)
                    continue
            self._import_cam_meteor(meteor_node, entry_code, period_code)

    def _import_cam_meteor(self, meteor_node, entry_code, period_code):
        """
        :param Node meteor_node:
        :param str entry_code:
        :param str period_code:
        """
        def shared_add_meteor(entry_code):
            """

            :param str entry_code:
            :return:
            :rtype: str
            """
            sql_select = "SELECT meteor_number FROM meteor WHERE entry_code='%s' " \
                         "ORDER BY meteor_number DESC" % entry_code
            row = self._db_conn.execute_get_row(sql_select)
            if row is None:
                row = {'meteor_number': 0}
            meteor_num = row['meteor_number'] + 1
            values_dict = {
                'meteor_code': entry_code + '-M%03d' % meteor_num,
                'entry_code': entry_code,
                'meteor_number': meteor_num,
            }
            self._db_conn.execute_insert('meteor', values_dict)

            return values_dict['meteor_code']

        meteor_code = shared_add_meteor(entry_code)

        cam_meteor = {}
        fields = self._db_conn.get_column_names("cam_meteor")
        for field in fields:
            cam_meteor[field] = get_node_text(meteor_node, "imo:%s" % field)
        cam_meteor['entry_code'] = entry_code
        cam_meteor['meteor_code'] = meteor_code
        cam_meteor['period_code'] = period_code

        # The original shower code is ALSO stored in a separate field, so that
        # the main shower_code can be recomputed in the database
        cam_meteor['shower_code_original'] = get_node_text(meteor_node, "imo:shower_code")

        self._db_conn.execute_insert('cam_meteor', cam_meteor)

        # Link files to meteors
        new_row = {
            'meteor_code': meteor_code,
        }
        self._import_file_entries(meteor_node, 'meteor_file', new_row)

        # Run over the positions
        positions = meteor_node.xpath("imo:pos", namespaces=NAMESPACE)
        for position_node in positions:
            self._import_cam_position(position_node, meteor_code)

    def _import_cam_position(self, position_node, meteor_code):
        """
        :param Node position_node:
        :param str meteor_code:
        """

        # Insert into cam_pos table
        cam_pos = {}
        fields = self._db_conn.get_column_names("cam_pos")
        for field in fields:
            cam_pos[field] = get_node_text(position_node, "imo:%s" % field)
        cam_pos['meteor_code'] = meteor_code

        self._db_conn.execute_insert('cam_pos', cam_pos)

        # Link files to meteors
        new_row = {
            'meteor_code': meteor_code,
            'pos_no': get_node_text(position_node, "imo:pos_no"),
        }
        # log.print_progress()
        self._import_file_entries(position_node, 'cam_pos_file', new_row)

    def _import_cam_system(self):
        """ add comment

        """
        # Create a new camera system code if the current one doesnt exist
        sql_select = "SELECT system_code FROM cam_system " \
                     "WHERE system_code='{system_code}'".format(**self._session)
        row = self._db_conn.execute_get_row(sql_select)
        if row is None:
            sql_insert = "INSERT INTO cam_system(system_code,contact_code,time_created) " \
                         "VALUES ('{system_code}', '{observer_code}', NOW())"\
                .format(**self._session)
            self._db_conn.execute(sql_insert)

    def _import_cam_software(self):
        """ add comment
        """
        # Create a new software code if the current one doesnt exist
        sql_select = "SELECT software_code FROM cam_software " \
                     "WHERE software_code = '{software_code}'".format(**self._session)
        row = self._db_conn.execute_get_row(sql_select)
        if row is None:
            sql_insert = "INSERT INTO cam_software" \
                         "(software_code, observer_code, time_created) " \
                         "VALUES ('{software_code}', '{observer_code}', NOW())"\
                .format(**self._session)
            self._db_conn.execute(sql_insert)

    def _import_location(self, session_node):
        """

        :param Node session_node:
        """
        # Allow to create a location code if none is given, but coordinates
        # are given instead
        if self._session['location_code'] is None:
            longitude = get_node_text(session_node, "vmo:location_lon")
            latitude = get_node_text(session_node, "vmo:location_lat")
            height = get_node_text(session_node, "vmo:location_height", "NULL")
            # Create new code
            if longitude and latitude:
                values_dict = {
                    'lat': latitude,
                    'lon': longitude,
                    'height': height,
                }
                values_dict.update(self._session)
                sql_select = "SELECT location_code FROM location " \
                             "WHERE lat = {lat} AND lon = {lon}".format(**values_dict)
                if height != "NULL":
                    sql_select += " AND height = {height};".format(**values_dict)

                row = self._db_conn.execute_get_row(sql_select)
                if row is None:
                    sql_count_template = "SELECT COUNT(*) FROM location " \
                                         "WHERE location_code='{location_code}'"
                    for i in range(1, 999999):
                        new_code = self._session['system_code']
                        if i > 1:
                            new_code += '-' + str(i)
                        sql_count = sql_count_template.format(location_code=new_code)
                        count = self._db_conn.execute_get_count(sql_count)
                        if count == 0:
                            values_dict['location_code'] = new_code
                            break
                    sql_insert = "INSERT INTO location" \
                                 "(location_code, name, country_code, lon, lat, height, " \
                                 "observer_code, comments, time_created) " \
                                 "VALUES ('{location_code}', '{system_code}', NULL, " \
                                 "{lon}, {lat}, {height}, '{observer_code}', " \
                                 "'Code automatically created while importing a camera " \
                                 "observation', NOW());".format(**values_dict)
                    log.debug("inserting: %s" % sql_insert)
                    self._db_conn.execute(sql_insert)
                    row = self._db_conn.execute_get_row(sql_select)

                if row is not None:
                    self._session['location_code'] = row['location_code']
                else:
                    log.error("could not locate newly inserted location_code for "
                              "(lat, lon, alt)=(%s, %s, %s)" % (latitude, longitude, height))

    def _call_import(self):
        """
        """

        def shared_add_entry(mysection, mycode, mystart, mystop, myreporter, mysource,
                             mystatus, mycomments, date_to_insert):
            """
            :param str mysection:
            :param str mycode:
            :param str mystart:
            :param str mystop:
            :param str myreporter:
            :param str mysource:
            :param str mystatus:
            :param str mycomments:
            :param str date_to_insert:
            :return: the new row
            :rtype: dict
            """
            myprefix = mysection + '-' + date_to_insert + '-' + mycode

            values_dict = {
                'myprefix': myprefix,
                'mysection': mysection,
                'mycode': myprefix,
                'mystart': mystart,
                'mystop': mystop,
                'mysource': mysource,
                'mystatus': mystatus,
                'mycomments': mycomments,
                'myreporter': myreporter,
                'mynumber': 1,
            }
            sql_select = "SELECT prefix_no FROM entry WHERE prefix='{myprefix}' " \
                         "ORDER BY prefix_no DESC;".format(**values_dict)
            row = self._db_conn.execute_get_row(sql_select)
            if row is not None:
                values_dict['mynumber'] = str(row['prefix_no'] + 1)
                values_dict['mycode'] = myprefix + '-' + values_dict['mynumber']

            sql_insert = "INSERT INTO entry(entry_code, prefix, prefix_no, section_code, " \
                         "start, stop, reporter_code, source_code, status_code, time_created) " \
                         "VALUES ('{mycode}', '{myprefix}', {mynumber}, '{mysection}', " \
                         "'{mystart}', '{mystop}', '{myreporter}', '{mysource}', '{mystatus}', " \
                         "NOW());".format(**values_dict)
            self._db_conn.execute(sql_insert)

            sql_insert = "INSERT INTO log_changes(id, timestamp, username, action, " \
                         "tablename, key1, comments) VALUES(0, NOW(), '{myreporter}', 'insert', " \
                         "'entry', '{mycode}', {mycomments});".format(**values_dict)

            if not FAST_IMPORT:
                self._db_conn.execute(sql_insert)

            sql_select = "SELECT * FROM entry WHERE entry_code='{mycode}'"\
                .format(**values_dict)
            row = self._db_conn.execute_get_row(sql_select)
            return row

        sessions = self._xml_conn.xpath("/imo:vmo/imo:cam_session", namespaces=NAMESPACE)
        for session_node in sessions:
            obs_code = get_node_text(session_node, "imo:observer_code")
            sys_code = get_node_text(session_node, "imo:system_code")
            start = get_node_text(session_node, "imo:period[1]/imo:start")
            stop = get_node_text(session_node, "imo:period[last()]/imo:stop")

            row = shared_add_entry('CAM', sys_code, start, stop, obs_code,
                                   'METRECDB', 'OK', 'NULL', self._date)

            entry_code = row["entry_code"]
            cam_session = {}
            fields = self._db_conn.get_column_names("cam_session")
            for field in fields:
                cam_session[field] = get_node_text(session_node, "imo:%s" % field)
            cam_session['version'] = time.strftime('%Y-%m-%dT%H:%M:%S')
            cam_session['entry_code'] = entry_code

            log.debug("processing session: %s" % str(cam_session))
            self._session = cam_session

            self._import_cam_system()
            self._import_cam_software()
            self._import_location(session_node)

            # Save all parameters of the cam_session table!!
            self._db_conn.execute_insert('cam_session', cam_session)

            if not FAST_IMPORT:
                if self._directory:
                    # Story the file reposity directory, if any
                    sql_update = "UPDATE entry SET directory = '%s' WHERE entry_code = '%s'" \
                                 % (self._directory, entry_code)
                    self._db_conn.execute(sql_update)

            # Link files to sessions
            new_row = {'entry_code': entry_code}
            self._import_file_entries(session_node, 'entry_file', new_row)

            # Run over the periods
            periods = session_node.xpath("imo:period", namespaces=NAMESPACE)
            for period_node in periods:
                self._import_cam_period(period_node, entry_code)


class ImportException(Exception):
    """ general module exception handler """

    def __init__(self, msg=''):
        super(ImportException, self).__init__(self, msg)
        log.exception(self)


class ShellCommandError(ImportException):
    """ This exception is raised when a shell command fails.
    The description will automatically be logged. """


class NoMatchError(Exception):
    """ minor exception indicating that no year/night/syscode match was
    found in the provide directory path. """


class LocationException(Exception):
    """ Major error related to missing latitude and longitude in the metrec
    log file.
    """


class Settings(object):
    """ Global configuration parameters. """

    # directory = r'E:\IMO Network Database\2011\20110101\bmh2'
    mml_output_dir = '/tmp/mr2'
    mml_output_file = mml_output_dir + '/vmo_data.xml'
    mml_feedback_file = mml_output_dir + '/vmo_feedback.txt'
    # mml_cmdline = 'java -jar "metrec2mml.jar" "{directory}" {system} {reporter} {output}'
    mml_reporter = 'ANON'
    mml_copy_to_dir = '/export/vmoftp'
    mml_data_root_url = '/CAM/METREC'

    db_conn = None
    commit = False
    sync_files = False
    auto_remove = False
    skip_existing = True
    summary_only = False

    @staticmethod
    def init_logger(log_file='/tmp/importer_out.txt', level=logging.INFO):
        """

        :param str log_file:
        :param int level:
        """
        global log
        if log is None:
            if isinstance(level, bool):
                level = [logging.INFO, logging.DEBUG][level]
            log = Logger(log_file, level)


class MMLDataSource(object):
    """ This class manages all the Metrec Meteor Language (MML)
    operations such as,

        * metrec2mml,
        * data validation,
        * database importation,
        * and data directory copy and removal.
    """

    def __init__(self, path='', year='', night='', sys_code=''):
        """
        :param str path:
        :param str year:
        :param str night:
        :param str sys_code:
        """
        self._xml_conn = None
        self._year = year
        self._night = night
        self._sys_code = sys_code
        self._source_dir = path
        self._entry_dir = '%s/%s/%s/%s' % (Settings.mml_data_root_url, year, night, sys_code)

    @property
    def xml(self):
        """
        :return:
        :rtype: Node
        """
        # if self._xml_conn is None:
        #     self.open_xml()
        return self._xml_conn

    @property
    def dbconn(self):
        """
        :return:
        :rtype: MySQLConn
        """
        return Settings.db_conn

    @property
    def night(self):
        """
        :return:
        :rtype: str
        """
        return self._night

    # def set_source_dir(self, year, night, sys_code):
    #     """
    #     :param str year:
    #     :param str night:
    #     :param str sys_code:
    #     """
    #     self._year = year
    #     self._night = night
    #     self._sys_code = sys_code
    #     self._entry_dir = '%s/%s/%s/%s' % (Settings.mml_data_root_url, year, night, sys_code)

    def get_source_dir(self):
        """
        :return: the night directory name
        :rtype: str
        """
        return self._source_dir

    def get_dest_url(self):
        """
        :return: the ftp destination directory location
        :rtype: str
        """
        return self._entry_dir

    def get_dest_dir(self):
        """
        :return: the ftp destination directory location
        :rtype: str
        """
        url_dir = self.get_dest_url()
        dest_dir = Settings.mml_copy_to_dir + url_dir
        return dest_dir

    # def open_xml(self):
    #     """
    #     :raises ImportException:
    #     """
    #     if not os.path.exists(Settings.mml_output_file):
    #         raise ImportException("Could not find vmo xml file: '%s'" % Settings.mml_output_file)
    #
    #     self._xml_conn = etree.parse(open(Settings.mml_output_file, 'r'))

    def metrec_to_mml(self, mml_save=False):
        # TODO: think about using convert.to_file_system_case
        log_path = os.path.join(self._source_dir, self._night + '.log')
        if not os.path.exists(log_path):
            log_path = log_path.replace('.log', '.LOG')
        if not os.path.exists(log_path):
            raise IOError('file does not exist: %s' % log_path)

        mml = MML(log_path, Settings.mml_reporter)
        xml_str = mml.get_xml_string()
        if mml_save:
            with open('mml.xml', 'w') as file_obj:
                file_obj.write(xml_str)
        self._xml_conn = etree.fromstring(xml_str.encode('utf-8'))

    # def metrec_to_mml_jar(self):
    #     """ Generates the vmo_data.xml file.
    #
    #     :raises ImportError:
    #     """
    #
    #     output_dir = os.path.dirname(Settings.mml_output_file)
    #
    #     if not os.path.exists(output_dir):
    #         os.makedirs(output_dir)
    #
    #     system_code = self._sys_code
    #
    #     cmdline = Settings.mml_cmdline.format(directory=self._source_dir,
    #                                           system=system_code,
    #                                           reporter=Settings.mml_reporter,
    #                                           output=Settings.mml_output_dir)
    #
    #     time_0 = time.time()
    #     log.info("metrec2mml process: %s", cmdline)
    #     proc = subprocess.Popen(args=cmdline,
    #                             shell=True,
    #                             stdin=subprocess.PIPE,
    #                             stdout=subprocess.PIPE,
    #                             stderr=subprocess.PIPE)
    #
    #     if proc.pid == 0:
    #         raise ImportError("Failed to start metrec2mml conversion")
    #
    #     line = proc.stderr.readline()
    #     while line:
    #         log.error("metrec2mml stderr: " + line.strip())
    #         line = proc.stderr.readline()
    #
    #     line = proc.stdout.readline()
    #     while line:
    #         if not line.startswith('PARSING OK'):
    #             log.info("metrec2mml stdout: " + line.strip())
    #         line = proc.stdout.readline()
    #
    #     log.info("Finished metrec2mml conversion in %0.2fsec", time.time()-time_0)
    #
    #     err_file_path = Settings.mml_feedback_file
    #     if os.path.exists(err_file_path):
    #         with open(err_file_path, 'rt') as file_obj:
    #             for line in file_obj.readlines():
    #                 msg = "metrec2mml (%s): %s " % (err_file_path, line.strip())
    #                 if "warning" in line.lower():
    #                     log.warning(msg)
    #                 else:
    #                     log.error(msg)
    #
    #     self.open_xml()

    def validate(self):
        """
        :return:
        :rtype: VMOXMLValidator
        """
        validator = VMOXMLValidator(self)
        validator.validate()
        return validator

    def mml_to_db(self, commit=True, remove_empty_position=False):
        """
        :param bool commit:
        :return:
        :rtype: VMOXMLImporter
        """
        importer = VMOXMLImporter(self, remove_empty_position)
        importer.import_into_db(commit)
        return importer

    def get_entry(self):
        """
        :return: shared_entry record
        :rtype: dict
        """
        sql_select = "SELECT * FROM entry WHERE entry_code = 'CAM-{night}-{sys_code}'"\
            .format(night=self._night, sys_code=self._sys_code)
        row = Settings.db_conn.execute_get_row(sql_select)
        return row

    def remove_entry(self, commit=True):
        """
        :param bool commit:
        """
        dest_dir = self.get_dest_url()
        try:
            # cursor.execute("BEGIN;")
            sql_delete = "DELETE FROM entry WHERE directory LIKE '%s%%'" % dest_dir
            entry_count = Settings.db_conn.execute_delete(sql_delete)

            sql_delete = "DELETE FROM files WHERE path LIKE '%s%%'" % dest_dir
            files_count = Settings.db_conn.execute_delete(sql_delete)

            log.info("Deleted %d entries and %d files from database."
                     % (entry_count, files_count))

            if commit:
                log.info("Commiting entry removal changes to database.")
                Settings.db_conn.commit()
            else:
                log.info("Rolling back database changes for entry removal.")
                Settings.db_conn.rollback()

        except Exception as exc:
            log.exception(exc)
            log.error("Caught exception rolling back database during entry removal.")
            Settings.db_conn.rollback()

    def remove_files(self, use_sudo=True):
        """
        :param bool use_sudo:
        """
        if "WIN" in platform.system().upper():
            dest_dir = self.get_dest_dir()
            if os.path.exists(dest_dir):
                shutil.rmtree(dest_dir)
            return

        dest_dir = self.get_dest_dir()
        call_shell_command("rm -rf %s" % (escape_shell_arg(dest_dir)), use_sudo)
        dest_parent_dir = os.path.dirname(dest_dir)
        if len(os.listdir(dest_parent_dir)) == 0:
            # removing empty night directory
            call_shell_command("rm -rf %s" % (escape_shell_arg(dest_parent_dir)), use_sudo)

    def copy_files(self, copy_entire_directory=True, use_sudo=True):
        """
        :param bool copy_entire_directory:
        :param bool use_sudo:
       """

        if "WIN" in platform.system().upper():
            dest_dir = self.get_dest_dir()
            src_dir = self.get_source_dir()
            # NOTE: parent directories are automatically created
            try:
                shutil.copytree(src_dir, dest_dir)
            except OSError as exc:
                log.error(str(exc))
            return

        dest_dir = self.get_dest_dir()
        src_dir = self.get_source_dir()
        new_dirs = []
        dir_path = dest_dir
        while True:
            if os.path.exists(dir_path):
                break
            new_dirs.append(dir_path)
            dir_path = os.path.dirname(dir_path)

        new_dirs.reverse()

        if copy_entire_directory:
            dest_parent_dir = os.path.dirname(dest_dir)
            if not os.path.exists(dest_parent_dir):
                call_shell_command("mkdir -p %s"
                                   % (escape_shell_arg(dest_parent_dir)),
                                   use_sudo)

            call_shell_command("cp -r %s %s"
                               % (escape_shell_arg(src_dir), escape_shell_arg(dest_dir)),
                               use_sudo)
        else:
            if not os.path.exists(dest_dir):
                call_shell_command("mkdir -p %s" % (escape_shell_arg(dest_dir)), use_sudo)

            file_count = 0
            files = self.xml.xpath("//imo:file/imo:path", namespaces=NAMESPACE)
            for path_node in files:
                src_file = os.path.join(src_dir, path_node.text)
                call_shell_command("cp %s %s"
                                   % (escape_shell_arg(src_file), escape_shell_arg(dest_dir)),
                                   use_sudo)
                file_count += 1
            log.info("Copied %d files to directory: '%s'" % (file_count, dest_dir))

        for dir_path in new_dirs:
            call_shell_command("chown -R www-data:www-data %s"
                               % (escape_shell_arg(dir_path)), use_sudo)
            call_shell_command("chmod -R 755 %s"
                               % (escape_shell_arg(dir_path)), use_sudo)


class DirectoryProcessor(object):
    """ Walk through a directory structure and process any
    VMO or MRG session data.
    """

    def __init__(self, directory, mml_save=False, remove_empty_position=False):
        """
        :param str directory: the directory to process.
        """
        Settings.db_conn.callback = log.print_progress
        self._iter = diriter.SystemSessionIterator(directory)
        self._mml_save = mml_save
        self._remove_empty_position = remove_empty_position

    def process_session(self, path, year, night, sys_code):
        """

        :param str path:
        :param str year:
        :param str night:
        :param str sys_code:
        """
        log.counters.reset_counters()
        log.notice("========== metrec2mml processing: night:%s, syscode:%s, path:'%s'"
                   % (night, sys_code, path))
        mml_data = MMLDataSource(path, year, night, sys_code)
        try:
            mml_data.metrec_to_mml(self._mml_save)
        except IOError as exc:
            log.exception(exc)
            return

        # try:
        #     summary = mml_data.validate().get_summary()
        # except LocationException:
        #     msg = "Metrec log file is missing locational information. " \
        #           "Cannot proceed with processing: %s" % path
        #     log.error(msg)
        #     return
        #
        # log.notice(summary)
        is_unique = mml_data.get_entry() is None

        if Settings.summary_only:
            return

        if Settings.auto_remove:
            if not is_unique:
                log.info("Removing duplicate entry.")
                mml_data.remove_entry(Settings.commit)
            if Settings.sync_files:
                mml_data.remove_files(True)

        mml_data.mml_to_db(Settings.commit, self._remove_empty_position)

        if Settings.sync_files:
            mml_data.copy_files()

    @staticmethod
    def print_summary(time_0, counters_tot, bad_nights, total_processed):
        """
        :param float time_0: start time
        :param dict counters_tot:
        :param int bad_nights:
        :param int total_processed:
        """
        msg = ""
        if counters_tot:
            for name in counters_tot:
                msg += " %d %s," % (counters_tot[name], name)

        time_str = time.strftime("%H:%M:%S", time.gmtime(time.time() - time_0))
        log.notice("==================================================")
        log.notice("SUMMARY (timed %s): %s" % (time_str, msg))
        log.notice("TOTAL DIRECTORIES PROCESSED: %d" % total_processed)
        log.notice("TOTAL DIRECTORIES FAILED: %d" % len(bad_nights))
        if len(bad_nights):
            log.notice("BAD DIRECTORY LISTING:")
            for path in bad_nights:
                log.notice("%s" % path)

    def process_directory_tree(self, continue_from_path=None):
        """
        :param str continue_from_path:
        """
        time_0 = time.time()
        counters_tot = Counters()
        counters_tot.init_counter('directories')
        bad_nights = []
        total_processed = 0

        log.debug("Processing: %s" % self._iter.template)
        entries = self._iter.sorted()
        # entries = list(self._iter)
        log.debug("Found %d directory matches." % len(entries))
        # entries = sorted(entries, key=lambda entry: entry[0])
        # log.debug("Sorting done.")

        skip_count = 0
        if Settings.skip_existing:
            log.notice("Finding duplicates...")
        for path, year, night, sys_code in entries:
            if Settings.skip_existing:
                mml_data = MMLDataSource(path, year, night, sys_code)
                if mml_data.get_entry() is not None:
                    log.info("Skipping existing entry: %s" % path)
                    skip_count += 1
                    continue

            if continue_from_path:
                if continue_from_path.lower() == path.lower():
                    log.notice("Continue from '%s'..." % path)
                    continue_from_path = None
                else:
                    continue

            if CONTINUE_PROCESSING:
                try:
                    self.process_session(path, year, night, sys_code)
                except Exception as ex:
                    import traceback
                    log.error(str(ex))
                    with open('errors.log', 'a') as err_file:
                        msg = 'Error: %s\n' % path
                        msg += 'Exception: %s\n' % str(ex)
                        msg += 'Traceback:\n%s\n' % traceback.format_exc()
                        err_file.write(msg)
            else:
                self.process_session(path, year, night, sys_code)

            total_processed += 1
            if log.counters.get_count('error'):
                bad_nights.append(path)

            counters_tot += log.counters
            counters_tot.increment_counter('directories')

        self.print_summary(time_0, counters_tot.get_counters(), bad_nights, total_processed)

    def remove(self):
        """ Remove and night entry and it's associates files
        """
        entries = list(self._iter)
        if len(entries) == 0:
            log.notice("No entries match the input directory. Quitting.")
            return

        log.notice("Removing %d entries" % len(entries))
        if len(entries) < 15:
            for entry in entries:
                print('\n  ', entry[0])
        answer = input("Continue (y/n)? ").strip()
        if answer == 'y':
            for path, year, night, sys_code in entries:
                mml_data = MMLDataSource(path, year, night, sys_code)
                mml_data.remove_entry(Settings.commit)
                if Settings.sync_files:
                    mml_data.remove_files(True)


class VMODatabaseManager(object):
    """ This class provides several commands to manage a VMO database. """

    def __init__(self,
                 db_name='vmo',
                 db_engine='mysql',
                 db_host='localhost',
                 db_port=0,
                 db_admin_user='root',
                 db_admin_password='',
                 db_user='',
                 db_password=''):
        self._db_name = db_name
        self._db_user = db_user
        self._db_password = db_password
        self._db_conn = DatabaseConnection(vault=None,
                                           db_name=db_name,
                                           db_engine=db_engine,
                                           db_host=db_host,
                                           db_port=db_port,
                                           db_usr=db_admin_user,
                                           db_pwd=db_admin_password)

    # def __init__(self, **kwargs):
    #     self._db_conn = DatabaseConnection(vault=None, **kwargs)
    #     self._db_name = self._db_conn.database

    def close(self):
        """ Close the database connection.
        """
        self._db_conn.close()

    def reporter(self, row=None):
        """ Create a new reporter user.
        :param dict row:
        """
        if row is None:
            row = {}
            print('Please enter the following required fields:')
            row['tex_first_name'] = unicode(input('First name: '))
            row['tex_last_name'] = unicode(input('Last name: '))
            row['email'] = input('Email: ')
            row['country_code'] = input('Country Code: ')
            first_name = unicodedata.normalize('NFKD', row['tex_first_name'])\
                .encode('ASCII', 'ignore').upper()
            last_name = unicodedata.normalize('NFKD', row['tex_last_name'])\
                .encode('ASCII', 'ignore').upper()
            row['observer_code'] = last_name[0:3] + first_name[0:2]

        self._db_conn.execute_insert('{}.observer'.format(self._db_name), row)
        self._db_conn.commit()
        print('Successfully inserted new reporter.')

    def create(self):
        """ Create a new VMO database.

        :raises DatabaseConnectionException: if the database already exists.
        """
        name = self._db_name
        conn = self._db_conn
        username = self._db_user
        password = self._db_password

        example = '\n  db_name = \'{db_name}\'' \
                  '\n  db_usr = \'{db_user}\'' \
                  '\n  db_pwd = \'{db_password}\''\
            .format(db_name=name, db_user=username, db_password=password)

        # awkward but necessary since the database does not yet exist.
        self._db_conn._con_kwargs['db'] = ''
        names = self.get_databases()
        if name in names:
            raise DatabaseConnectionException('{db_name} already exists.'.format(db_name=name))

        conn.execute("create database {db_name};"
                     .format(db_name=name))
        conn.execute("create user '{db_user}'@'localhost' identified by '{db_password}';"
                     .format(db_user=username, db_password=password))
        conn.execute("grant all privileges on {db_name}.* to '{db_name}'@'localhost';"
                     .format(db_name=name))
        log.notice('Created database "{db_name}" and user "{db_user}" with password '
                   '"{db_password}"'
                   .format(db_name=name, db_user=username, db_password=password))
        log.notice('NOTE: The following settings will need to be updated in '
                   'the VMO configuration file:%s', example)

    def get_databases(self):
        """ Get a list of all the database names.
        :return:
        :rtype: list
        """
        conn = self._db_conn
        rows = conn.execute('show databases;')
        databases = [row['Database'] for row in rows]

        return databases

    def get_table_counts(self, db_name):
        """ Get a dictionary of tables with row count values.

        :param str db_name:
        :return:
        :rtype: dict
        """
        return self._db_conn.get_table_counts(db_name)

    def import_schema(self):
        """ Import the default database schema configuration.

        :raises DatabaseConnectionException: if the database does not exist.
        """
        name = self._db_name
        conn = self._db_conn

        names = self.get_databases()
        if name not in names:
            raise DatabaseConnectionException('{db_name} does not exists.'.format(db_name=name))

        conn.execute("use {db_name};".format(db_name=name))
        sql_dir = os.path.join(VMO_DIR, 'database')
        conn.execute_file(os.path.join(sql_dir, 'vmo.sql'))
        conn.execute_file(os.path.join(sql_dir, 'vmo_shared_country.sql'))
        conn.execute_file(os.path.join(sql_dir, 'vmo_shared_entry_source.sql'))
        conn.execute_file(os.path.join(sql_dir, 'vmo_shared_entry_status.sql'))
        conn.execute("insert into {db_name}.observer "
                     "(observer_code, first_name, last_name) "
                     "values ('ANON', 'Anonymous', 'Observer');".format(db_name=name))
        conn.commit()
        # counts = conn.get_database_count(name)

    def drop(self):
        """ Delete a database.

        :raises DatabaseConnectionException: if the database does not exist.
        """
        name = self._db_name
        conn = self._db_conn
        username = name

        names = self.get_databases()
        if name not in names:
            raise DatabaseConnectionException('{db_name} does not exists.'.format(db_name=name))

        conn.execute("drop database {db_name};"
                     .format(db_name=name))
        conn.execute("revoke all privileges on {db_name}.* FROM '{db_user}'@'localhost';"
                     .format(db_name=name, db_user=username))
        conn.execute("drop user '{db_user}'@'localhost';"
                     .format(db_user=username))

    def clear(self):
        """ Clear all the records in the tables that are effected by an import.

        :raises DatabaseConnectionException: if the database does not exist.
        """
        name = self._db_name
        conn = self._db_conn

        names = self.get_databases()
        if name not in names:
            raise DatabaseConnectionException('{db_name} does not exists.'.format(db_name=name))

        tables = [
                  # 'cam_meteor',
                  # 'cam_period',
                  # 'cam_pos',
                  # 'cam_session',
                  # 'cam_software',
                  # 'cam_system',
                  'entry',
                  # 'files',
                  # 'meteor',
                  # 'period'
                  ]

        records = conn.execute('SELECT * FROM entry')
        print('Deleting %d entry entries...' % len(records))
        for record in records:
            entry_code = record['entry_code']
            count = conn.execute_delete("delete from entry where entry_code='{entry_code}';".format(entry_code=entry_code))
            conn.commit()
            print('Deleted entry: %s' % entry_code)

        count = conn.execute_delete("delete from cam_software")
        conn.commit()
        print('Deleted %d cam_software entries' % count)

        count = conn.execute_delete("delete from cam_system")
        conn.commit()
        print('Deleted %d cam_system entries' % count)

        count = conn.execute_delete("delete from files")
        conn.commit()
        print('Deleted %d files entries' % count)

        count = conn.execute_delete("delete from log_changes")
        conn.commit()
        print('Deleted %d log_changes entries' % count)

        count = conn.execute_delete("delete from location")
        conn.commit()
        print('Deleted %d location entries' % count)


def escape_shell_arg(arg):
    """ Escape any single quotes.
    :param str arg:
    :return:
    :rtype: str
    """
    return "\\'".join("'" + p + "'" for p in arg.split("'"))


def call_shell_command(cmd, sudo=False):
    """ Executes a command line instruction.
    :param str cmd:
    :param bool sudo:
    :raises ShellCommandError:
    """
    if sudo:
        cmd = "sudo " + cmd  # + " 2>&1"
    log.debug(cmd)
    output = subprocess.check_output(shlex.split(cmd))
    if output:
        log.error(cmd)
        raise ShellCommandError(cmd)


def get_node_text(context, xpath_expr, default_text=None):
    """ Extract the text from the first XML element.
    """
    try:
        node = context.xpath(xpath_expr, namespaces=NAMESPACE)
    except Exception as exc:
        log.exception(exc)

    if len(node):
        return node[0].text
    else:
        return default_text
