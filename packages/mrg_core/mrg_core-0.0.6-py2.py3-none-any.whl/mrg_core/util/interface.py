"""
Routines related to reading/writing data from and to files/databases
Part of MOTS - Meteor Orbit trajectory Software (Version 3.x)
"""
#   --------------------------------------------------------------------------
#
#   Version History
#   --------------------------------------------------------------------------
#   v0.1,  08 Aug 2014, dvk - first go
#   v0.2,  11 Aug 2014, dvk - added mr_readinf2
#   v0.3,  19 Aug 2014, dvk - added readdaf
#   v0.4,  20 Aug 2014, dvk - added a check in readdaf for the column number
#   v1.0,  15 Mar 2015, dvk - updated mr_readinf - sometimes the *.inf file
#                             contains '60' seconds, change to 0 and make
#                             sure the minute is correct.
#   v1.1,  19 Jun 2015, dvk - added class mr_logfile
#   v1.2,  21 Jun 2015, dvk - bug fix in mr_logfile - didn't read date properly
#                             in newer MetRec versions
#   v1.3,  25 Jun 2015, dvk - Update mr_logfile(previoushour; date)
#   v1.4,  30 Jun 2015, dvk - completed documentation
#   v1.5,  12 Jul 2015, dvk - added class mots_daffile
#   v1.6,  17 Sep 2015, dvk - finished class mots_daffile
#   v1.7,  30 Sep 2015, dvk - added arrays of trajectory elements to
#                             mots_daffile; added 'datetime' objects for the
#                             date + time from the header and for each element
#                             in the trajectory
#   v1.8,  03 Oct 2015, dvk - all tested
#   v2.0,  27 Dec 2015, dvk - added class mr_inffile - deprecates mr_readinf
#                             mr_logfile: Added arrays for the individual meteor
#                             data elements, changed 'time' to string and added
#                             'DateTime' field in the meteors array.
#   v2.1,  12 Jan 2016, dvk - added array 'vel' in logfile
#   v2.2,  01 Aug 2016, dvk - Updated class names to CamelCase
#                           - Some syntax updates
#                           - renamed to mrg_interface.py
#   v2.3,  02 Aug 2016, dvk - More updates to make syntax conform to PEP-8
#   v2.4,  02 Aug 2016, dvk - Deleted unused variables tbeg, tend, dtold
#   v2.5,  03 Aug 2016, dvk - Changed 'datetime.datetime' to 'dt.datetime' in
#                             readdaf2 and readinf
#   v2.6,  09 Aug 2016, dvk - Changed 'appearance_date' and '.._time' back to
#                             'AppearanceDate' and 'AppearanceTime' in strings
#                             and when writing DAF files.
#   v2.7,  10 Aug 2016, dvk - In MetRecLogFile: Replace encoded characters \xe4
#                             and \xed with 'm' and 'b'
#   v2.8,  11 Aug 2016, dvk - In class MetRecLogFile, added the property 't_eff'
#                             (effective obs. time)
#   v2.9,  03 Oct 2016, jdr - Corrected 'trailing-whitespace', 'reimported',
#                             'unused-variable', 'anomalous-backslash-in-string',
#                             'wrong-import-order', 'bad-indentation',
#                             'bad-continuation', 'consider-using-enumerate' in
#                             function kml_traject, 'bad-whitespace' and
#                             'bare-except' errors from pylint.
#   v3.0,  06 Oct 2016, dvk - added 'read_daf' - this routine reads all daf files
#                             in the source directory recursively and provides
#                             one large data array with all trajectory data
#                             extracted from the files.
#   v3.1,  07 Oct 2016, dvk - updated name of routine read_daf to read_daf_files
#                             to avoid confusion.
#                           - added a routine read_inf_files similar to
#                             read_daf_files.
#   v3.2,  18 Oct 2016, jdr - Added the ''camera'' attribute to the class
#                             MetRecInfFile.
#   v3.3,  30 Nov 2016,  rr - Added a new class (UFOCaptureInfFile) for a
#                             UFOCapture xml files, with import of a module
#                             required to read xml format. The class includes
#                             also a new camera attribute: camera_resolution.
#   v3.4,  14 Dec 2016, jdr - Removed the if __name__ section, as this is purely
#                             an module file.
#                           - Removed testing functions.
#                           - Corrected minor PyLint errors.
#   v3.5,  21 Dec 2016, jdr - Removed unused functions readdaf and readdaf2.
#   v3.6,  28 Dec 2016, jdr - updated docstring documentation to follow
#                             numpydocs
#   v3.7,  02 Jan 2016, jdr - Updated DafFile class, refactoring some methods
#                             and adding new ones.
#   v3.8,  03 Jan 2016, jdr - Updated MetRecInfFile class modifying invalid
#                             attribute names and adding property decorators
#   v3.9,  04 Jan 2016, jdr - Updated MetRecLogFile class modifying invalid
#                             attribute names, and refactored pylint errors.
#   v3.10, 06 Jan 2016, jdr - Updated UFOCaptureInfFile class modifying invalid
#                             attribute names and adding property decorators.
#   v3.11, 24 Jan 2016,  rr - Updated UFOCaptureInfFile class adding station
#                             position and correcting appearance_date, appearance_time,
#                             and datetime for leading zeros.
#
from __future__ import print_function

from collections import OrderedDict
import datetime as dt
import fnmatch
import sys
import os
from io import open

import xml.etree.ElementTree as ET
import numpy as np

from mrg_core.util.astro import xyz2geo


