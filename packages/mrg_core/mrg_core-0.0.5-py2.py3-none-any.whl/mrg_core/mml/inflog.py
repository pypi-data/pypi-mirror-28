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
This module implements the METREC INF astrometry file parser.
"""
from __future__ import print_function

from datetime import datetime
from datetime import timedelta
from collections import OrderedDict

from mrg_core.util.fileparser import FileParser


class InfFile(FileParser):
    """ Parse a METREC `*`.inf astrometry file. A typical file is provided
    here::

        AppearanceDate 15.02.2016
        AppearanceTime 20:18:09
        ReferenceStars c:\\cilbo\\metrec\\config\\20150214.ref
        FrameCount 10
        #   time  bright   x      y      alpha     delta   c_x    c_y    c_alpha  c_delta  use
        01   9.211 ----  0.715  0.489    1.9854   40.920  -----  -----  --------  -------  no
        02   9.251 ----  0.690  0.453    1.9287   39.963  -----  -----  --------  -------  no
        03   9.291 ----  0.664  0.416    1.8740   39.002  -----  -----  --------  -------  no
        04   9.331  2.4  0.639  0.380    1.8213   38.037  -----  -----    1.8225   37.958  yes
        05   9.371 ----  0.613  0.344    1.7695   37.066  -----  -----  --------  -------  no
        06   9.411  4.4  0.587  0.307    1.7188   36.092  -----  -----    1.7238   36.257  yes
        07   9.451  4.0  0.574  0.280    1.6787   35.515  -----  -----    1.6761   35.400  yes
        08   9.491 ----  0.560  0.253    1.6387   34.935  -----  -----  --------  -------  no
        09   9.531 ----  0.546  0.227    1.5996   34.353  -----  -----  --------  -------  no
        10   9.571 ----  0.532  0.200    1.5605   33.769  -----  -----  --------  -------  no
    """

    def __init__(self, path=None):
        """
        :param str path: the hhmmss.inf astrometry file path.
        :raises IOError: if the INF path specified does not exist.
        """
        self._positions = []
        super(InfFile, self).__init__(path)

    @property
    def positions(self):
        """
        :return: the list of ordered dictionary meteor detection positions.
        :rtype: list
        """
        return self._positions

    @property
    def fov_position(self):
        """ Retrieve the field-of-view start and end positions.
        :return: 2D tuple of floats in the form: ((x0, y0), (x1, y1))
        :rtype: tuple
        """
        pos = self.bright_positions
        if len(pos) >= 2:
            return (pos[+0]['x'], pos[+0]['y']), (pos[-1]['x'], pos[-1]['y'])

    @property
    def bright_positions(self):
        """ Retrieve the list of position that are valid position, meaning,
        the *bright* column value is a valid number, and the *use* column
        is True (yes).

        :return: the list od :class:`OrderedDict` of valid positions to
            be exported.
        :rtype: list
        """
        bright_list = []
        for position in self.positions:
            if position['bright'] is not None:
                bright_list.append(position)
        return bright_list

    def _set_timestamp(self, row):
        """ From the INF header and position row construct a timestamp with
        milli-second precision. The 'timestamp' key will be added to the position
        row argument.

        :param OrderedDict row: the position record.
        """
        timestamp_str = self._header['AppearanceDate'] + ' ' + self._header['AppearanceTime']
        timestamp = datetime.strptime(timestamp_str, '%d.%m.%Y %H:%M:%S').replace(second=0)
        timestamp += timedelta(seconds=row['time'])
        if len(self._positions) and row['time'] < self._positions[0]['time']:
            timestamp += timedelta(seconds=60.0)

        row['timestamp'] = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]

    def _parse_position_line(self, headings, line):
        """
        :param list headings: the meteor position line headings.
        :param str line: the meteor position line.
        :return:
        :rtype: OrderedDict
        """
        # line = line.replace('yes', 'True').replace('no', 'False').lstrip('0')
        data = line.split()
        values = []
        for elem in data:
            if '--' in elem:
                values.append(None)
            elif 'yes' in elem:
                values.append(True)
            elif 'no' in elem:
                values.append(False)
            elif '.' in elem:
                values.append(float(elem))
            else:
                values.append(int(elem))

        row = OrderedDict(list(zip(headings, values)))
        self._set_timestamp(row)
        return row

    def parse(self):
        """ Parse the entire INF astrometry file content."""
        in_header = True
        head = []
        iterator = self._lines.__iter__()
        for line in iterator:
            line = line.strip()
            if in_header:
                if line.startswith('#'):
                    in_header = False
                    head = line.split()
                else:
                    try:
                        key, value = [part.strip() for part in line.split(' ', 1)]
                        self._header[key] = value
                    except ValueError:
                        print('ERROR: in INF file header section: %s, line: %s' % (self.path, line))
            else:
                try:
                    # special handling of badly formatted old INF files
                    if ',' in line:
                        # in 'bright' column
                        # ref: 2005/20050107/KAYAK1/041950.INF
                        #      2005/20051117/KAYAK1/225402.INF
                        line = line.replace(',', '.')
                    if '"' in line:
                        # ref: 2011/20110815/orion1/005006.inf
                        line = line.replace('"', ' ')
                    if '/' in line:
                        # ref: 2011/20110815/orion1/005006.inf
                        line = line.replace('/', '-')
                    if '$' in line:
                        # ref: 2011/20110815/orion1/005006.inf
                        line = line.replace('$', ' ')
                    if '-+' in line:
                        # ref: 2014/20140506/sraka/*.inf
                        line = line.replace('-+', '  ')
                    row = self._parse_position_line(head, line)
                except ValueError:
                    print('ERROR: in INF file positions section: %s, line: %s' % (self.path, line))
                    raise
                self._positions.append(row)
