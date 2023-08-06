"""
DAF file interface
"""
from collections import OrderedDict
import logging
from numbers import Number

import numpy as np
import pandas as pd

from mrg_core.util.fileparser import FileParser


DATA_COLUMNS = ['station', 'frame', 'time', 'bright', 'x_pxl', 'y_pxl',
                'alt', 'e_alt', 'e_pos', 'lon', 'lat', 'dist', 'e_dist',
                'vel', 'e_vel']
DATA_FORMATS = ['%1d', '%03d', '%4.2f', '%5.1f', '%4.3f', '%4.3f',
                '%7.1f', '%5.1f', '%5.1f', '%8.3f', '%7.3f', '%9.1f', '%5.1f',
                '%5.3f', '%5.3f']
DATA2STR = dict(zip(DATA_COLUMNS, DATA_FORMATS))


def formatstr(format_string, value):
    """
    Returns a string representation of the input value number if it possible
    and otherwise a string with dashes instead of digits.

    Parameters
    ----------
    format_string: str
       Format string, as if it would be used for the standard function .format
    value: object
       Object for which the string representation is requested. Ideally, this
       value should be a number.

    Returns
    -------
    str
       String representation, following the required format, of the input value.
       If the input value cannot be converted to the requested format, the
       output string will be a sequence of dashes following the required format
       picture.

    Examples
    --------
    >>> formatstr('%4.2f', 1.3)
        1.30
    >>> formatstr('%4.2f', 'a')
        --.--
    >>> formatstr('%3.1f', np.nan )
        --.-

    """
    if not isinstance(value, Number) or np.isnan(value):
        length = format_string.split('%')[1].split('.')
        string = '-' * (int(length[0]) - int(length[1][:-1]))
        string += '.' + '-' * int(length[1][:-1])
    else:
        string = format_string % value

    return string


class DafFile(FileParser):
    """
    Detailed Altitude File interface

    """

    def __init__(self, path=''):
        self._headers = pd.DataFrame(
            columns=['Station', 'LogFile:', 'StationDirectory:',
                     'AppearanceDate:', 'AppearanceTime:',
                     'INFFilename:', 'FrameCount:', 'Shower:', 'Accuracy:'])
        self._data = pd.DataFrame(columns=DATA_COLUMNS)
        super(DafFile, self).__init__(path)

    @property
    def headers(self):
        """
        The headers of the Detailed Altitude File.

        :type: pandas.DataFrame
        """
        return self._headers

    @headers.setter
    def headers(self, value):
        index = len(self._headers.index)
        self._headers.loc[index] = [index + 1] + value

    @property
    def data(self):
        """
        The data of the Detailed Altitude File.

        :type: pandas.DataFrame
        """
        return self._data

    @data.setter
    def data(self, value):
        value.columns = DATA_COLUMNS[1:]
        value['station'] = pd.Series(len(self._headers.index),
                                     index=value.index)
        self._data = self._data.append(value, ignore_index=True)

    def _str_header(self, idx):
        """
        Returns a string representation of the DAF data header block
        corresponding to the station ``idx``.
        :param idx:  index for the data block. Note that station indexes start
                    at 1, while panda's DataFrame indexes start at 0.
        :type idx: int

        :return: string representation of the data block corresponding to the
                 station ``idx``
        :rtype: str

        """
        header = ''
        for name in self._headers.columns.values:
            header += name + ' ' + str(self._headers[name][idx]) + '\n'

        return header

    def _str_data(self, idx):
        """
        Returns a string representation of the data block corresponding to the
        station ``idx``.

        :param idx: index for the data block. Note that station indexes start
                    at 1, while panda's DataFrame indexes start at 0.
        :type idx: int

        :return: string representation of the data block corresponding to the
                 station ``idx``
        :rtype: str
        """
        data = ('!                     Position         Altitude in m     '
                '       SubPoint        Cam. dist in m  Velocity in km/s\n'
                '!###   Time  Bright   x      y       h       +/-h  +/-pos'
                '   lon/deg  lat/deg     dist   +/-dist    v      +/-v\n')
        data_block = self._data[self._data['station'] == idx + 1]
        for i in range(0, len(data_block)):
            for name in DATA_COLUMNS[1:]:
                data += ' ' + formatstr(DATA2STR[name], self._data[name][i]) + ' '
            data += '\n'

        return data

    def __str__(self):
        """Returns the string representation of the DAF File object."""
        daf = ''
        for station in self._headers.index:
            daf += self._str_header(station) + '\n'
            daf += self._str_data(station) + '\n'

        return daf[:-1]

    @staticmethod
    def _parse_position_line(station, line):
        """
        :param int station: station ID, either 0 or 1.
        :param str line: the meteor position line.
        :return:
        :rtype: OrderedDict
        """
        # line = line.replace('yes', 'True').replace('no', 'False').lstrip('0')
        data = line.split()
        values = [int(station)]
        for elem in data:
            if '--' in elem:
                values += [None]
            elif '.' in elem:
                values += [float(elem)]
            else:
                values += [int(elem)]

        row = OrderedDict(list(zip(DATA_COLUMNS, values)))
        return row

    def parse(self):
        """Parse the entire Detailed Altitude File content."""
        in_header = True
        head = {}
        iterator = self._lines.__iter__()
        for line in iterator:
            line = line.strip()
            if in_header:
                if line.startswith('!'):
                    in_header = False
                    self._headers = self._headers.append(head, ignore_index=True)
                elif not line.split():
                    continue
                else:
                    try:
                        key, value = [part.strip() for part in line.split(' ', 1)]
                        head[key] = value
                    except ValueError:
                        logging.error('In DAF file header section: %s, '
                                      'line: %s', self.path, line)
            else:
                if not line.split():
                    in_header = True
                elif line.startswith('!'):
                    continue
                else:
                    try:
                        row = self._parse_position_line(head['Station'], line)
                    except ValueError:
                        logging.error('In DAF file positions section: %s, '
                                      'line: %s', self.path, line)
                        raise
                    self._data = self._data.append(row, ignore_index=True)

    def save(self, path):
        """
        Saves to the file provided in the input ``path`` the complete
        contents of the Detailed Altitude File object, and its header(s).

        Parameters
        ----------
        path: str
           Full path for the output DAF file to be created.

        """

        with open(path, 'wt') as daf:
            daf.write(self.__str__())