# --------------------------------------------------------------------------------------------------
# Interface to MetRec files
# --------------------------------------------------------------------------------------------------
class MetRecInfFile(object):
    """
    Class for a MetRec INF file. Contains data structure for the different
    elements of the file, and routines to access the data.

    Examples
    --------
    >>> # Reading a file:
    >>> di = MetRecInfFile('/test_data/Metrec_Data/ICC7/20140830/004236.inf')
    >>> # Display the data which can be used for further processing:
    >>> di.dataarr[0]
    {'use': 'yes', 'c_Dec': 33.279, 'c_x': nan, \
    'DateTime': datetime.datetime(2014, 8, 31, 0, 42, 36, 862000), 'c_y': nan, \
    'bright': 3.9, 'RA': 301.143, 'Time': 36.862, 'y': 0.824, 'x': 0.425, \
    'Dec': 33.263, '###': 4, 'c_RA': 301.152}
    >>> # Accessing for example the astrometry:
    >>> for element in di.astrometry:
    >>>     print(element)
    (301.143, 33.263) \
    (301.8375, 32.764) \
    (302.3355, 32.393)
    ...

    Attributes
    ----------
    filename: str
        Filename of the MetRec INF file (the input parameter to __init__)

    camera: str
        Camera identifier which provides information about the camera that has
        recorded the data related to this inf file (default 'UNK')

    appearance_date: str
        Date of the meteor in the format as it is in the file ('dd.mm.yyyy')

    appearance_time: str
        Time of the meteor in the format as it is in the file ('hh:mm:ss')

    start_time_dt : datetime
        Appearance date and time as Python datetime object

    reference_stars: str
        Path and name of the ReferenceStars file, e.g. '../config/20140828.ref'

    frame_count: int
        Number of frames in which the meteor was detected plus the pre- and
        post-detection frames (i.e. normally the number of trajectory elements
        is smaller than this. In the case of CILBO, we add 3 frames before and
        after the detection, thus the number of trajectory lines is
        frame_count - 2*3.

    rawdataarr: array of dictionary
        Contains the raw data as a dictionary with elements '###', 'Time',
        'DateTime', 'bright', 'x', 'y', 'alpha', 'delta', 'c_x', 'c_y',
        'c_alpha', 'c_delta', 'use'.

    dataarr: array of dictionary
        This is what should normally be used in further computations.
        Contains the data converted into a form where it can be used - only
        the entries where 'use' = yes are taken, The detailed elements are:
        '###'      : string   - orginial number of the saved frame
        'Time'     : string   - Time of meteor as given in inf file, string
        'DateTime' : DateTime - Time of meteor
        'x'        : float    - horizontal position of meteor in image (0..1)
        'y'        : float    - vertical position of meteor in image (0..1)
        'RA'       : float    - Right Ascension of meteor
        'Dec'      : float    - Decliation of meteor
        'c_x'      : float    - horizontal position fitted to a line
        'c_y'      : float    -  vertical position fitted to a line
        'c_RA'     : float    - Right Ascension of meteor fitted to a line
        'c_Dec'    : float    - Decliatino of meteor fitted to a line
        'use'      : string   - Flag saying that this line can be used,
                                should always be 'yes'

    right_ascension: array of float
        All right ascension elements. NOTE: This and the following arrays only
        contain elements where the 'use' field said 'yes'.

    declination: array of float
        All Declination elements

    c_x : array of float
        All fitted x elements

    c_y : array of float
        All fitted y elements

    c_ra : array of float
        All fitted RA elements

    c_dec : array of float
        All fitted Declination elements

    """
    def __init__(self, filename, camera='UNK'):
        """
        Upon initialization, the inf file is read in and the content is
        assigned to class properties.

        Parameters
        ----------
        filename: str
           path and name of one MetRec INF file.
        camera: str
           Identifier of the camera used for recording the data corresponding
           to the MetRec INF file ``inffile``. If not provided, *UNK* will be
           assigned.

        """

        # Reassign variables
        self.filename = filename
        self.camera = camera

        # Initialize some stuff
        self.rawdataarr = []  # a list of dictionaries called 'rawdata'
        self.dataarr = []     # good data only

        self.right_ascension, self.declination = [], []
        self.c_x, self.c_y, self.c_ra, self.c_dec = [], [], [], []

        if not os.path.isfile(self.filename):
            print('MetRecInfFile encountered an I/O error: '
                  'file {} does not exist'.format(self.filename))
            sys.exit()

        with open(self.filename, 'r', encoding='utf-8') as inffile:
            while True:
                line = inffile.readline()
                if not line:
                    break

                # Depending on contents of line, assign to different variables
                if 'AppearanceDate' in line:
                    self.appearance_date = line.split()[1].strip()

                if 'AppearanceTime' in line:
                    self.appearance_time = line.split()[1].strip()
                    self.start_time_dt = \
                        dt.datetime.strptime(self.appearance_date + '-' + self.appearance_time,
                                             '%d.%m.%Y-%H:%M:%S')

                if 'ReferenceStars' in line:
                    self.reference_stars = line.split()[1].strip()

                if 'FrameCount' in line:
                    self.frame_count = line.split()[1].strip()

                if '#' in line:
                    # Now we know that the next line is a data element.
                    # We read it in until we get an empty line (length = 0).
                    line = inffile.readline().strip()

                    #
                    # Used to check whether we go to the next minute.
                    #
                    oldseconds = 0.0
                    starttime = (self.start_time_dt -
                                 dt.timedelta(0, self.start_time_dt.second))
                    while len(line) > 0:
                        lineels = line.split()

                        data = {
                            '###': int(lineels[0]),
                            'Time': float(lineels[1]),
                            'x': float(lineels[3]),
                            'y': float(lineels[4]),
                            'alpha': float(lineels[5]),
                            'delta': float(lineels[6]),
                            'use': lineels[11]
                        }

                        # Creating datetime object - handle that the 'Time' field
                        # may go from 59 to 0. In the inf files sometimes there
                        # was a 60 in there too! Note that we assume that starttime1
                        # is equal ot starttime2. 'starttime' was created outside
                        # the loop
                        seconds = data['Time']
                        if seconds < oldseconds:
                            # When time goes 'backwards' add one minute
                            starttime = starttime + dt.timedelta(0, 60)
                        oldseconds = seconds
                        data['DateTime'] = starttime + dt.timedelta(0, seconds)
                        try:
                            data['bright'] = float(lineels[2])
                        except ValueError:
                            data['bright'] = np.nan
                        try:
                            data['c_x'] = float(lineels[7])
                        except ValueError:
                            data['c_x'] = np.nan
                        try:
                            data['c_y'] = float(lineels[8])
                        except ValueError:
                            data['c_y'] = np.nan
                        try:
                            data['c_alpha'] = float(lineels[9])
                        except ValueError:
                            data['c_alpha'] = np.nan
                        try:
                            data['c_delta'] = float(lineels[10])
                        except ValueError:
                            data['c_delta'] = np.nan

                        # Append data to dataarr and read next line.
                        self.rawdataarr.append(data)

                        line = inffile.readline().strip()

                    # Now produce the 'good data' array
                    for i, element in enumerate(self.rawdataarr):
                        if element['use'] == 'yes':
                            data = {
                                '###': self.rawdataarr[i]['###'],
                                'Time': self.rawdataarr[i]['Time'],
                                'DateTime': self.rawdataarr[i]['DateTime'],
                                'bright': self.rawdataarr[i]['bright'],
                                'x': self.rawdataarr[i]['x'],
                                'y': self.rawdataarr[i]['y'],
                                'RA': round(self.rawdataarr[i]['alpha'] * 15., 4),
                                'Dec': self.rawdataarr[i]['delta'],
                                'c_x': self.rawdataarr[i]['c_x'],
                                'c_y': self.rawdataarr[i]['c_y'],
                                'c_RA': round(self.rawdataarr[i]['c_alpha'] * 15., 4),
                                'c_Dec': self.rawdataarr[i]['c_delta'],
                                'use': self.rawdataarr[i]['use']
                            }

                            self.right_ascension.append(data['RA'])
                            self.declination.append(data['Dec'])
                            self.c_x.append(data['c_x'])
                            self.c_y.append(data['c_y'])
                            self.c_ra.append(data['c_RA'])
                            self.c_dec.append(data['c_Dec'])

                            self.dataarr.append(data)

    def _get_valid_data(self, name):
        """
        Returns a list with all the data for the column ``name`` for those
        frames tagged for *USE* in the MetRec INF file, i.e. it filters the
        raw data read from MetRec INF file, by column ``name`` for those
        frames (lines) tagged where the column *use* is set to **yes**.

        Parameters
        ----------
        name: str
           MetRec INF file column name for which the data is to be retrieved.

        Returns
        -------
        list
           List with all the data for the MetRec INF file column ``name`` of
           those frames tagged for *USE*.

        """
        return [element[name]
                for element in self.rawdataarr if element['use'] == 'yes']

    @property
    def astrometry(self):
        """
         Returns a list of two-dimensional float precision vectors (tuples)
         providing the right ascension and declination of the meteor for those
         frames tagged for *USE* in the MetRec INF file.  This attribute is
         provided for backward compatibility.
        """
        return list(zip(self.right_ascension, self.declination))

    @property
    def bright(self):
        """
        Returns a list of float precision numbers providing the magnitude of
        the meteor for those frames tagged for *USE* in the MetRec INF file.
        """
        return self._get_valid_data('bright')

    @property
    def datetime(self):
        """
        Returns a list of datetime objects providing the times for those frames
        tagged for *USE* in the MetRec INF file.
        """
        return self._get_valid_data('DateTime')

    @property
    def pos(self):
        """
         Returns a list of two-dimensional float precision vectors (tuples)
         providing the horizontal and vertical position of the meteor in the
         recorded image for those frames tagged for *USE* in the MetRec INF
         file.  Both position values range from 0 to 1.  This attribute is
         provided for backward compatibility.
        """
        return list(zip(self.x_pos, self.y_pos))

    @property
    def x_pos(self):
        """
         Returns a list of float precision numbers providing the horizontal
         position of the meteor in the recorded image for those frames tagged
         for *USE* in the MetRec INF file.  These values range from 0 to 1.
        """
        return self._get_valid_data('x')

    @property
    def y_pos(self):
        """
         Returns a list of float precision numbers providing the vertical
         position of the meteor in the recorded image for those frames tagged
         for *USE* in the MetRec INF file.  These values range from 0 to 1.
        """
        return self._get_valid_data('y')


