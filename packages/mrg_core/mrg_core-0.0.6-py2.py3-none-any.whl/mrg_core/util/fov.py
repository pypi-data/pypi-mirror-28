"""
The fov module provides routines to calculate the ephemeris of the Sun and Moon,
and can then determine the "good-time-intervals" for any given observation
night. The method for determining the closest apporach of the Moon is basically
done using a brute force approach. The Sun set and rise times are first
calculated and then the closest approach of the Moon is determined by iterating
over the Sun down period using 1 minute intervals, and calculating the azimuth
and elevation for each minute of it's trajectory. The brute force approach is
very CPU intensive and has been improved by increasing the resolution from 1
minute to 30 minutes and then back tracking when the cross over into the field
of view is occurs.

One of the problems was figuring out how to incorporate the metrec configuration
parameters into this module. A small program was developed named ephemeris.exe
that handles the task of reading in the metrec configuration file, then reading
in the appropriate reference stars configuration, and finally determining the
azimuth and elevation of the field of view. The output of the ephemeris.exe
program is a key = value pair console output that is then piped into the fov.py
program and parsed to determine the new default parameters. These piped metrec
parameters can be overriden using command line parameters.

A second way of incorporating the metrec parameters is to use an existing
metrec log file (that corresponds to the current directional and locational
setup). The metrec log files contain information related to RA and DEC for a
specified Epoch (reference stars date) at the center of the field of view.
This information can be used to calculate the FOV azimuth and elevation for
any given date. This is the prefered way of executing the FOV program. The
reason being is that any modifications made to the metrec code wrt orientation
calculation will automatically be taken into account, this is not the case with
the ephemeris.exe program since it was developed in houseand does not
follow the same development path as metrec.

The FOV schedule can be displayed graphically. The graphical presentation is
done by taking the XML schedule output file and using an XSLT template file to
process the XML nodes and transform them into HTML nodes that can subsequently
be rendered by a browser. The major obstacle to overcome was to NOT use
javascript (due to performance reasons) to position the schedule bars for each
date.

There are a number of different modes of operation that the fov module may be
used. The simplest one is to use the GUI web application with a metrec
configuration file as the basis of the entry parameters.

The steps to start the GUI system up are,
        - start fovserver.py
        - open a browser and navigate to http://localhost:8000
        - modify the entry field and press "Submit"

A command line approach based on a metrec config file would be something like
this,
        - fov.py --metrec c:\\metrec.cfg --date-end 365 --min-lunar-angle=30:0
        - double click on the fov.xml file to view the grapical results.

or a none metrec config file parameter list,
        - fov.py --latitude=52:15:48.2 --longitude=4:29:21.5 --height=10 --fov-azimuth=357:0 ...
                    ... --fov-elevation=58:0 --date-end 365 --min-lunar-angle=30:0
        - double click on the fov.xml file to view the grapical results.


version 1.0 (2010/07/06)
    - initial release

version 1.1 changes (2011/03/14):
    - integrated fov.exe as a replacement for ephemeris.exe. This uses the
    metrec code base as is, which should fix any synchronisation issues when
    new metrec updates are provided.

version 1.2 changes (2011/08/03):
    - introduced the --date-corr switch that enables the current (today's) date
    to be corrected back to yesterday, if the current time is less than
    the --date-corr value. This allows the mrg.exe program to be restarted
    during an observation. Also, if the corrected date's sun set is before the
    current time, than the non-corrected date is used.

@date: 2011/08/03

@version: 1.2

@author: Hans Smit


@todo: Implement better data entry processing. This module now assumes all the
entry fields are in the correct format and are available.

@todo: it seems that changing the observer's altitude (height) do not effect
    the results. Why is this?

"""
from __future__ import print_function

import os
import logging
import sys
import xml.dom.minidom

try:
    from lxml import etree
except ImportError:
    print('pip install lxml')

try:
    import ephem
except ImportError:
    print('pip install ephem')
    sys.exit(-1)


def fix_float(att):
    """ Python 2/3 compatibility fix for str(float). Reference:
    https://github.com/unified-font-object/ufoLib/issues/19
    """
    try:
        att = list(att)
        if isinstance(eval(str(att[1])), float):
            att[1] = repr(att[1])
    except:
        pass
    return att


