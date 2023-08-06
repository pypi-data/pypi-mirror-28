"""
   MetRec Ref Stars File class module.
"""
from collections import OrderedDict
import logging

import numpy as np

from mrg_core.util.fileparser import FileParser


class RefStarsFile(FileParser):
    """ Parse a METREC reference `*`.ref file. A typical file is provided
    here::

        SiteCode 14260
        Longitude 10.858890
        Latitude 45.697498
        Altitude 1208
        OperationMode unguided
        ReferenceDate 2010 3 19
        ReferenceTime 22 35 0
        VideoBrightness 255
        VideoContrast 255
        CenterOfPlate  192  144
        OrderOfPlateConstants 3
        NumOfRefStars 42
        RefStar1  1.8  1.1   147  11.0620  61.7510 152.25  51.00
        RefStar2  1.8  0.0   252  12.9000  55.9600 226.50  67.25
        RefStar3  2.7  0.9    50  16.4000  61.5140 245.00 200.00
        RefStar4  2.2  0.1   180  13.3990  54.9250 244.00  80.50

    Parameters
    ----------
    path: str
       The yyyymmdd.ref MetRec RefStars file path.
    camera: str
       Identifier of the camera for which the RefStars file has been computed.
       If not provided, *UNK* will be assigned.

    Raises
    ------
    IOError
       if the RefStars file path specified does not exist.

    Examples
    --------
    >>> # Retrieving all the data, by column
    >>> stars = RefStarsFile('/Data/ICC7/20100319/20100319.ref')
    >>> stars['#']
    [1, 2, 3, 4]
    >>> stars['pixelsum']
    [147, 252, 50, 180]

    >>> # Retrieving all the data, by column and demonstrating the usage
    >>> # of the camera initialization parameter.
    >>> stars = RefStarsFile('/Data/ICC7/20100319/20100319.ref', camera='ICC7')
    >>> stars.camera
    ICC7
    >>> stars['Unknown_column_name']
    [nan, nan, nan, nan]
    >>> stars.header['Longitude']
    10.858890

    """

    columns = ['#', 'magnitude', 'B-V', 'pixelsum',
               'alpha', 'delta', 'x', 'y']

    def __init__(self, path, camera='UNK'):
        self._data = []
        super(RefStarsFile, self).__init__(path)
        self._camera = camera

    def __getitem__(self, item):
        """
        Returns the column ``item`` from the Ref Star data.

        Parameters
        ----------
        item: str
           Column name: '#', 'magnitude', 'B-V', 'pixelsum',
           'alpha', 'delta', 'x' and 'y'.

        Returns
        -------
        list
           Column values for the column item. If the requested item does not
           correspond to a valid column name, a list of np.nan of length equal
           to the number of data rows will be returned.

        """
        return [row.get(item, np.nan) for row in self._data]

    @property
    def camera(self):
        """Property: Identifier of the camera for which the MetRec Ref Stars
        File has been computed.
        """
        return self._camera

    @property
    def rawdata(self):
        """Property: list of OrderedDict with elements '#', 'magnitude', 'B-V',
        'pixelsum', 'alpha', 'delta', 'x' and 'y'.
        """
        return self._data

    def _parse_position_line(self, line):
        """
        :param str line: the RefStar{} data record line.
        :return:
        :rtype: OrderedDict
        """
        # Remove RefStar from the beginning of the line
        data = line[7:].split()

        values = []
        for elem in data:
            if '--' in elem:
                values.append(None)
            elif '.' in elem:
                values.append(float(elem))
            else:
                values.append(int(elem))

        row = OrderedDict(list(zip(self.columns, values)))
        return row

    def parse(self):
        """ Parse the entire REF astrometry file content."""
        in_header = True
        iterator = self._lines.__iter__()
        for line in iterator:
            line = line.strip()
            if line.startswith('RefStar'):
                in_header = False

            if in_header:
                try:
                    key, value = [part.strip() for part in line.split(' ', 1)]
                    self._header[key] = value
                except ValueError:
                    logging.warning('In RefStar file header section: %s, '
                                    'line: %s', self.path, line)
            else:
                try:
                    row = self._parse_position_line(line)
                except ValueError:
                    logging.error('In RefStar file data section: %s, '
                                  'line: %s', self.path, line)
                    raise
                self._data.append(row)