# DafFile version history
#  dvk, V0.1 12 Jul 2015
#  dvk, V1.0 15 Sep 2015
#  dvk, V1.1 03 Oct 2015
#  jdr, V1.2 27 Dec 2016
#     - Completed write method to add Shower and Accuracy and corrected the
#       FrameCount header keyword.
#  jdr, v1.3 02 Jan 2017:
#     - Added support 'private' method _header_str and _str_data and removed
#       the duplicated code from the summary and write public methods.
#     - Removed unnecessary verification of input MetRec Log file name in the
#       write method.
#     - Modified the way information is presented on the console when using
#       summary method.
#     - Replace try: open, except IOError by os.path.isfile call in __init__
#     - Modified attribute names to make them PEP-8 compliant.
class DafFile(object):
    """
    Class for a 'detailed altitude file'. Contains data structure for the
    different elements of the file, and routines to access the data.

    Examples
    --------
    >>> # Reading a file:
    >>> df = DafFile('test_data/daffiles_checked/20111213/000143.daf')
    >>> df.trajectory1[0]
    {'dv': '--.---', 'dist': 109353.3, 'dpos': 1.7, 'dh': '----.-',
    'ddist': '----.-', 'h': 100556.0, 'v': '--.---', 'lon': -16.924,
    'lat': 28.534, 'Bright': 3.7, 'Time': 43.68, 'y': 0.958, 'x': 0.615,
    '###': 0}
    >>> df.summary()

    Attributes
    ----------
    filename: str
       Name of the daffile

    log_file1: str
       Name of the related log file

    station_directory1: str
       Name of the directory where this data resides

    appearance_date1: str
       Date of the meteor as seen from station 1 (note: after midnight this is
       one plus the date given in the directory name)

    appearance_time1: string
        Time of the meteor as seen from station 1

    datetime1: datetime object
        Date and time of the meteor as Python datetime object

    inf_filename1: string
        Name of the inf file from station 1 which was used to create the
        information in this file

    stream1: string
        Stream as identified by MetRec from station 1

    frame_count1: integer
        Number of frames in which the meteor was detected plus the pre- and
        post-detection frames (i.e. normally the number of trajectory elements
        is smaller than this. In the case of CILBO, we add 3 frames before and
        after the detection, thus the number of trajectory lines is
        frame_count - 2*3.

    trajectory1: array of dictionary
        For each frame where the meteor is detected, a line describing the
        trajectory is given. It contains the following keys:

        '###'      : int      - a number starting with 0
        'Time'     : float    - the time entry, these are seconds + milliseconds
        'DateTime' : datetime - the correct time of this frame as datetime
                                object, from appearance_date/Time + this 'Time'
        'Bright'   : float    - the magnitude of the meteor (from inf file)
        'x'        : float    - position in x direction, 0 to 1 (from inf file)
        'y'        : float    - position in y direction, 0 to 1 (from inf file)
        'h'        : float    - computed altitude, in m
        'dh'       : float    - estimated error in altitude, in m
        'dpos'     : float    - estimated error in position (independent of
                                x/y/z), in m
        'lon'      : float    - longitude of subpoint in decimal degrees
        'lat'      : float    - latitude of subpoint in decimal degrees
        'dist'     : float    - distance to camera1, in m
        'ddist'    : float    - an error estimate of this distance
        'v'        : float    - velocity computed from one frame to the next
                                in km/s. NOTE: First line is empty!
        'dv'       : float    - an error estimate for the velocity, in km/s

    number1, time1, ... dv1 : As above, but an array containing all these
    elements.

    NOTE: All these entries except 'daffile' are repeated for camera 2.

    """
    # ----------------------------------------------------------------------------------------------
    def __init__(self, filename):
        """
        Upon initialization, the daf file is read in and the content is
        assigned to class properties.

        Parameters
        ----------
        filename: str
            Path and name of one .daf file.

        """
        self.filename = filename
        self.trajectory1 = []         # a list (of dictionary 'trajectory1')
        self.trajectory2 = []
        self.number1, self.number2 = [], []
        self.time1, self.time2 = [], []
        self.datetime1, self.datetime2 = [], []
        self.bright1, self.bright2 = [], []
        self.x_pxl1, self.x_pxl2 = [], []
        self.y_pxl1, self.y_pxl2 = [], []
        self.height1, self.height2 = [], []
        self.dh1, self.dh2 = [], []
        self.dpos1, self.dpos2 = [], []
        self.lon1, self.lon2 = [], []
        self.lat1, self.lat2 = [], []
        self.dist1, self.dist2 = [], []
        self.ddist1, self.ddist2 = [], []
        self.vel1, self.vel2 = [], []
        self.dv1, self.dv2 = [], []

        if not os.path.isfile(self.filename):
            # print('Class DafFile encountered an I/O error: '
            #       'file {} does not exist'.format(self.filename))
            raise IOError('Class DafFile encountered an I/O error: '
                          'file {} does not exist'.format(self.filename))
            # sys.exit()

        count = 1
        with open(self.filename, 'r', encoding='utf-8') as daf:
            while True:
                line = daf.readline()

                if not line:
                    break
                # Depending on contents of line, assign to different variables
                # Since all station 1 stuff comes first we assume the first
                # time round everything goes in the '1' variables. Once
                # 'Station 2' was found, assign second station
                if 'Station 2' in line:
                    count = 2

                if 'LogFile:' in line:
                    if count == 1:
                        self.log_file1 = line.split(':')[1].lstrip().rstrip()
                    else:
                        self.log_file2 = line.split(':')[1].lstrip().rstrip()

                if 'StationDirectory' in line:
                    if count == 1:
                        self.station_directory1 = \
                            line.split(' ')[1].lstrip().rstrip()
                    else:
                        self.station_directory2 = \
                            line.split(' ')[1].lstrip().rstrip()

                if 'AppearanceDate' in line:
                    if count == 1:
                        self.appearance_date1 = \
                            line.split(':')[1].lstrip().rstrip()
                    else:
                        self.appearance_date2 = \
                            line.split(':')[1].lstrip().rstrip()

                if 'AppearanceTime' in line:
                    if count == 1:
                        self.appearance_time1 = \
                            line.split(' ')[1].lstrip().rstrip()
                        self.starttime1 = \
                            dt.datetime.strptime(self.appearance_date1 + '-' +
                                                 self.appearance_time1,
                                                 '%d.%m.%Y-%H:%M:%S')
                    else:
                        self.appearance_time2 = \
                            line.split(' ')[1].lstrip().rstrip()
                        self.starttime2 = \
                            dt.datetime.strptime(self.appearance_date2 + '-' +
                                                 self.appearance_time2,
                                                 '%d.%m.%Y-%H:%M:%S')

                if 'INFFilename' in line:
                    if count == 1:
                        self.inf_filename1 = line.split(':')[1].lstrip().rstrip()
                    else:
                        self.inf_filename2 = line.split(':')[1].lstrip().rstrip()

                self.stream1 = '---'    # needed for daf files without Stream
                self.stream2 = '---'
                if 'Stream' in line:
                    if count == 1:
                        self.stream1 = line.split(':')[1].lstrip().rstrip()
                    else:
                        self.stream2 = line.split(':')[1].lstrip().rstrip()

                if 'FrameCount' in line:
                    if count == 1:
                        self.frame_count1 = line.split(':')[1].lstrip().rstrip()
                    else:
                        self.frame_count2 = line.split(':')[1].lstrip().rstrip()

                if '!###' in line:
                    # Now we know that the next line is a trajectory element.
                    # We read it in until we get an empty line(length = 0).
                    line = daf.readline().lstrip()

                    #
                    # Used to check whether we go to the next minute
                    #
                    oldseconds = 0.0
                    starttime = self.starttime1\
                                - dt.timedelta(0, self.starttime1.second)
                    while len(line) > 0:
                        trajectory = {}

                        # split using white spaces
                        line = line.replace('   ', ' ')
                        line = line.replace('  ', ' ')
                        lineels = line.split(' ')
                        # print "lineels: ", lineels
                        trajectory['###'] = int(lineels[0])
                        trajectory['Time'] = float(lineels[1])

                        # Creating datetime object - handle that the 'Time' field
                        # may go from 59 to 0. In the inf files sometimes there
                        # was a 60 in there too! Note that we assume that starttime1
                        # is equal ot starttime2. 'starttime' was created outside
                        # the loop
                        seconds = float(trajectory['Time'])
                        if seconds < oldseconds:
                            # When time goes 'backwards' add one minute
                            starttime = starttime + dt.timedelta(0, 60)
                        oldseconds = seconds
                        trajectory['DateTime'] = starttime \
                                                + dt.timedelta(0, seconds)

                        trajectory['Bright'] = float(lineels[2])
                        trajectory['x'] = float(lineels[3])
                        trajectory['y'] = float(lineels[4])
                        trajectory['h'] = float(lineels[5])
                        try:
                            trajectory['dh'] = float(lineels[6])
                        except ValueError:
                            trajectory['dh'] = lineels[6].rstrip()
                        try:
                            trajectory['dpos'] = float(lineels[7])
                        except ValueError:
                            trajectory['dpos'] = lineels[7].rstrip()
                        trajectory['lon'] = float(lineels[8])
                        trajectory['lat'] = float(lineels[9])
                        trajectory['dist'] = float(lineels[10])
                        try:
                            trajectory['ddist'] = float(lineels[11])
                        except ValueError:
                            trajectory['ddist'] = lineels[11]
                        try:
                            trajectory['v'] = float(lineels[12])
                        except ValueError:
                            trajectory['v'] = lineels[12].rstrip()
                        try:
                            trajectory['dv'] = float(lineels[13])
                        except ValueError:
                            trajectory['dv'] = lineels[13].rstrip()

                        if count == 1:
                            self.trajectory1.append(trajectory)

                            # Create arrays with same info as in trajectory[]
                            self.number1.append(trajectory['###'])
                            self.time1.append(trajectory['Time'])
                            self.datetime1.append(trajectory['DateTime'])
                            self.bright1.append(trajectory['Bright'])
                            self.x_pxl1.append(trajectory['x'])
                            self.y_pxl1.append(trajectory['y'])
                            try:
                                self.height1.append(float(trajectory['h']))
                            except ValueError:
                                self.height1.append(np.nan)
                            try:
                                self.dh1.append(float(trajectory['dh']))
                            except ValueError:
                                self.dh1.append(np.nan)
                            try:
                                self.dpos1.append(float(trajectory['dpos']))
                            except ValueError:
                                self.dpos1.append(np.nan)
                            self.lon1.append(trajectory['lon'])
                            self.lat1.append(trajectory['lat'])
                            self.dist1.append(trajectory['dist'])
                            try:
                                self.ddist1.append(float(trajectory['ddist']))
                            except ValueError:
                                self.ddist1.append(np.nan)
                            try:
                                self.vel1.append(float(trajectory['v']))
                            except ValueError:
                                self.vel1.append(np.nan)
                            try:
                                self.dv1.append(float(trajectory['dv']))
                            except ValueError:
                                self.dv1.append(np.nan)

                        else:
                            self.trajectory2.append(trajectory)

                            # Create arrays with same info as in trajectory[]
                            self.number2.append(trajectory['###'])
                            self.time2.append(trajectory['Time'])
                            self.datetime2.append(trajectory['DateTime'])
                            self.bright2.append(trajectory['Bright'])
                            self.x_pxl2.append(trajectory['x'])
                            self.y_pxl2.append(trajectory['y'])
                            try:
                                self.height2.append(float(trajectory['h']))
                            except ValueError:
                                self.height2.append(np.nan)
                            try:
                                self.dh2.append(float(trajectory['dh']))
                            except ValueError:
                                self.dh2.append(np.nan)
                            try:
                                self.dpos2.append(float(trajectory['dpos']))
                            except ValueError:
                                self.dpos2.append(np.nan)
                            self.lon2.append(trajectory['lon'])
                            self.lat2.append(trajectory['lat'])
                            self.dist2.append(trajectory['dist'])
                            try:
                                self.ddist2.append(float(trajectory['ddist']))
                            except ValueError:
                                self.ddist2.append(np.nan)
                            try:
                                self.vel2.append(float(trajectory['v']))
                            except ValueError:
                                self.vel2.append(np.nan)
                            try:
                                self.dv2.append(float(trajectory['dv']))
                            except ValueError:
                                self.dv2.append(np.nan)

                        line = daf.readline().lstrip()

    @staticmethod
    def _str_data(trajectory):
        """
        Returns a string representation of the DAF data block provided in the
        input ``trajectory``.

        Parameters
        ----------
        trajectory: list
           n-element list of dictionary providing the DAF data block points to
           be converted to a string representation.

        Returns
        -------
        str
           a string representation of the DAF data block provided in the input
           ``trajectory``.

        """
        data = ('!                     Position         '
                'Altitude in m            SubPoint      '
                '  Cam. dist in m  Velocity in km/s\n'
                '!###   Time  Bright   x      y       h       +/-h'
                '  +/-pos   lon/deg  lat/deg     dist   '
                '+/-dist     v       +/-v\n')

        for point in trajectory:
            data += str.format(' %03i  %05.2f %6.1f  %5.3f  %5.3f  %8.1f' %
                               (point['###'],
                                point['Time'],
                                point['Bright'],
                                point['x'], point['y'],
                                point['h']))
            try:
                # 'dh' could be string('----.-') or a number
                data += str.format('  %6.1f' % point['dh'])

            #
            # The function str will throw an TypeError exception if
            # trajectory['dh'] is not a number (float or int).
            #
            except TypeError:
                data += '  ' + point['dh']

            data += str.format('  %5.1f  %8.3f  %7.3f  %9.1f' %
                               (point['dpos'],
                                point['lon'], point['lat'],
                                point['dist']))
            try:
                # 'ddist' could be string ('----.-') or a number
                data += str.format('  %6.1f' % point['ddist'])
            except TypeError:
                data += '  ----.-'

            try:
                # 'v' will be '--.---' for the first entry or nothing
                data += '  %7.3f' % point['v']
            except TypeError:
                data += '   --.---'

            try:
                # 'dv' will be '--.---' or a float
                data += '  %7.3f' % point['dv']
            except TypeError:
                data += '   --.---'

            data += '\n'

        return data

    @staticmethod
    def _str_header(header_dict):
        """
        Returns a string representation of the DAF data header block
        corresponding to the ``header_dict``.

        Parameters
        ----------
        header_dict: OrderedDict
           OrderedDict object that contains the DAF data header block to be
           converted into a string.

        Returns
        -------
        str
           a string representation of the data block corresponding to the
           ``header_dict``.

        """
        header = ''
        for name in header_dict:
            header += '{} {}\n'.format(name, str(header_dict[name]))

        return header

    def summary(self):
        """
        Prints a summary of the DAF file content to the console.

        Examples
        --------
        >>> daf = DafFile('test_data/daffiles_checked/20111213/000143.daf')
        >>> daf.summary()

        """
        print('-' * 80)
        print("Summary for daf file %s:\n" % self.filename)
        # Current version of the reader does not contain information about
        # accuracy.
        header_dict = OrderedDict([
            ('Station', 1),
            ('LogFile:', self.log_file1),
            ('StationDirectory:', self.station_directory1),
            ('AppearanceDate:', self.appearance_date1),
            ('AppearanceTime:', self.appearance_time1),
            ('INFFilename:', self.inf_filename1),
            ('FrameCount:', self.frame_count1),
            ('Shower:', self.stream1)])

        print(self._str_header(header_dict))
        print(self._str_data(self.trajectory1))

        header_dict = OrderedDict([
            ('Station', 2),
            ('LogFile:', self.log_file2),
            ('StationDirectory:', self.station_directory2),
            ('AppearanceDate:', self.appearance_date2),
            ('AppearanceTime:', self.appearance_time2),
            ('INFFilename:', self.inf_filename2),
            ('FrameCount:', self.frame_count2),
            ('Shower:', self.stream2)])
        print(self._str_header(header_dict))
        print(self._str_data(self.trajectory2))

        print('-' * 80)

    @staticmethod
    def write(filename,
              log_file1, station_directory1, appearance_date1, appearance_time1,
              inf_filename1, stream1, frame_count1, accuracy1, trajectory1,
              log_file2, station_directory2, appearance_date2, appearance_time2,
              inf_filename2, stream2, frame_count2, accuracy2, trajectory2):
        """
        Writes a daf file with 'filename'.

        Returns error messages in case the format of some input parameters
        is not ok or if the file couldn't be written.
        """
        error = ''                       # String containing error messages
        try:
            outfile = open(filename, 'wb')
        except IOError:
            return 'outFile %s could not be opened.' % filename

        # use 'set' to check because we don't know the order
        tkeys = ['dv', 'dist', 'dpos', 'dh', 'ddist', 'DateTime', 'h', 'v', 'lon', 'lat',
                 'Bright', 'Time', 'y', 'x', '###']
        if set(trajectory1[0].keys()) != set(tkeys):
            error += 'A column in trajectory1 seems to be missing\n'
        if set(trajectory2[0].keys()) != set(tkeys):
            error += 'A column in trajectory2 seems to be missing\n'

        header_dict = OrderedDict([
            ('Station', 1),
            ('LogFile:', log_file1),
            ('StationDirectory:', station_directory1),
            ('AppearanceDate:', appearance_date1),
            ('AppearanceTime:', appearance_time1),
            ('INFFilename:', inf_filename1),
            ('FrameCount:', frame_count1),
            ('Shower:', stream1),
            ('Accuracy:', "%4.1f'" % accuracy1)])
        outfile.write('{}\n'.format(DafFile._str_header(header_dict)))
        outfile.write('{}\n'.format(DafFile._str_data(trajectory1)))

        header_dict = OrderedDict([
            ('Station', 2),
            ('LogFile:', log_file2),
            ('StationDirectory:', station_directory2),
            ('AppearanceDate:', appearance_date2),
            ('AppearanceTime:', appearance_time2),
            ('INFFilename:', inf_filename2),
            ('FrameCount:', frame_count2),
            ('Shower:', stream2),
            ('Accuracy:', "%4.1f'" % accuracy2)])
        outfile.write('{}\n'.format(DafFile._str_header(header_dict)))
        outfile.write('{}\n'.format(DafFile._str_data(trajectory2)))

        outfile.close()
        return error