class FOV(object):
    """
    This class determines the good-time-intervals GTI for the
    camera's field of view FOV. This is the computation back bone of the module
    and the computational work horse is provided by the pyephem module. To
    download this module, following the links provided here:
    U{http://rhodesmill.org/pyephem/}. This module is an easy to use ephermeris
    package that provides a very clean and consistent interface to the
    computation model, and also provides useful conversion functions for
    angles and time.

    Example Usage::
            cam = FOV (
                    longitude='4:51:59.8',
                    latitude='52:21:00.0',
                    height=9,
                    minLunarAngle='5:0:0',
                    horizon='-0:34'
            )
            cam.set_horizontal_fov(az='140:0:0',el='10:0:0')
            cam.date = ephem.Date((2010,6,29,12))
            gti = cam.compute()
            print cam
    """

    def __init__(self, latitude, longitude, height=0, min_lunar_angle='0:0:0', horizon='-0:34'):
        """
        initializer. The angles may be provided as:

                - string '[deg]:[min]:[sec].[decimal]',
                - string '[deg].[decimal]'
                - float [radians].

        @param latitude: the latitude of the observer
        @param longitude: the longitude of the observer
        @param height: the altitude in meters above sea level of
                the observer.
        @param min_lunar_angle: the minimum allowable angle between
                the moon and the fov.
        @param horizon: The horizon attribute defines your horizon,
                the altitude of the upper limb of a body at the moment
                you consider it to be rising and setting. A negative
                value indicates that it is below the observer's 0 deg
                horizon.
        """
        if height is None:
            height = 0

        self._moon = ephem.Moon()
        self._sun = ephem.Sun()

        self._obs = ephem.Observer()
        self._obs.long = ephem.degrees(longitude)
        self._obs.lat = ephem.degrees(latitude)
        self._obs.elev = float(height)
        self._obs.pressure = 0
        self._obs.horizon = ephem.degrees(horizon)
        self._min_lunar_angle = ephem.degrees(min_lunar_angle)
        self._az = ephem.degrees('0:0')
        self._el = ephem.degrees('0:90')
        self._moon_fov_in = 0
        self._moon_fov_out = 0
        self.sun_set_time = None
        self.sun_rise_time = None

    def set_horizontal_fov(self, az_deg_str, el_deg_str):
        """
        Set the camera's fov pointing in azimuth and elevation coordinates.

        Reference: U{http://en.wikipedia.org/wiki/Horizontal_coordinate_system}

        @param az_deg_str: the azimuth angle the camera is pointing
                towards.
        @param el_deg_str: the elevation angle the camera is
                pointing towards.
        """
        self._az = ephem.degrees(az_deg_str)
        self._el = ephem.degrees(el_deg_str)

    def set_equatorial_fov(self, ra_hour_str, dec_deg_str, epoch):
        """
        This method calculates the azimuth and altitude (elevation) of the
        camera's FOV using RA and DEC values for specific time (epoch). The
        metrec refstars application calculates the FOV's RA and DEC at the time
        that the camera images of the sky were acquired.

        Reference: U{http://en.wikipedia.org/wiki/Equatorial_coordinate_system}

        @param ra: the right ascension at the given epoch time. The parameter
                may be formatted in '[HH]:[MM]:[SS.sss]', '[HH.hhh]', or as a
                numeric value in radians.

        @param dec: the declination at the given epoch time. The parameter
                may be formatted in '[deg]:[MM]:[SS.sss]', '[deg.ddd]', or as a
                numeric value in radians.

        @param epoch: the time associated with the RA and DEC parameters. Use
                the 'yyyy/mm/dd HH:MM:SS.sss' format.
        """
        self._obs.date = ephem.Date(epoch)
        camera = ephem.FixedBody()
        setattr(camera, '_ra', ephem.hours(ra_hour_str))
        setattr(camera, '_dec', ephem.degrees(dec_deg_str))
        setattr(camera, '_epoch', ephem.Date(epoch))
        # camera._ra = ephem.hours(ra)
        # camera._dec = ephem.degrees(dec)
        # camera._epoch = ephem.Date(epoch)
        camera.compute(self._obs)
        self.set_horizontal_fov(camera.az, camera.alt)


    @property
    def date(self):
        """
        the date to carry out the calculation on.
        """
        return self._obs.date

    @date.setter
    def date(self, new_date):
        """ set the date """
        self._obs.date = ephem.Date(new_date)
        self.sun_set_time = self._obs.next_setting(self._sun, new_date)
        self.sun_rise_time = self._obs.next_rising(self._sun, self.sun_set_time)
        self._sun.compute(self._obs)
        self._moon.compute(self._obs)

    def compute(self, date=None, resolution=30):
        """
        Computes the GTI (good-time-interval) based on sun rise /
        set and angular approach of the moon. The approach of the
        moon is calculated in one minute intervals, if the angle
        between the moon's az/el and the fov az/el is less than
        the minimum lunar angle than the camera should be turned
        off (non-observing interval).

        @param date: for which the calculations are to be
                determine on. The time of the given date will fast
                forwarded to the sun set time, and the GTI will be
                calculated from this point forward until the following
                day's sun rise occurs.
                NOTE: date argument may be passed as:
                        - a tuple: (2010,6,29,12)
                        - a string: '2010/12/31 23:59:59.123'
                        - a numeric: julian-date. (to be tested).

                if no date is provided then the current observer's date is used.

        @param resolution: the minute interval to scan with. When an event
                is detected, then the coarse scan is back tracked, and a fine
                scan with 1 minute resolution.

        @rtype: array of tuples (date,bool)
        @return: the GTI time and observation transition state array.
        """
        if not date:
            date = self._obs.date

        res_org = resolution
        self.sun_set_time = self._obs.next_setting(self._sun, date)
        self.sun_rise_time = self._obs.next_rising(self._sun, ephem.Date(self.sun_set_time))

        obs_time = self.sun_set_time

        is_on = True
        gti_list = [(ephem.Date(self.sun_set_time), is_on, 'Sun')]

        counter = 0
        logging.debug('Observation time,  sep angle, moon az, moon alt, az, el')

        while obs_time < self.sun_rise_time:
            self._obs.date = obs_time
            self._moon.compute(self._obs)
            angle = ephem.separation(
                (self._moon.az, self._moon.alt),
                (self._az, self._el)
            )
            if (counter % 15) == 0:
                # print every 15th minutes
                logging.debug('%s, %s, %s, %s, %s, %s',
                              ephem.Date(obs_time),
                              repr(ephem.degrees(angle)),
                              repr(self._moon.az),
                              repr(self._moon.alt),
                              repr(self._az),
                              repr(self._el))

            obs_time += ephem.minute * resolution
            toggle = False
            if angle < self._min_lunar_angle:
                if is_on:
                    toggle = True
            else:
                if not is_on:
                    toggle = True

            if toggle and resolution != 1:
                obs_time -= ephem.minute * resolution
                resolution = 1
                toggle = False

            if toggle:
                is_on = not is_on
                obs_time -= ephem.minute * resolution
                gti_list.append((ephem.Date(obs_time), is_on, 'Moon'))
                obs_time += ephem.minute * resolution
                resolution = res_org

            counter += resolution

        gti_list.append((ephem.Date(self.sun_rise_time), False, 'Sun'))

        for gti in gti_list:
            if gti[2] == 'Moon':
                if gti[1]:
                    self._moon_fov_out = gti[0]
                else:
                    self._moon_fov_in = gti[0]

        # recalculate the current date values
        self._obs.date = date
        self._moon.compute(self._obs)

        return gti_list

    @property
    def attributes(self):
        """
        Collects all the provided parameters and calculated attributes based
        on the current observation date.

        @rtype: array
        @return array of (name,value) tuples
        """
        atts = [('Date', self._obs.date,
                 'The date used for the starting calculations.'),
                ('Latitude', self._obs.lat,
                 'The observer\'s latitudinal location'),
                ('Longitude', self._obs.long,
                 'The observer\'s longitudinal location'),
                ('Altitude', self._obs.elev,
                 'The observer\'s height above sea level (meters)'),
                ('Azimuth', self._az,
                 'The camera\'s pointing direction from North to clockwise. (degrees)'),
                ('Elevation', self._el,
                 'The camera\'s pointing direction above the horizon. (degrees)'),
                ('MinLunarAngle', self._min_lunar_angle,
                 'The minimum allowable angular distance from the FOV to the moon. '
                 'This usually corresponds to the FOV angle. (degrees)'),
                ('Horizon', self._obs.horizon,
                 'The MaximumSolarAltitude (degrees)'),
                ('SunSet', self.sun_set_time,
                 'The time that the sun sets'),
                ('SunRise', self.sun_rise_time,
                 'The time that the sun rises'),
                ('MoonPhase', self._moon.phase,
                 'The phase of the moon for the given date.'),
                ('MoonMag', self._moon.mag,
                 'The magnitude of the moon for the given date.'),
                ('MoonRise', self._obs.next_rising(self._moon, self.sun_set_time),
                 'The time the moon rises above the horizon.'),
                ('MoonRiseAZ', self._moon.az,
                 'The azimuth location of where the moon will rise.'),
                ('MoonSet', self._obs.next_setting(self._moon, self.sun_set_time),
                 'The time the moon will set below the horizon.'),
                ('MoonSetAZ', self._moon.az,
                 'The azimuth location of where the moon will set.'),
                ('MoonTrans', self._obs.next_transit(self._moon, self.sun_set_time),
                 'The time the moon will culminate (cross the 180 deg '
                 'meridian and be at it\'s highest point)'),
                ('MoonTransEL', self._moon.alt,
                 'The maximum elevation that the moon will reach when it culminates'),
                ('MoonFovIn', self._moon_fov_in,
                 'The time that the moon approaches the field of view (moves in to FOV).'),
                ('MoonFovOut', self._moon_fov_out,
                 'The time that the moon moves out of the field of view (moves out of FOV).')]
        return atts


