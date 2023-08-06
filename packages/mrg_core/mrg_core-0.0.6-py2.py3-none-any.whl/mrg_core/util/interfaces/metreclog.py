"""
   MetRec Log File class module.
"""
from __future__ import print_function
from collections import OrderedDict
from datetime import datetime
from datetime import timedelta
import logging
import re

from pandas import DataFrame

from mrg_core.util.fileparser import FileParser


# The following regular expresion helps to extract all numbers from an input
# string by using RE_NUMBER.findall(string).
RE_NUMBER = re.compile(r'-?\d*\.?\d+')

# The following regular expression helps to extract the observation time from
# an input string by using RE_OBS_TIME.findall(string).
RE_OBS_TIME = re.compile(r'^(\d{2}):(\d{2}):(\d{2}).*')

# The following regular expression helps to extract the shower ID, i.e. three
# consecutive uppercase letters, from an input string by using
# RE_SHOWER.findall(string).
RE_SHOWER = re.compile(r'[A-Z]{3}')


class MetRecLogFile(FileParser):
    """ Parse a MetRec log file.

    The contents of the class can be printed to stdout or save on a file.
    When this operation is performed, the magic method __str__
    reprocesses the rawdata in order to print out any updated information,
    and so does it for the different keywords in the different headers
    of the MetRec Log file. For any other MetRec Log file original line,
    the output matches the original line, with the exception of any trailing
    blank characters, which are removed.

    Parameters
    ----------
    path: str
       The yyyymmdd.log MetRec Log file path.
    camera: str
       Identifier of the camera for which the MetRec Log file has been
       created. If not provided, *UNK* will be assigned.

    Raises
    ------
    IOError
       if the MetRec Log file path specified does not exist.

    """

    _meteor = OrderedDict([
        ('time', '%s'),
        ('#', '%d'),
        ('xbeg', '%4.3f'),
        ('ybeg', '%4.3f'),
        ('xend', '%4.3f'),
        ('yend', '%4.3f'),
        ('frames', '%d'),
        ('dur', '%3.2f'),
        ('pixel', '%d'),
        ('dir', '%d'),
        ('vel', '%3.1f'),
        ('snr', '%2.1f'),
        ('shower', '%s'),
        ('bright', '%2.1f'),
        ('raddist', '%2.1f'),
        ('exp vel', '%3.1f'),
        ('RAbeg', '%5.3f'),
        ('Decbeg', '%4.2f'),
        ('RAend', '%5.3f'),
        ('Decend', '%4.2f'),
        ('acc', '%2.1')
    ])

    def __init__(self, path, camera='UNK'):
        self._metrec_cfg = OrderedDict()
        self._rawdata = []
        self._stats = OrderedDict()
        super(MetRecLogFile, self).__init__(path)
        self._camera = camera

    @property
    def camera(self):
        """Property: Identifier of the camera for which the MetRec Ref Stars
        File has been computed.
        """
        return self._camera

    @property
    def meteors(self):
        """ Property: Pandas' DataFrame containing all records of meteor
        detection events and associated characteristics.  Meteor detection
        events flagged as 'Skipped' are not provided.
        """
        data = [record for record in self._rawdata
                if record['IsData'] and not record['Skipped']]

        return DataFrame(data)

    @property
    def rawdata(self):
        """Property: List of OrderedDict that contain all time-tagged records
        in the MetRec Log File.  The dictionary keyword 'IsData', when True,
        indicates that the record is a meteor detection event.
        """
        return self._rawdata

    def _str_meteor_line(self, row):
        """
        Returns a string representation of the meteor ``row`` passed as input
        in the standard format of the MetRec Log files.

        Parameters
        ----------
        row: OrderedDict
           Complete meteor detection event data.

        Returns
        -------
        str
           String representation of the meteor detection event data.

        """
        values = [value for key, value in row.items() if key in self._meteor]

        # Create the common string representation for all meteor detection
        # events
        met = ('{} Meteor #{} at ({:.3f},{:.3f})->({:.3f},{:.3f}) '
               'frames={} dur={:.2f}s pixel={} dir={:3d}$ vel={}$/s snr={}\n'
               '         shower={} bright={}mag ').format(*values[:14])

        # Add raddist and exp vel data if the meteor belongs to a shower.
        if not row['shower'] == 'SPO':
            met += 'raddist={}$ exp vel={}$/s '.format(*values[14:16])

        # Add the remaining of the common string representation.
        met += ("({:.3f}h,{:.2f}$) -> ({:.3f}h,{:.2f}$) "
                "acc={}'").format(*values[16:])

        return met

    def __str__(self):
        """Returns a str representation of the _header, _metrec_cfg, _meteors
        and _stats in the original MetRec format."""

        logfile = []

        # Keep track of the line number so that we can print any other messages
        # after the time-tagged events.
        idx = 0

        # Log file header section
        for key, value in self._header.items():
            logfile.append('{:<8}: {}'.format(key, value))
            idx += 1

        # MetRec Configuration section
        # Put back all the textual messages printed by MetRec in the log file.
        for line in self._lines[idx:]:
            hhmmss = RE_OBS_TIME.findall(line)

            # MetRec Configuration section ends when meteor recognition starts
            if len(hhmmss):
                break

            idx += 1
            parts = line.split(': ', 1)
            key = parts[0].rstrip('.')
            if key in self._metrec_cfg:
                value = self._metrec_cfg[key]
                value = value.replace(u'\xf8', '$')
                # value = value.encode('utf-8')
                logfile.append('{}: {}'.format(parts[0], value))
            else:
                logfile.append(line.rstrip())

        # Output the meteor detection events and any other time-tagged data.
        # If there's any textual messages printed by MetRec in the log file
        # in-between or after the meteor detection events, add them at the
        # right place.
        time_tagged_data = self._rawdata.__iter__()
        while idx < len(self._lines):
            line = self._lines[idx]
            idx += 1

            hhmmss = RE_OBS_TIME.findall(line)

            # Output any line that has no time information as is in the
            # original MetRec Log file.
            if not len(hhmmss):
                logfile.append(line.rstrip())

                # Next section starts with the following literal line.
                if line.startswith('======='):
                    break
                else:
                    continue

            # Print the time-tagged data until all the data has been consumed
            try:
                row = next(time_tagged_data)
            except StopIteration:
                continue

            if row['IsData']:
                # Meteor detection events have always 2 information lines.
                logfile.append(self._str_meteor_line(row))
                idx += 1
            else:
                logfile.append('{} {}'.format(row['time'], row['message']))

        #
        # Observing statistics
        in_numbers = False
        for key, value in self._stats.items():
            idx += 1

            # Add a blank line if we are in a subsection of statistics
            if ((key.startswith('#') and not in_numbers) or
                    (not key.startswith('#') and in_numbers)):
                logfile.append('')
                idx += 1
                in_numbers = not in_numbers

            logfile.append('{:<25}: {}'.format(key, value))

        #
        # Add any additional lines that may exist after the end of the
        # observing statistics
        logfile.extend([line.rstrip() for line in self._lines[idx:]])

        log_str = '\n'.join(logfile)
        log_str = log_str.replace('$', u'\xf8')

        return log_str

    def _parse_meteor_line(self, line):
        """
        :param str line: the complete meteor event specification line.
        :return:
        :rtype: OrderedDict
        """
        result = OrderedDict()

        logging.debug('Parsing meteor line: %s', line)
        parts = line.split(' ', 1)

        # Get the time string, all numeric values and the shower ID.
        time = parts[0]
        numbers = RE_NUMBER.findall(parts[1])
        shower = RE_SHOWER.findall(parts[1])[0]

        # Get the shower ID at the right place.
        values = [time] + numbers[0:11] + [shower] + numbers[11:]

        # SPO showers have no data for 'raddist' and 'exp vel'
        if shower == 'SPO':
            values[14:14] = [None, None]

        for i, key in enumerate(self._meteor):

            if not values[i]:
                result[key] = values[i]

            elif '.' in values[i]:
                result[key] = float(values[i])
            else:
                try:
                    result[key] = int(values[i])
                except ValueError:
                    result[key] = values[i]

        return result

    def _set_timestamp(self, row):
        """ From the LOG header and meteors row construct a datetime data type
        timestamp. The 'timestamp' key will be added to the meteors row
        argument.

        Parameters
        ----------
        row: OrderedDict
           the position record.
        """
        sttime_str = self._header['Date'] + ' ' + self._header['Time']
        begin_time = datetime.strptime(sttime_str, '%Y/%m/%d %H:%M:%S')
        timestamp_str = self._header['Date'] + ' ' + row['time']
        timestamp = datetime.strptime(timestamp_str, '%Y/%m/%d %H:%M:%S')
        if timestamp < begin_time:
            timestamp += timedelta(days=1.0)

        row['timestamp'] = timestamp

    def parse(self):
        """Parse the entire MetRec log file content.
        """
        # MetRec log file is split in several sections.
        section2header = {
            0: self._header,
            1: self._metrec_cfg,
            3: self._stats
        }

        # Keep track of the section the current line is in.
        section = 0
        iterator = self._lines.__iter__()
        for i, line in enumerate(iterator):
            line = line.strip()
            line = line.replace(u'\xf8', '$')
            line = line.replace(u'\xe5', 'snr')

            hhmmss = RE_OBS_TIME.findall(line)

            # Parse meteor recognition section
            if ' Meteor #' in line and len(hhmmss):

                # the 2nd line contains more meteor analysis
                line = line.strip()
                line += next(iterator)
                # the 3rd line contains state info
                state_line = self._lines[i+2]
                if 'Comment:' in state_line:
                    state_line = self._lines[i+3]

                if 'Restart recognition' in line:
                    # However, on occasion a recognition restart occurs
                    # and the line format becomes (20150410/pav36):
                    #     19:42:37 Restart recognition19:58:43 Meteor #1 at ...
                    #
                    #      snr=3.5
                    #              shower=SPO bright=0.8mag ....
                    #     20:38:12 Meteor #6 at ....
                    # discard the restart part and collect the next few
                    # lines.
                    logging.warning('mixed meteor and restart '
                                    'recognition line.')
                    line = line.split('Restart recognition')[1]
                    if 'shower' not in line:
                        line += next(iterator)

                try:
                    meteor_dict = self._parse_meteor_line(line)
                except SyntaxError as exc:
                    logging.error('error parsing meteor line: %s', line)
                    logging.exception(exc)
                    raise

                meteor_dict['Skipped'] = 'Skip saving meteor #' in state_line
                self._set_timestamp(meteor_dict)
                meteor_dict['IsData'] = True
                self._rawdata.append(meteor_dict)

            # Keep all other records as information. Set IsData to False for
            # fast filtering.
            elif len(hhmmss):
                info = OrderedDict()
                parts = line.split(' ', 1)

                info['time'] = parts[0]
                self._set_timestamp(info)
                info['message'] = parts[1]
                info['IsData'] = False

                self._rawdata.append(info)
                section = 2

            elif line.startswith('===='):
                section += 1
                # line = next(iterator).strip()

            # Parse headers and config sections
            elif section != 2:
                try:
                    # some keywords have no assigned value, e.g. 20160104.log
                    # start of observation       :
                    if line.endswith(':'):
                        key = line[:-1].rstrip('.').strip()
                        value = ''
                    else:
                        key, value = [part.rstrip('.').strip()
                                      for part in line.split(': ', 1)
                                      if not line.startswith('WARNING')]

                    # Depending on the section number, assign the key, value
                    # to the appropriate OrderedDict
                    section2header[section][key] = value
                except ValueError:
                    continue

    def save(self, path=None):
        """
        Saves the contents of the _header, _metrec_cfg, _meteors and _stats
        private class attributes to the requested ``path``.

        If ``path`` is not provided, the value provided in the instantiation
        of the class will be used.

        Parameters
        ----------
        path: str
           The hhmmss.log MetRec Log file path to which the contents of the
           class shall be saved in the standard MetRec format.

        Raises
        ------
        IOError
           If neither the ``path`` method argument is provided nor the ``path``
           private class attribute is set.

        """
        if not path:
            path = self._path

        try:
            with open(path, 'wt') as fhandle:
                fhandle.write('{}\n'.format(self.__str__()))
        except IOError:
            message = "MetRecLogFile: No path provided to save the class' data"
            logging.error(message)
            raise IOError(message)