# MetRecLogFile version history
#
# dvk, 20 Jun 2015
# dvk, 25 Jun 2015:
#    - Changed 'previoushour' to 14 instead of 0. This is needed so that one
#      day is added if the first meteor appears after midnight. NOTE: This may
#      not work in Australia! AND: For 20130320 I now get 0 for ICC7 (instead
#      of 48).
#    - Updated 'date' - its the date of the file creation, not necessarily the
#      evening of the observing night.
# dvk, 04 Oct 2015 - added property 'ref_filename'
# dvk, V2.0, 27 Dec 2015 - added individual arrays for data of meteors
# dvk, V2.1, 10 Aug 2016 - replaced more encoded characters
# dvk, V2.2, 11 Aug 2016 - added property t_eff
# jdr, v2.2.1, 21 Dec 2016 - reformatted documentation
# jdr, v2.3, 04 Jan 2016:
#    - Replace try: open, except IOError by os.path.isfile call in __init__
#    - Modified attribute names to make them PEP-8 compliant.
class MetRecLogFile(object):
    """
    Class for a MetRec log file. Contains data structure for the different
    content elements of the file, and routines to access the data.

    Attributes
    ----------
    filename : str
         Name of the logfile
    software : str
         Name/version of software, e.g. 'MetRec V5.1 (2012/06/28 W32)'
    date : str
         Date of file creation
    ref_filename : str
         path and name of reference file
    tbeg : datetime
         Date and time of beginning of observation
    tend : datetime
         Date and time of end of observation
    no_obs_meteors : int
         Number of observed meteors
    no_spo : int
         Number of sporadic meteors
    configuration : dict
         A dictionary containing the configuration items
         Details to come !TODO
    t_eff: float
         The effective observing time in seconds
    meteors: list
         An array containing summary information for all meteor entries
         in the log file. It contains the following keys:
         'time'     : string   - time of meteor as given in file
         'DateTime' : datetime - date and time of the meteor
         'number'   : integer  - number in the original (!) log file
         'xbeg'     : float    - x pos. of meteor beginning in image
         'ybeg'     : float    - y pos. of meteor beginning in image
         'xend'     : float    - x pos. of meteor end in image
         'yend'     : float    - y pos. of meteor end in image
         'frames'   : int      - no. of frames where meteor visible
         'duration' : float    - duration of meteor in s
         'pixel'    : integer  - number of pixels above brightness thresh.
         'dir'      : float    - direction of meteor in degrees
         'vel'      : float    - velocity in degrees/s
         'snr'      : float    - signal-to-noise ration
         'shower'   : string   - three-letter shower association
         'bright'   : float    - maximum magnitude of meteor
         'raddist'  : float    - distance to radiant in degrees
                                 ('nan' for SPO)
         'exp vel'  : float    - expected apparent velocity in deg/s
                                 ('nan' for SPO)
         'RAbeg'    : float    - R.A. of meteor beginning
         'Decbeg'   : float    - Dec of meteor beginning
         'RAend'    : float    - R.A. of meteor ending
         'Decend'   : float    - Dec of meteor ending
         'acc'      : float    - estimate of astrometric accuracy in arcmin

    For each of the elements in 'meteors' an individual array is also produced
    for convenience (added in V2.0 of mr_logfile).

    Examples
    --------
    >>> lf = MetRecLogFile('test_data/ICC7/20111213/20111213.log')
    >>> # Finding the accuracy of a meteor of known time:
    >>> chktime = '02:42:58'
    >>> lf = MetRecLogFile('test_data/ICC7/20111002/20111002.log')
    >>> lf.acc[lf.time.index(chktime)]
    0.7

    """

    # --------------------------------------------------------------------------
    def __init__(self, filename):
        """
        Upon initialization, the log file is read in and the content is
        assigned to class properties.

        Parameters
        ----------
        filename: str
           path and name of one MetRec LOG file.

        """
        # Reassign variables
        self.filename = filename

        # Initialize some stuff
        cont = False             # needed for reading two lines of meteor
        delta = dt.timedelta(0)  # if 0, hours increase - set to 24 if
                                 # hour '0' follows hour '23'. Needed to add
                                 # a day for times after midnight
        previoushour = 16        # Updated in V1.3 - was 0 before, but then
                                 # it didn't add a day if the first meteor
                                 # was after midnight.

        self.time, self.datetime, self.number = [], [], []
        self.xbeg, self.ybeg, self.xend, self.yend = [], [], [], []
        self.frames, self.duration, self.pixel = [], [], []
        self.direction, self.snr, self.shower, self.bright = [], [], [], []
        self.raddist, self.expvel, self.rabeg, self.decbeg = [], [], [], []
        self.raend, self.decend, self.acc, self.vel = [], [], [], []
        self.meteors = []

        # Create date from filename as it needs the date of the
        # evening when the observation starts
        ddate = os.path.split(os.path.split(filename)[0])[1]

        if not os.path.isfile(self.filename):
            print('Class MetRecLogFile encountered an I/O error: '
                  'file {} does not exist'.format(self.filename))
            sys.exit()

        # with open(self.filename, 'r', encoding='utf-8', errors='ignore') as log_file:
        with open(self.filename, 'r', encoding='iso-8859-1') as log_file:

            for line in log_file:
                # Replace some special characters to avoid they don't print
                line = line.replace(u'\xf8', 'd')
                line = line.replace(u'\xe5', 'snr')
                line = line.replace(u'\xe4', '#')           # V2.1
                line = line.replace(u'\xed', 'b')           # V2.1
                line = line.strip()

                # line = line.decode('utf-8').replace('\r', '')
                # Get rid of possible leading spaces in direction
                line = line.replace('dir= ', 'dir=')
                line = line.replace('dir= ', 'dir=')

                lineels = line.split(' ')  # split into elements

                # Depending on contents of line, assign to different variables
                if 'Software:' in line:
                    self.software = line.split(':')[1].strip()

                if 'Date    :' in line:
                    # NOTE: This is the date when the file is created - i.e. if
                    # created after midnight, it is *not* the same as the filename
                    self.date = line.split(':')[1].strip().replace('/', '')

                if 'ReferenceStars' in line:
                    self.ref_filename =\
                        line.split('.:')[1].replace(' ', '').replace('\\', '/')

                if 'start of observation' in line:
                    tbegdate = line.rsplit()[4].replace('/', '')
                    tbegtime = line.rsplit()[5].replace(':', '')
                    self.tbeg = dt.datetime(int(tbegdate[0:4]),
                                            int(tbegdate[4:6]),
                                            int(tbegdate[6:8]),
                                            int(tbegtime[0:2]),
                                            int(tbegtime[2:4]),
                                            int(tbegtime[4:6]))

                if 'end of observation' in line:
                    tenddate = line.rsplit()[4].replace('/', '')
                    tendtime = line.rsplit()[5].replace(':', '')
                    self.tend = dt.datetime(int(tenddate[0:4]),
                                            int(tenddate[4:6]),
                                            int(tenddate[6:8]),
                                            int(tendtime[0:2]),
                                            int(tendtime[2:4]),
                                            int(tendtime[4:6]))

                if '# observed meteors' in line:
                    self.no_obs_meteors = int(line.rsplit()[4])

                if 'Sporadics (SPO)' in line:
                    no_spo = line.rsplit()[3].replace('#=', '').replace(',', '')
                    self.no_spo = int(no_spo)

                if 'effective observing time' in line:
                    t_eff_h = float(line.split(':')[1].split('h')[0].strip())
                    t_eff_m = float(line.split(':')[1].split('h')[1].split('m')[0].strip())
                    t_eff_s = float(line.split(':')[1].split('h')[1].split('m')[1].strip(' s'))
                    self.t_eff = t_eff_h * 3600. + t_eff_m * 60 + t_eff_s

                if ' Meteor #' in line:
                    cont = True  # set continuation flag
                    meteor = {}  # create a new dictionary
                    meteor['number'] = int(lineels[2].replace('#', ''))
                    self.number.append(meteor['number'])

                    meteor['time'] = lineels[0]
                    self.time.append(meteor['time'])
                    # When assigning time, add 1 day if '0 hours' comes after
                    # '23' hours
                    hour = int(lineels[0].split(':')[0])
                    if delta == dt.timedelta(0):
                        if (hour - previoushour) < 0:
                            delta = dt.timedelta(1)  # This is one day
                        previoushour = hour

                    meteor['DateTime'] = dt.datetime.strptime(ddate + lineels[0],
                                                              '%Y%m%d%H:%M:%S') + delta
                    self.datetime.append(meteor['DateTime'])

                    beg = lineels[4].split('->')[0]
                    beg = beg.replace('(', '').replace(')', '')
                    end = lineels[4].split('->')[1]
                    end = end.replace('(', '').replace(')', '')
                    meteor['xbeg'] = float(beg.split(',')[0])
                    self.xbeg.append(meteor['xbeg'])
                    meteor['ybeg'] = float(beg.split(',')[1])
                    self.ybeg.append(meteor['ybeg'])
                    meteor['xend'] = float(end.split(',')[0])
                    self.xend.append(meteor['xend'])
                    meteor['yend'] = float(end.split(',')[1])
                    self.yend.append(meteor['yend'])

                    meteor['frames'] = int(lineels[5].split('=')[1])
                    self.frames.append(meteor['frames'])

                    duration = lineels[6].split('=')[1].replace('s', '')
                    meteor['dur'] = float(duration)
                    self.duration.append(meteor['dur'])

                    meteor['pixel'] = int(lineels[7].split('=')[1])
                    self.pixel.append(meteor['pixel'])
                    direction = lineels[8].split('=')[1].replace('d', '')

                    meteor['dir'] = int(direction)
                    self.direction.append(meteor['dir'])

                    vel = lineels[9].split('=')[1].replace('d/s', '')
                    meteor['vel'] = float(vel)
                    self.vel.append(meteor['vel'])

                    meteor['snr'] = float(lineels[10].split('=')[1])
                    self.snr.append(meteor['snr'])

                elif cont:
                    cont = False
                    meteor['shower'] = lineels[0].split('=')[1]
                    self.shower.append(meteor['shower'])
                    bright = lineels[1].split('=')[1].replace('mag', '')
                    meteor['bright'] = float(bright)
                    self.bright.append(meteor['bright'])

                    # Check whether shower is 'SPO' - then line is shorter
                    if meteor['shower'] == 'SPO':
                        meteor['raddist'] = np.nan
                        self.raddist.append(meteor['raddist'])
                        meteor['exp vel'] = np.nan
                        self.expvel.append(meteor['exp vel'])
                        beg = lineels[2].replace('(', '').replace('d)', '')
                        beg = beg.split('h,')
                        end = lineels[4].replace('(', '').replace('d)', '')
                        end = end.split('h,')
                        meteor['RAbeg'] = float(beg[0])
                        self.rabeg.append(meteor['RAbeg'])
                        meteor['Decbeg'] = float(beg[1])
                        self.decbeg.append(meteor['Decbeg'])
                        meteor['RAend'] = float(end[0])
                        self.raend.append(meteor['RAend'])
                        meteor['Decend'] = float(end[1])
                        self.decend.append(meteor['Decend'])
                        acc = lineels[5].split('=')[1].replace("'", "")
                        meteor['acc'] = float(acc)
                        self.acc.append(meteor['acc'])

                    else:
                        raddist = lineels[2].split('=')[1].replace('d', '')
                        meteor['raddist'] = float(raddist)
                        self.raddist.append(meteor['raddist'])
                        exp_vel = lineels[4].split('=')[1].replace('d/s', '')
                        meteor['exp vel'] = float(exp_vel)
                        self.expvel.append(meteor['exp vel'])
                        beg = lineels[5].replace('(', '').replace('d)', '')
                        beg = beg.split('h,')
                        end = lineels[7].replace('(', '').replace('d)', '')
                        end = end.split('h,')
                        meteor['RAbeg'] = float(beg[0])
                        self.rabeg.append(meteor['RAbeg'])
                        meteor['Decbeg'] = float(beg[1])
                        self.decbeg.append(meteor['Decbeg'])
                        meteor['RAend'] = float(end[0])
                        self.raend.append(meteor['RAend'])
                        meteor['Decend'] = float(end[1])
                        self.decend.append(meteor['Decend'])
                        acc = lineels[8].split('=')[1].replace("'", "")
                        meteor['acc'] = float(acc)
                        self.acc.append(meteor['acc'])

                    self.meteors.append(meteor)

        # The following are dummys only for now
        self.configuration = {'Autoconfiguration': 'no'}

    def summary(self):
        """
        Prints a summary of the logfile content to the console.
        !TODO: Add output for configuration.

        """
        print("---------------------------------")
        print("Summary for log file %s:" % self.filename)
        print("tbeg: %s" % self.tbeg.isoformat())
        print("tend: %s" % self.tend.isoformat())
        print("Duration: %s" % (self.tend - self.tbeg))
        print("Effective observing time: %f.1 s" % self.t_eff)          # V2.2
        print("No of observed meteors: %i" % self.no_obs_meteors)
        print("No of Sporadics: %i" % self.no_spo)
        print("Meteors: ")
        print("------------------------------------------------------------" +
              "-------------------------------------------------")
        print("  time     no  xbeg  ybeg  xend  yend frm  dur  px" +
              "  dir  sho  mag rdis expv  RAbeg Decbeg  RAend Decend  acc")
        print("------------------------------------------------------------" +
              "-------------------------------------------------")
        for meteor in self.meteors:
            print(('%8s %04i %5.3f %5.3f %5.3f %5.3f %03i %4.2f %03i' +
                   ' %5.1f %3s %4.1f %4.1f %4.1f %6.3f %6.2f %6.3f %6.2f' +
                   ' %4.1f')
                  % (meteor['time'], meteor['number'],
                     meteor['xbeg'], meteor['ybeg'],
                     meteor['xend'], meteor['yend'],
                     meteor['frames'], meteor['dur'], meteor['pixel'],
                     meteor['dir'], meteor['shower'], meteor['bright'],
                     meteor['raddist'], meteor['exp vel'],
                     meteor['RAbeg'], meteor['Decbeg'],
                     meteor['RAend'], meteor['Decend'], meteor['acc']))
        print("------------------------------------------------------------" +
              "----------------------------------------------------------")


