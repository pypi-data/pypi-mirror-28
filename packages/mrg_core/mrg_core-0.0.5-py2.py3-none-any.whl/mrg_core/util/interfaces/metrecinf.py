"""
   MetRec Inf File class module.
"""
from collections import OrderedDict
from datetime import datetime
from datetime import timedelta
import logging
from numbers import Number
import re

import numpy as np

from mrg_core.util.fileparser import FileParser


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
    >>> formatstr('%02d', 4)
        '04'
    >>> formatstr('%4.2f', 1.3)
        '1.30'
    >>> formatstr('%4.2f', 'a')
        '--.--'
    >>> formatstr('%3.1f', np.nan )
        '--.-'

    """
    if not isinstance(value, Number) or np.isnan(value):

        # Remove the presentation type specifier, i.e. 'f', 'd', or 'x'
        format_spec = format_string[:-1]
        length = format_spec.split('%')[1].split('.')

        if len(length) == 2:
            # string = '-' * (int(length[0]) - int(length[1][:-1]))
            # string += '.' + '-' * int(length[1][:-1])
            string = '-' * int(length[0])
        else:
            string = '-' * int(length[0][:-1])
    else:
        string = format_string % value

    return string


class MetRecInfFile(FileParser):
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

    Parameters
    ----------
    path: str
       The hhmmss.inf astrometry file path.
    camera: str
       Identifier of the camera used for recording the data corresponding
       to the MetRec INF File. If not provided, *UNK* will be assigned.
    clean: bool
       Flag indicating if the data read from the MetRec INF file should be
       cleaned when being accessed.

    Raises
    ------
    IOError
       if the INF path specified does not exist.

    Examples
    --------
    >>> # Retrieving all the raw data, by column, and demonstrating the usage
    >>> # of the clean flag.
    >>> inf_file = MetRecInfFile('/Data/ICC7/20160215/201809.inf', clean=False)
    >>> inf_file['bright']
    [None, None, None, 2.4, None, 4.4, 4.0, None, None, None]
    >>> inf_file['Unknown_column_name']
    [nan, nan, nan, nan, nan, nan, nan, nan, nan, nan]

    >>> # Retrieving only cleaned data, by column, and demonstrating the usage
    >>> # of the camera initialization parameter.
    >>> inf_file = MetRecInfFile('/Data/ICC7/20160215/201809.inf', camera='ICC7')
    >>> inf_file['bright']
    [2.4, 4.4, 4.0]
    >>> inf_file['Unknown_column_name']
    [nan, nan, nan]
    >>> inf_file.camera
    ICC7
    >>> inf_file.path
    /Data/ICC7/20160215/201809.inf

    """
    # Formatting of the data block
    # For '#', force two digits in all cases or wrong formatting when > 99
    # For 'bright', force 4.1 format in all cases or wrong format when 5.1
    _data2str = [
        ('#', ('%02d', 2)),
        ('time', ('%{:2.1f}f', 0.2)),
        ('bright', ('%4.1f', 4.1)),
        ('x', ('%{:2.1f}f', 4.3)),
        ('y', ('%{:2.1f}f', 4.3)),
        ('alpha', ('%{:2.1f}f', 0.3)),
        ('delta', ('%{:2.1f}f', 0.3)),
        ('c_x', ('%{:2.1f}f', 5.3)),
        ('c_y', ('%{:2.1f}f', 5.3)),
        ('c_alpha', ('%{:2.1f}f', 0)),
        ('c_delta', ('%{:2.1f}f', 0))
    ]

    def __init__(self, path=None, camera='UNK', clean=True):
        self._positions = []
        super(MetRecInfFile, self).__init__(path)

        if not self._positions:
            logging.warning('MetRecInfFile: No data available in %s', path)

        self._camera = camera
        self._clean = clean

    def __getitem__(self, item):
        """
        Returns the column ``item`` from the raw data, unless the internal
        flag ``_clean`` is set.  In the later case, only the data for rows
        with use == 'yes' will be returned.

        Parameters
        ----------
        item: str
           Column name, i.e. '#', 'time', 'bright', 'x, 'y', 'alpha', 'delta',
           'c_x', 'c_y', 'c_alpha', 'c_delta', 'use' or 'timestamp'.

        Returns
        -------
        list
           Column values for the column item.  If the flag clean was used in
           the initialization process, only the data for the rows with use
           equal to 'yes' will be returned.  If the requested item does not
           correspond to a valid column name, a list of np.nan of length equal
           to the number of data rows will be returned.

        """
        if self._clean:
            data = [row for row in self._positions if row['use']]
        else:
            data = self._positions
        value = [row.get(item, np.nan) for row in data]
        return value

    @property
    def camera(self):
        """Retrieve the identifier (str) of the camera used for recording the
        data corresponding to the MetRec INF File.
        """
        return self._camera

    @property
    def rawdata(self):
        """ Retrieve a list of OrderedDict with elements '#', 'time', 'bright',
        'x', 'y', 'alpha', 'delta', 'c_x', 'c_y', 'c_alpha', 'c_delta', 'use'
        and 'timestamp'.  If the flag clean was set to True in the class
        instantiation, only the original MetRec INF File rows with 'use' = yes
        are provided.
        """
        return self._positions

    def __str__(self):
        """Returns a str representation of the _header and the _positions in
        the original MetRec format.
        """
        inf = []
        idx = 0

        # Create the INF file header.
        for key, value in self._header.items():
            inf.append('{} {}'.format(key, value))
            idx += 1

        # Create the data-block section
        if self._lines:
            # Add the original header
            inf.append(self._lines[idx].rstrip())

            # Create the column format specifiers.
            column_formats, blanks = self._setup_format(idx+1)
            self._update_format(column_formats, blanks)

            # Create the data block
            for record in self._positions:
                frame = []
                for i, (key, value) in enumerate(record.items()):
                    if key == 'use':
                        if value:
                            frame.append('yes')
                        else:
                            frame.append('no')
                    elif key == 'timestamp':
                        pass
                    else:
                        # Replace the {} from the format string (item 0) with the
                        # required width.precision provided by the number in item
                        # 1.  Get the values' string representation.
                        fmt = column_formats[key][0].format(column_formats[key][1])
                        column = formatstr(fmt, value)

                        # Append to the end of the column the required number of
                        # blank characters to separate it from the next column.
                        frame.append('{}{}'.format(column, ' ' * blanks[i]))

                inf.append(''.join(frame))

        return '\n'.join(inf)

    def _setup_format(self, idx):
        """
        Returns an OrderedDict that contains for each of the data-block columns
        a tuple that corresponds to the replacement field of the format string
        to be used in the formatting of the different values in each of the
        columns (item 0) and the width[.precision] of the format specification
        of that replacement field, e.g.::

           column_formats['time'] = ('%{:2.1f}f', 4.2)

        which indicates that the time column's values shall be formatted as a
        floating point number with a width of 4 and a precision of 2 digits.

        It also returns a list of integer numbers indicating the number of
        blank characters that should be left between two adjacent columns.
        The value in position 0 corresponds to the blanks between column 0
        and 1 ('#" and 'time'), the value in position 1, the blanks between
        column 1 and 2, and so forth.

        This function takes as default values for the format specification
        those defined in the private constant _data2str and modifies them
        in order to provide the maximum width and precision found in the
        original MetRec INF file, per column.  For the number of blanks, it
        takes as default the maximum acceptable number of blanks between
        columns (currently set to 10 spaces), reducing that value to the
        length of the minimum gap found between two given adjacent columns.

        Parameters
        ----------
        idx: int
           Line number of the first row of the data-block section of the
           original MetRec INF file, i.e. line number of the data row that
           provides the meteor information for the frame number 01.

        Returns
        -------
        tuple
           column_formats: OrderedDict that contains for each of the data-block
                           columns a tuple that corresponds to the replacement
                           field of the format string to be used in the
                           formatting of the different values in each of the
                           columns (item 0) and the width[.precision] of the
                           format specification of that replacement field

            blanks:        List of int indicating the number of blank
                           characters that should be left between two adjacent
                           columns.

        Notes
        -----
        Some MetRec INF files are 'badly' formatted due to an existing bug.
        This issue can be found in the 'x', 'y' and/or 'c_y' columns of some
        of these files, where negative numbers are provided.  This case is
        handled as an exception within this routine, in order to keep in the
        output the same 'bad' format.

        """
        # Setup default formatting for the data block.  It might get changed
        # during the generation of the final format.
        column_formats = OrderedDict(self._data2str)
        blanks = [10] * len(column_formats)

        for line in self._lines[idx:]:
            # Remove the EOL character from the current line.
            line = line.rstrip()

            # Get the data items.
            data = line.split()

            # Get all the column separator white-spaces and check if we need
            # to reduce the minimum space between adjacent columns.
            whites = re.findall(r'\s+', line)
            blanks = [min(blanks[i], len(num)) for i, num in enumerate(whites)]

            for i, column in enumerate(column_formats):
                elem = data[i]

                # Remove negative number that appear in some cases where they
                # should not, e.g.
                # ICC7/20110921/002519.inf, column 'y'
                # ICC7/20121007/043504.inf, column 'x'
                # ICC9/20160306/041030.inf, column 'c_y'
                if column in ['y', 'x', 'c_y'] and re.match(r'-\d', elem):
                    elem = elem.replace('-', '')
                    logging.info('MetRecInfFile: Bad formatted column "%s" '
                                 'in MetRec INF file %s', column, self._path)

                length = len(elem)

                if '.' in elem:
                    # In some cases, there are columns that mix dashes with floats
                    # Take the maximum integer value of the current string length
                    # and the stored one.  This will give you the maximum allowed
                    # width for this column.
                    length = max(length, int(column_formats[column][1]))

                    # For float the format length is also a float, with the
                    # decimal part being the resolution.
                    length += len(elem.split('.')[1]) / 10.0

                # Check if we need to update the string representation format.
                if length > column_formats[column][1]:
                    column_formats[column] = (column_formats[column][0], length)

        return column_formats, blanks

    def _update_format(self, formats, blanks):
        """
        Updates, in-place, the format specifiers for all columns and blanks
        between adjacent columns, if such update is necessary.

        Updates are only necessary when the length of the integral part of a
        the maximum value of a given column exceeds the specified value of the
        input format string for that column.

        Parameters
        ----------
        formats: OrderedDict
           For each of the data-block columns a tuple that corresponds
           to the replacement field of the format string to be used in the
           formatting of the different values in each of the columns (item 0)
           and the width[.precision] of the format specification of that
           replacement field.
        blanks: list
           Integer number of blank characters that should be left between two
           adjacent columns.

        Notes
        -----
        The updates only will take effect if the given column is supposed to
        have a 'dynamic' formatting, i.e. if the formats[key][0] does not
        contain {} then the updates for tha key column will not be visible.
        An example of this situation is for the '#' or 'bright' columns in
        the current version.

        """
        # Set the value of the 'clean' flag to False to retrieve all data
        # points from a given column and save the original value to restore it
        # at the end of the searches.
        clean = self._clean
        self._clean = False

        for i, key in enumerate(formats):
            # Find the maximum value in the _positions data for the 'key'
            # column.  First remove None values.  If all None, no update is
            # require, continue to the next column.
            try:
                value = max([item for item in self.__getitem__(key) if item])
            except ValueError:
                continue

            fmt = formats[key][0].format(formats[key][1])

            # Compute the length of the string representation of the maximum
            # value, if the current format is used.
            length = len(formatstr(fmt, value))

            # Update the blanks if there are more than 1, and the format to
            # be used, if the length of the maximum value of the 'key' column
            # is bigger than the current format.  Keep the [.precision] values
            # as originally defined.
            if length > formats[key][1]:
                if blanks[i-1] > 1:
                    blanks[i-1] -= length - int(formats[key][1])

                formats[key] = (formats[key][0], length + formats[key][1] % 1)

        # Restore the original value of the 'clean' flag.
        self._clean = clean

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
        """ Parse the entire MetRec INF file content.  This method is used
        automatically when the class instance is initialized and does not need
        to be called a second time."""
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
                        logging.warning('In INF file header section: %s, '
                                        'line: %s', self.path, line)
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
                    row = self._parse_position_line(head, line)
                except ValueError:
                    logging.error('ERROR: in INF file positions section: %s, '
                                  'line: %s', self.path, line)
                    raise
                self._positions.append(row)

    def save(self, path=None):
        """
        Saves the contents of the _header and _positions private class
        attributes to the requested ``path``.

        If ``path`` is not provided, the value provided in the instantiation
        of the class will be used.

        Parameters
        ----------
        path: str
           The hhmmss.inf astrometry file path to which the contents of the
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
            message = "MetRecInfFile: No path provided to save the class' data"
            logging.error(message)
            raise IOError(message)
