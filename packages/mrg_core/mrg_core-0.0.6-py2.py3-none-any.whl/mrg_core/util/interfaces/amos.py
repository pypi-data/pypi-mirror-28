"""
   UFOCapture XML file class module.

"""
import datetime as dt
import xml.etree.ElementTree as ElementTree

import numpy as np


class UFOCaptureInfFile(object):
    """
    Class for a UFOCapture xml file. Contains data structure for the different
    elements of the file, and routines to access the data.

    Examples
    --------
    >>> # Reading a file:
    >>> di = UFOCaptureInfFile('test_data/AMOS/M20160930_045308_AMOSCHI-PC_A.XML')
    >>> # Display the data which can be used for further processing:
    >>> di.dataarr[0]
    {'use': 'yes', 'c_Dec': nan, 'c_x': nan, \
    'DateTime': datetime.datetime(2016, 9, 30, 4, 53, 8, 270000), 'c_y': nan, \
    'bright': 2.33, 'RA': 18.7219567, 'Time': 8.27, 'y': nan, 'x': nan, \
    'Dec': -68.7064479, '###': 21, 'c_RA': nan}


    Attributes
    ----------
    filename: str
        Filename of the XML file (the input parameter to __init__)

    camera: str
        Camera identifier which provides information about the camera that has
        recorded the data related to this inf file (default 'UNK')
        The code for the camera is taken from the name of the XML file (e.g. AMOSCHI-PC)

    camera_resolution: array of int
        Provides information about the camera resolution

    appearance_date : string
        Date of the meteor in the format as it is in the file ('dd.mm.yyyy')

    appearance_time : string
        Time of the meteor in the format as it is in the file ('hh:mm:ss.ssssss')

    start_time_dt: datetime
        Appearance date and time as Python datetime object

    frame_count: int
        Number of frames in which the meteor was detected plus

    dataarr : array of dictionary (here with one element only)
        'use'      : string   - Flag saying that this line can be used,
                                should always be 'yes'

    right_ascension : array of float
        All right ascension elements ---> converted to decimal degree

    declination : array of float
        All Declination elements

    c_x : array of float
        All fitted x elements ---> here all values are NaN

    c_y : array of float
        All fitted y elements ---> here all values are NaN

    c_ra : array of float
        All fitted RA elements ---> here all values are NaN

    c_dec : array of float
        All fitted Dec elements ---> here all values are NaN

    pos: array[2, n] of float
        Array containing all position values in the image[x, y], one for each
        meteor detection. This is provided for backward compatibility.
        --->  here only the first and the last element is with a value others are NaN

    """
    def __init__(self, filename):
        """
        Upon initialization, the inf file is read in and the content is
        assigned to class properties.

        Parameters:
        -----------
        filename: str
           path and name of one XML file.

        """

        # Reassign variables
        self.filename = filename

        # Initialize some stuff
        self.dataarr = []     # good data only
        self.camera_resolution = []

        self.bright = []
        self.right_ascension, self.declination = [], []
        self.c_x, self.c_y, self.c_ra, self.c_dec = [], [], [], []

        xml_file = ElementTree.parse(filename)
        root = xml_file.getroot()

        station = root.attrib
        self.camera = station.get('clip_name')[17:-1]

        self.appearance_date = (station.get('d') + '.' +
                                station.get('mo').zfill(2) + '.' +
                                station.get('y'))

        self.appearance_time = (station.get('h').zfill(2) + ':' +
                                station.get('m').zfill(2) + ':' +
                                station.get('s'))

        self.start_time_dt = dt.datetime.strptime(self.appearance_date + '-' +
                                                  self.appearance_time,
                                                  '%d.%m.%Y-%H:%M:%S.%f')

        datetime = dt.datetime.strptime(station.get('y') + station.get('mo') +
                                        station.get('d') + station.get('h') +
                                        station.get('m') + station.get('s'),
                                        '%Y%m%d%H%M%S.%f')
        fps = float(station.get('fps'))
        head = float(station.get('head'))

        # resolution of a camera
        self.camera_resolution.append(int(station.get('cx')))
        self.camera_resolution.append(int(station.get('cy')))

        #
        for ufo in xml_file.iter('ua2_fdata2'):
            fno = float(ufo.attrib.get('fno'))
            # Calculates the time for frames in respect to the DataTime.
            # Format of 'Time' is kept the same as from .inf files, i.e. ss.sss
            data = {
                '###': int(ufo.attrib.get('fno')),
                'Time': round(datetime.second +
                              datetime.microsecond * 10**(-6) +
                              (fno - head) / fps, 3),
                'DateTime': datetime + dt.timedelta(0, (fno - head) / fps),
                'bright': float(ufo.attrib.get('mag')),
                'RA': round(float(ufo.attrib.get('ra')) / 15., 7),
                'Dec': float(ufo.attrib.get('dec')),
                'x': np.nan,
                'y': np.nan,
                'c_x': np.nan,
                'c_y': np.nan,
                'c_RA': np.nan,
                'c_Dec': np.nan,
                'use': 'yes'}

            self.bright.append(data['bright'])
            self.right_ascension.append(data['RA'])
            self.declination.append(data['Dec'])
            self.c_x.append(data['c_x'])
            self.c_y.append(data['c_y'])
            self.c_ra.append(data['c_RA'])
            self.c_dec.append(data['c_Dec'])
            self.dataarr.append(data)

        # parse values of position of a meteor (x, y) and place them at the
        # beginning and the end
        for ufo in xml_file.iter('ua2_object'):
            self.dataarr[0]['x'] = float(ufo.attrib.get('x1'))
            self.dataarr[0]['y'] = float(ufo.attrib.get('y1'))
            self.dataarr[-1]['x'] = float(ufo.attrib.get('x2'))
            self.dataarr[-1]['y'] = float(ufo.attrib.get('y2'))
            self.frame_count = int(ufo.attrib.get('fN'))

    def _get_valid_data(self, name):
        """
        Returns a list with all the data for the column ``name`` for all
        frames in the data array, i.e. it returns a list with all the values
        associated to the column ``name in the internal data array.

        Parameters
        ----------
        name: str
           UFO-Capture INF file column name for which the data is to be
           retrieved.

        Returns
        -------
        list
           List with all the data for the UFO-Capture INF file column
           ``name``.

        """
        return [element[name] for element in self.dataarr]

    @property
    def astrometry(self):
        """
         Returns a list of two-dimensional float precision vectors (tuples)
         providing the right ascension and declination of the meteor for all
         frames in the UFO Capture file.  This attribute is provided for
         backward compatibility.
        """
        return list(zip(self.right_ascension, self.declination))

    @property
    def datetime(self):
        """
        Returns a list of datetime objects providing the times for all frames
        in the UFO Capture File.
        """
        return self._get_valid_data('DateTime')

    @property
    def pos(self):
        """
         Returns a list of two-dimensional float precision vectors (tuples)
         providing the horizontal and vertical position of the meteor in the
         recorded image.  Note that since the UFO Capture file provides this
         information only for the first and last frames, therefore all other
         positions are set to NaN.  The horizontal and vertical positions are
         provided in pixels.  This attribute is provided for backward
         compatibility.
        """
        return list(zip(self.x_pos, self.y_pos))

    @property
    def x_pos(self):
        """
         Returns a list of float precision numbers providing the horizontal
         position of the meteor in the recorded image.  Note that since the
         UFO Capture file provides this information only for the first and
         last frames, therefore all other positions are set to NaN.  The
         horizontal position is provided in pixels.
        """
        return self._get_valid_data('x')

    @property
    def y_pos(self):
        """
         Returns a list of float precision numbers providing the vertical
         position of the meteor in the recorded image.  Note that since the
         UFO Capture file provides this information only for the first and
         last frames, therefore all other positions are set to NaN.  The
         vertical position is provided in pixels.
        """
        return self._get_valid_data('y')