def mr_readinf(filename):
    """
    Opens a MetRec INF file, returns data structure with complete content.

    Parameters
    ----------
    filename: str
        Path and name of one MetRec INF file.

    Returns
    -------
    tuple
       containing a data structure with the complete content of the file. This
       structure is as follows:

       -  appearance_date (str): AppearanceDate in the format 'YYYY/MM/DD'.
       -  appearance_time (str): AppearanceTime in the format hh:mm:ss.
       -  reference_stars (str): Filename of ReferenceStars file.
       -  frame_count (int): Number of frames in which a meteor was detected.
       -  data (numpy.array): An array with FC lines and the columns as in
          the MetRec INF files. It can be called via data['RA'], data['Dec'],
          etc.

    Notes
    -----
    1.  RA is in decimal hours!
    2.  Deprecated in v2.0, 26 Dec 2015. Use MetRecInfFile class instead!
        mr_readinf will be removed in the first official release of the
        MRG Toolkit and replaced by the MetRecInfFile class or
        equivalent.

    """
    inffile = open(filename, 'r', encoding='utf-8')
    appearance_date = inffile.readline().split(' ')[1].rstrip()
    appearance_time = inffile.readline().split(' ')[1].rstrip()
    reference_stars = inffile.readline().split(' ')[1].rstrip()
    frame_count = inffile.readline().split(' ')[1].rstrip()
    inffile.close()

    # Now use numpy to read the data - a bit inefficent as the file is closed
    data = np.genfromtxt(inffile, skip_header=5, dtype=
                         ['i2', 'float', 'float', 'float', 'float', 'float',
                          'float', 'float', 'float', 'float', 'float', 'a3'],
                         names=['no', 'time', 'appmag', 'x', 'y', 'RA',
                                'Dec', 'c_x', 'c_y', 'c_RA', 'c_Dec', 'use'])

    return appearance_date, appearance_time, reference_stars, frame_count, data