class FOVOutputCSV(object):
    """ Class that implements an CSV output format """

    def __init__(self, fov):
        self._str = FOVOutputCSV.get_header(fov)
        return

    @staticmethod
    def get_header(fov, header_format='# %-15s= %s\n'):
        """
        The human readable string representation of this instance.
        The default format is: "# %-15s= %s\\n"
        """
        output = ''
        for att in fov.attributes:
            try:
                att = fix_float(att)
                output += header_format % (att[0], str(att[1]))
            except TypeError as exc:
                logging.error('Could not format (%s): %s, exc: %s',
                              repr(header_format), repr(att), str(exc))
                # logging.exception(exc)
        return output

    def process(self, date, gti):
        """ output the gti event to a string buffer """
        logging.debug('FOVOutputCSV.process %s', str(date))
        for timestamp, is_rising, obj_type in gti:
            self._str += '\n%s, %d, %s' % (str(timestamp), is_rising, obj_type)

    def to_string(self):
        """ return the contents of the buffer """
        return self._str


class FOVOutputXML(object):
    """ Class that implements an XML output format """

    def __init__(self, fov):
        """
        Construct a new FOV output processing helper class. This class is
        uses XML as the output format.

        @param fov: the FOV instance to print the output from.
        """
        doc = xml.dom.minidom.Document()
        # doc.appendChild(
        #     doc.createProcessingInstruction(
        #         'xml-stylesheet',
        #         'type="text/xsl" href="fov.xsl"'
        #     )
        # )
        doc.appendChild(doc.createElement('gti'))
        params = doc.documentElement.appendChild(
            doc.createElement('parameters')
        )

        self._doc = doc
        self._params_node = params

        for item in fov.attributes:
            key = item[0]
            item = fix_float(item)
            val = str(item[1])
            desc = str(item[2])
            self.add_parameter(key, val, desc)

    def add_parameter(self, key, val, desc=''):
        """  Appends a <param> element to the document root.

        :param str key:
        :param str val:
        :param str desc:
        """
        param = self._params_node.appendChild(self._doc.createElement('param'))
        param.setAttribute('name', key)
        param.setAttribute('value', val)
        param.appendChild(self._doc.createTextNode(desc))

    def process(self, date, gti):
        """ The good time intervals for a given date is processed here.

        @param date: an ephem.Date object
        @param gti: an array of GTI object
        """
        doc = self._doc
        date_node = doc.documentElement.appendChild(doc.createElement('date'))
        yyyymmdd = date.tuple()
        date_node.setAttribute('id', '%04d-%02d-%02d' % (yyyymmdd[0], yyyymmdd[1], yyyymmdd[2]))
        date_node.setAttribute('date', '%02d' % yyyymmdd[2])
        for interval in gti:
            timestamp = interval[0].tuple()
            state = interval[1]
            interval_type = interval[2]
            evt_node = doc.createElement('event')
            evt_node.setAttribute('state', str(state))
            evt_node.setAttribute('hh', '%02d' % timestamp[3])
            evt_node.setAttribute('mm', '%02d' % timestamp[4])
            evt_node.setAttribute('type', interval_type)
            evt_node.setAttribute('date', '%04d-%02d-%02d' % (timestamp[0],
                                                              timestamp[1],
                                                              timestamp[2]))
            date_node.appendChild(evt_node)

    def to_string(self):
        """ Output the XML DOM to string format. """
        return self._doc.toxml(encoding='utf-8').decode('utf-8')
        # return self._doc.toprettyxml()