def mr_readinf2(inffile):
    """
    Reads a MetRec INF file, returns data usable for MOTS routines.
    Only take those elements marked as 'use = yes'.

    Parameters
    ----------
    inffile: str
        Path and name of one MetRec INF file.

    Returns
    -------
    tuple
        containing a data structure with the complete content of the file.
        This structure is as follows:

        -  infheader (dict): Header of the inf file. A dictionary with the
           entries {'AppearanceDate', 'AppearanceTime', 'RS','frame_count'}
           'RS' is the name of the ReferenceStars file (.ref).
        -  times (numpy.array): An array of datetime.datetime objects for
           each line of the inf file (i.e. each frame where the meteor was
           seen)
        -  pos (numpy.array): 2 x n array with x/y position for each frame.
        -  astrom (np.array): 2 x n array with RA/Dec for each frame.
        -  mag (np.array): vector giving apparent magnitude for each time
           in times.

        Empty values are filled with 'nan'.

    Examples
    --------
    >>> infheader, times, pos, astrom, mag = mr_readinf2(inffile)


    Notes
    -----
    1.  Deprecated in v2.0, 26 Dec 2015. Use MetRecInfFile class instead!
        mr_readinf will be removed in the first official release of the
        MRG Toolkit and replaced by the MetRecInfFile class or equivalent.

    """
    appear_date, appear_time, refstars, fcount, data = mr_readinf(inffile)

    # We collect the 'header' information in a dictionary
    infheader = {'AppearanceDate': appear_date, 'AppearanceTime': appear_time,
                 'RS': refstars, 'frame_count': fcount}

    # Collect time info - yyyy mm dd is in the 'AppearanceDate', hhmmss in
    # 'appearance_time - the milliseconds are in the data entry.
    year = int(appear_date.split('.')[2])
    month = int(appear_date.split('.')[1])
    day = int(appear_date.split('.')[0])
    hour = int(appear_time.split(':')[0])
    minute = int(appear_time.split(':')[1])

    times = []
    right_ascension, declination = [], []
    appmag = []
    posx, posy = [], []

    # [JDR] Remove unused variable i from the for loop by replacing it
    # with "_"
    for _, element in enumerate(data):
        # only take those that MetRec flags as to be used
        if element['use'] == 'yes':
            # need to split time into seconds and microseconds
            sec = int(element['time'])
            usec = int(round((element['time'] - sec) * 1000.)) * 1000

            if sec == 60:
                sec = 0    # the inf file may contain 60 - added in V1.0
                minute += 1

            times.append(dt.datetime(year, month, day,
                                     hour, minute, sec, usec))

            # RA needs to be converted from dec hours to dec degrees
            right_ascension.append(round(element['RA'] * 15., 4))
            declination.append(round(element['Dec'], 4))
            appmag.append(round(element['appmag'], 1))
            posx.append(round(element['x'], 3))
            posy.append(round(element['y'], 3))

    pos = zip(posx, posy)
    # Needed like this for other MOTS routines
    astrometry = zip(right_ascension, declination)

    return infheader, times, pos, astrometry, appmag


def read_daf_files(src):
    """
    Reads the content of all daf files into one large array in memory.

    Parameters
    ----------
    src: string
       Root path to read in daf files.

    Returns
    -------
    list
        The structure is data[met][traj][frame_no]{} where:

        -  met: a counter for the meteor.
        -  traj: either 0 or 1 - '0' for 'trajectory1' in the daf file,
           i.e. the trajectory as seen from station 1, '1' for
           'trajectory2' in the daf file, i.e. the trajectory as seen from
           station 2.
        -  frame_no: The number of the frame.  0 is the entry for the data
           linked to the first frame the meteor was observed in, 1 to the
           second, etc.
        -  {}: The dictionary contains the data as defined in the
           'trajectory1' or 'trajectory2' description of the DafFile
           interface class.

    """
    # ----------------------------------------------------------------------------------------------
    # Define variables and constants
    # ----------------------------------------------------------------------------------------------
    data = []

    # ----------------------------------------------------------------------------------------------
    # Do the work
    # ----------------------------------------------------------------------------------------------
    # Read all daf file names - from this web page:
    # http://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python
    # Queried 2016-10-05
    matches = []
    for root, _, file_names in os.walk(src):
        for filename in fnmatch.filter(file_names, '*.daf'):
            matches.append(os.path.join(root, filename))

    # Take the trajectory data from the daf files
    for filename in matches:
        daf = DafFile(filename)
        data.append([daf.trajectory1, daf.trajectory2])

    return data