class FOVOutputHTML(FOVOutputXML):
    """ Class that implements an HTML output format """

    def __init__(self, fov, fov_xsl_file=None, params=None):
        if fov_xsl_file is None:
            cwd_dir = os.path.dirname(os.path.realpath(__file__))
            fov_xsl_file = os.path.join(cwd_dir, 'fov.xsl')
        self._xsl = fov_xsl_file
        self._str = None
        self._params = params
        super(FOVOutputHTML, self).__init__(fov)

    def to_string(self):
        """ return the contents of the buffer """

        # output the gti event to a string buffer
        xslt_params = {}
        if self._params:
            for key, val in self._params.items():
                xslt_params[key] = etree.XSLT.strparam(val)

        # f = open(xmlFile, "rt")
        # xmlDoc = etree.parse(f)
        # f.close()
        html = self._doc.toxml()
        xml_doc = etree.fromstring(html)

        with open(self._xsl) as file_obj:
            xsl_doc = etree.parse(file_obj)

        xslt = etree.XSLT(xsl_doc)
        htm_doc = xslt(xml_doc, **xslt_params)
        self._str = etree.tostring(htm_doc,
                                   encoding='utf-8',
                                   pretty_print=True,
                                   xml_declaration=True)
        return self._str.decode('utf-8')