def read_inf_files(src):
    """
    A function to read the content of all MetRec INF files into one large
    array in memory.

    Parameters
    ----------
    src: str
       Root path to read in inf files.

    Returns
    -------
    list
       The structure is data[met][frame_no]{} where:
          -  met: a counter for the meteor
          -  frame_no: The number of the frame.  0 is the entry for the data
             linked to the first frame the meteor was observed in, 1 to the
             second, etc.
          -  {}: The dictionary contains the data as defined in the
             description of the 'dataarr' property of the class MetRecInfFile.

    """
    # ----------------------------------------------------------------------------------------------
    # Define variables and constants
    # ----------------------------------------------------------------------------------------------
    data = []

    # ----------------------------------------------------------------------------------------------
    # Do the work
    # ----------------------------------------------------------------------------------------------
    # Read all inf file names - from this web page:
    # http://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python
    # Queried 2016-10-05
    matches = []
    for root, _, file_names in os.walk(src):
        for filename in fnmatch.filter(file_names, '*.inf'):
            matches.append(os.path.join(root, filename))

    # Take the trajectory data from the daf files
    for filename in matches:
        inf_file = MetRecInfFile(filename)
        data.append(inf_file.dataarr)

    return data


# --------------------------------------------------------------------------------------------------
# Interface to UFOCapture files from AMOS network
# --------------------------------------------------------------------------------------------------
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
        self.station_position = []

        self.bright = []
        self.right_ascension, self.declination = [], []
        self.c_x, self.c_y, self.c_ra, self.c_dec = [], [], [], []

        xml_file = ET.parse(filename)
        root = xml_file.getroot()

        station = root.attrib
        # Station position: [latitude, longitude, altitude] (degrees, degrees, m)
        self.station_position = [station.get('lng'), station.get('lat'), station.get('alt')]

        self.camera = station.get('clip_name')[17:-1]

        self.appearance_date = (station.get('d').zfill(2) + '.' +
                                station.get('mo').zfill(2) + '.' +
                                station.get('y'))

        self.appearance_time = (station.get('h').zfill(2) + ':' +
                                station.get('m').zfill(2) + ':' +
                                station.get('s'))

        self.start_time_dt = dt.datetime.strptime(self.appearance_date + '-' +
                                                  self.appearance_time,
                                                  '%d.%m.%Y-%H:%M:%S.%f')

        datetime = dt.datetime.strptime(station.get('y') + station.get('mo').zfill(2) +
                                        station.get('d').zfill(2) + station.get('h').zfill(2) +
                                        station.get('m').zfill(2) + station.get('s'),
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

        # for backward compatibility
        self.pos = zip(self.x_pos, self.y_pos)

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
