# File: mots_astro.py
#
#   Version History
#   --------------------------------------------------------------------------
#   v3.0, 03 Aug 2014, dvk: Taken over from Geert, updated formatting
#   v3.1, 03 Dec 2015, dvk: geo2xyz: Updated header, longitude and latitude
#                           were wrongly described in the text field (the
#                           formulae are correct).
#   v3.2, 01 Aug 2016, dvk: Updated first half of comment fields to better
#                           Sphinx standard following Hans' convention.
#   v3.3, 06 Aug 2016, jdr: Updates to match PEP8 requirements.
#   v3.4, 09 Aug 2016, dvk: Fixed hor2equ
#   v3.5, 16 Sep 2016, jdr: pylint fixes. Removed datetime from the import
#                           modules. Updated the math to use numpy. Changed
#                           Exception by ValueError in the delta_lon routine.
#   v3.6, 18 Sep 2016, jdr: Completed the migration from math to numpy.
#   v3.7, 29 Dec 2016, jdr: Improved documentation formatting for compliance
#                           to numpydocs.  Added logging capabilities to
#                           the module.

"""
MOTS Celestial mechanics module.

Notes
-----
1. All angle arguments in decimal degrees, not radians!

2. A lot of this could be done in SPICE - to stay independent of external
   routines we re-implemented a lot of stuff here.

NOTE: There are a couple of duplications! Jorge should clean this up...

   julian day routine(s):
      mots_astro.jd(mydate)
      convert.julian_day(year, month, date, hore, minute, second)

   equatorial to horizontal conversion routine(s):
      mots_astro.equ2hor(equ, geo, mytime)
      convert.equ2hor(time_tuple, lon, lat, ra, dec)

Not sure how these routines ended up in 'convert.py' - a number of others
are not there! i suggest: Keep all the 'astro' stuff here, including
coordinate conversions. In the end this file can be replaced with SPICE
routines (dvk).

"""
# ----------------------------------------------------------------------------
# Import required Python modules and functions
# ----------------------------------------------------------------------------
import logging

from numpy.linalg import norm
from numpy import random
import numpy as np


def julian_day(utc_time):
    """
    Convert Gregorian date/time in Universal Time Coordinated to Julian Day.

    This is the number of days since Greenwich noon of 01 January 4713 B.C.
    Algorithm from 'Astronomical Algorithms', Jean Meeus, p. 61.

    Parameters
    ----------
    utc_time: datetime
       is the input date and time in UTC to be converted to Julian Day.

    Returns
    -------
    float
       Decimal julian day corresponding to the input time ``utc_time``.

    Examples
    --------
    >>> import datetime
    >>> julian_day(datetime.datetime(2000, 1, 1, 12, 0, 0))
        2451545.0
    >>> julian_day(datetime.datetime(2000, 1, 1, 12, 0, 0, int(1E5)))
        2451545.0000011576

    Notes
    -----
    This routine has the following limitations:
       1. Due to the implementation of the input time as a datetime object, the
          earliest date that can be converted is 1 January 1 A.C at midnight
          UTC, i.e. 1-JAN-1T00:00:00.

    """
    # Get the day expressed as a decimal number
    year = utc_time.year
    month = utc_time.month
    day = utc_time.day
    day += (utc_time.hour / 24.0)
    day += (utc_time.minute / 1440.0)
    day += (utc_time.second + (utc_time.microsecond / 1E6)) / 86400.0

    #
    # In this algorithm, January and February have to be considered as
    # "13th and 14th month"
    #
    if month == 1 or month == 2:
        month += 12
        year -= 1

    #
    # Calculate the correction factor between the Gregorian Calendar (UTC)
    # and the Julian calendar.
    #
    century = np.floor(year / 100.0)
    greg2jul_factor = 2 - century + np.floor(century / 4.0)

    #
    # Calculate the Julian day
    #
    jday = np.floor(365.25 * (year + 4716)) + \
           np.floor(30.6001 * (month + 1)) + \
           day + greg2jul_factor - 1524.5

    return jday


def gmst(utc_time):
    """
    Get the Greenwich Mean Sidereal Time (GMST) for a given date/time in UT.

    The GMST is the "sidereal time" at zero degrees longitude; "sidereal time"
    is the hour angle of the vernal point. This concept can can be understood
    as the right ascension of the meridian (the line going through
    north-zenith-south); i.e. the orientation of the stars with respect
    to the Earth axis.

    Uses formula 11.4 from Astronomical Algorithms by Jean Meeus.

    Parameters
    ----------
    utc_time : datetime
       Date and time in UT to convert to GMST.

    Returns
    -------
    float
       Greenwich Mean Sidereal Time expressed in degrees.

    Examples
    --------
    >>> import datetime
    >>> gmst(datetime.datetime(1984, 4, 28, 13, 15, 25))
        -2066704.4504038128

    """
    #
    # Compute the number of Julian days from the J2000 reference epoch
    # (2000-01-01T12:00:00 UTC), and the number of Julian years since
    # that epoch (variable named 'T' in chapter 11 of the Astronomical
    # Algorithms)
    #
    days = julian_day(utc_time) - 2451545.0
    years = days / 36525.0

    #
    # Greenwich Mean Sidereal Time (Meeus formula 11.4) already in degrees.
    #
    gmst_val = 280.46061837 + (360.98564736629 * days) \
               + (0.000387933 * pow(years, 2)) - (pow(years, 3) / 38710000.0)

    return gmst_val


def lmst(utc_time, longitude):
    """
    Convert a date/time and an earth longitude to the corresponding Local Mean
    Sidereal Time (LMST) in decimal degrees

    Algorithm from "Astronomical Algorithms", Jean Meeus.

    Parameters
    ----------
    utc_time : datetime
       is the requested input date in UTC.

    longitude : float
       is the Earth longitude in decimal degrees east.

    Returns
    -------
    float
       local mean sidereal time

    Examples
    --------
    >>> import datetime
    >>> date = datetime.datetime(2000, 1, 1, 12, 0, 0)
    >>> lmst(date, 0.00)
        280.46061837

    References
    ----------
    .. [1] "Astronomical Algorithms," Jean Meeus, 1991. ISBN 0-943396-35-2

    """
    return gmst(utc_time) + longitude


def equ2hor(equ, geo, utc_time):
    """
    Returns the altitude and azimuth of a given point in the sky.

    This is returned as equatorial coordinates in decimal degrees.
    For the altitude, the horizon is 0 degrees and zenith is 90 degrees.
    For azimuth, north is 0 degrees and south is 180 degrees.

    Algorithm taken from "Astronomical Algorithms" by Jean Meeus, p.89

    Parameters
    ----------
    equ : numpy.array
       2-dimensional vector containing the equatorial sky coordinates
       [RA, Dec] in degrees.

    geo : numpy.array
       3-dimensional vector containing the geographical geodetic earth
       coordinates for the observing location [lon, lat, height] in
       degrees and meters.

    utc_time : datetime
       date and time in UTC.

    Returns
    -------
    numpy.array
        Returns the altitude (elevation) and azimuth coordinates of
        the input point ``equ`` as seen from the observing location
        ``geo``, in degrees: Altitude ranges from 0.00 (horizon) to
        90.00 degrees (zenith), while azimuth is 0.00 (north), 90.00
        (east), 180.00 (south) and 270.00 (west).

    Examples
    --------
    >>> import datetime
    >>> date = datetime.datetime(2008, 7, 4, 23, 45, 5)
    >>> equ2hor([12.3, 34.5], [1.2, 3.4, 5.6], date)
        array([0.7076025, 55.47856732])

    """
    #
    # Convert declination and latitude from degrees to radians.
    #
    dec = np.radians(equ[1])
    lat = np.radians(geo[1])

    #
    # This is the right ascension of the local meridian line
    # (north-zenith-south), i.e. the local mean siderial time at the
    # input longitude (geo[0]), in the format of hour angle in
    # radians:
    #
    #   h_angle = lmst(utc, lon) - RA
    #
    hour_angle = np.radians(lmst(utc_time, geo[0]) - equ[0])

    #
    # Get the Elevation (altitude) in degrees
    #
    elevation = np.degrees(np.arcsin(np.sin(lat) * np.sin(dec) +
                                     np.cos(lat) * np.cos(dec) *
                                     np.cos(hour_angle)))

    #
    # Get the Azimuth in degrees
    #
    azimuth = 180.0 + np.degrees(np.arctan2(np.sin(hour_angle),
                                            np.cos(hour_angle) * np.sin(lat) -
                                            np.tan(dec) * np.cos(lat)))

    return np.array([elevation, azimuth])


def hor2equ(hor, geo, utc_time):
    """
    Returns the equatorial coordinates for a point in the sky expressed in
    horizontal coordinates (Azimuth north = 0 degrees!)

    Algorithm taken from "Astronomical Algorithms" by Jean Meeus, p.89.

    Parameters
    ----------
    hor: numpy.array
       2-dimensional float precision array describing the horizontal
       coordinates [altitude, azimuth] in degrees: For altitude: horizon = 0
       and zenith = 90.  For azimuth: north = 0, east = 90, etc.
    geo: numpy.array
       3-dimensional float precision array describing the geographical
       earth coordinates [lon,lat] in degrees (east and north are positive
       values, west and south are negative)
    utc_time: datetime
       Input time in UTC

    Returns
    -------
    numpy.array
       2-dimensional array containing the equatorial coordinates
       [right ascension, declination], in degrees, of the input point ``hor``.

    Examples
    --------
    >>> import datetime
    >>> date = datetime.datetime(2008, 7, 4, 23, 45, 5)
    >>> hor2equ([0.707602498, 55.4785673164], [1.2, 3.4, 5.6], date)
    array([12.3, 34.5])

    """
    #
    # Convert the input elevation (altitude), azimuth and latitude to
    # radians.
    #
    alt = np.radians(hor[0])
    azimuth = np.radians(hor[1] - 180.0)
    lat = np.radians(geo[1])

    #
    # Get the right ascension using the following formula:
    #
    #   ra = lmst(utc, lon) - hour_angle
    #
    lms_time = lmst(utc_time, geo[0])
    h_angle = np.arctan2(np.sin(azimuth),
                         np.cos(azimuth) * np.sin(lat) +
                         np.tan(alt) * np.cos(lat))
    right_ascension = lms_time - np.degrees(h_angle)

    #
    # Right ascension should be between 0 and 360. degrees
    #
    if right_ascension < 0.0 or right_ascension > 360.0:
        right_ascension -= np.floor(right_ascension/360.)*360.

    dec = np.arcsin(np.sin(lat) * np.sin(alt) -
                    np.cos(lat) * np.cos(alt) * np.cos(azimuth))

    result = np.array([right_ascension, np.degrees(dec)])
    return result


def equ2xyz(equ):
    """
    Convert equatorial coords (dec deg) to XYZ geocentric coordinates
    (length = unit vector)

    Parameters
    ----------
    equ : numpy.array
       2-dimensional float precision array containing the input point in
       equatorial coordinates [right ascension, declination] in degrees,
       using an undefined equinox (the selection of equinox by the user
       is independent from the mathematical conversion performed by this
       routine).

    Returns
    -------
    numpy.array
        3-dimensional float precision array containing a vector with the
        geocentric coordinates [x, y, z] of the input point ``equ``. This
        vector has unit length and no units.

    Examples
    --------
    >>> import numpy
    >>> equ2xyz([10.0, 20].0)
        array([0.92541658, 0.16317591, 0.34202014])
    >>> equ2xyz([numpy.degrees(0.6), numpy.degrees(0.8)])
        array([0.57501686, 0.39339020, 0.71735609])
    >>> equ2xyz([numpy.degrees(0.6), numpy.degrees(-0.8)])
        array([0.57501686, 0.3933902, -0.71735609])
    >>> equ2xyz([numpy.degrees(5.4), numpy.degrees(2.14)])
        array([-0.34207499,  0.41649027,  0.84233043])

    """
    #
    # Convert input right ascension and declination to radians.
    #
    right_ascension = np.radians(equ[0])
    declination = np.radians(equ[1])

    result = np.array([np.cos(declination) * np.cos(right_ascension),
                       np.cos(declination) * np.sin(right_ascension),
                       np.sin(declination)])
    return result


def xyz2equ(xyz):
    """
    Converts XYZ geocentric coordinates to equatorial coordinates

    Parameters
    ----------
    xyz : numpy.array
       3-dimensional float precision vector containing the geocentric
       coordinates [x,y,z]

    Returns
    -------
    numpy.array
       2-dimensional float precision vector containing the equatorial
       coordinates [right ascension, declination] in degrees.

    Examples
    --------
    >>> xyz2equ([0.92541658, 0.16317591, 0.34202014])
        array([9.99999991, 19.99999979])
    >>> xyz2equ(equ2xyz([20.0,5.0]))
        array([20.0, 5.0])
    """
    xyz /= norm(xyz)

    right_ascension = np.degrees(np.arctan2(xyz[1], xyz[0]))
    declination = np.degrees(np.arcsin(xyz[2]))

    #
    # Right ascension should be in the [0,360) range.
    #
    right_ascension %= 360.0

    return np.array([right_ascension, declination])


def detic2centric(detic):
    """
    Convert geodetic (maps, WGS84) to geocentric (spherical; astronomical)
    earth coordinates, this will only affect the latitude.

    Parameters
    ----------
    numpy.array
       3-diminesional float precision array containing the geodetic
       coordinates of the input point [longitude, latitude, altitude] in
       degrees and meters. Longitude is measured positive towards the East
       and its range is [-180.0, 180.0] degrees. Latitude is measured
       positive towards North, and its range is [-90.0, 90.0] degrees.
       Altitude (also known as height) is measured over the reference
       ellipsoid.

    Returns
    -------
    numpy.array
       3-dimensional float precision array containing the geocentric
       coordinates of the input point [longitude, latitude, height] in
       degrees and meters.

    Examples
    --------
    >>> detic2centric([5.1234, 50.1234, 100.0])
        array ([5.1234, 49.9339326, 100.0])

    """

    #
    # Local parameters.
    #
    # Radius of the Earth at equator and at pole, in meters.
    # (from WGS84 parameters)
    #
    radius_equ = 6378137.0
    radius_pole = 6356752.314

    #
    # Compute the geocentric latitude
    #
    lat = np.arctan((pow(radius_pole, 2) / pow(radius_equ, 2)) *
                    np.tan(np.radians(detic[1])))

    #
    # Convert geocentric latitude to degrees. Longitude and height do not
    # change.
    #
    return np.array([detic[0], np.degrees(lat), detic[2]])


def centric2detic(centric):
    """
    Convert geocentric to geodetic Earth coordinates.

    Convert geocentric (also known as latitudinal, spherical or astronomical)
    to geodetic (maps, WGS84) earth coordinates. Note that this will only
    affect the latitude.

    Parameters
    ----------
    centric : numpy.array
       3-dimensional float precision array containing the geocentric
       coordinates [longitude, latitude, radius], in degrees and meters,
       of a point on the Earth.

    Returns
    -------
    numpy.array
       3-dimensional float precision array containing the geodetic
       coordinates [longitude, latitude, radius], in degrees and meters,
       of the ``centric`` input point.

    Examples
    --------
    >>> centric2detic([10,20,30])
        array([10.000, 20.12400657, 30.000])
    >>> centric2detic([-5.123, 51.456, 100.0])
        array([-5.123, 51.64341707, 100.0])

    """
    #
    # WGS84 parameters: Radii of the Earth (equator and pole) in meters.
    #
    radius_equ = 6378137.0
    radius_pole = 6356752.314

    lat = np.arctan((pow(radius_equ, 2) / pow(radius_pole, 2)) *
                    np.tan(np.radians(centric[1])))

    #
    # Create the output 3-dimensional numpy.array and convert the
    # geodetic latitude to degrees.
    #
    detic = np.array([centric[0], np.degrees(lat), centric[2]])

    return detic


def radius_earth(latitude):
    """
    Returns the radius of the earth for a given GEOCENTRIC latitude.

    The Earth is modeled as a rotational ellipsoid, with the equatorial and
    polar radii being taken from WGS84

    Parameters
    ----------
    latitude : float
       Float precision number giving a Geocentric latitude in decimal degrees.
       Latitude is measured positive towards the North.

    Returns
    -------
    float
       Float precision number giving the Earth radius at the input ``latitude``
       in meters.

    Examples
    --------
    >>> radius_earth(50.1234)
        6365516.5442940332
    >>> radius_earth(0.0)
        6378137.0
    >>> radius_earth(-90.0)
        6356752.314
    """

    #
    # Convert input latitude to radians
    #
    lat = np.radians(latitude)

    #
    # Radius of the Earth at the equator and pole, in meters, taken from
    # the WGS84 parameters.
    #
    radius_equ = 6378137.0
    radius_pole = 6356752.314

    radius = np.sqrt(((pow(radius_equ, 2) - pow(radius_pole, 2)) /
                      (pow((radius_equ/radius_pole) * np.tan(lat), 2) + 1))
                     + pow(radius_pole, 2))
    return radius


def geo2xyz(geodetic, utc_time):
    """
    Convert geodetic geographical coordinates (WGS84 system) to the XYZ
    orthogonal non-rotating geocentric coordinates (meter) defined as follows:

       -  The x-axis is in the equatorial plane of the Earth, pointing towards
          vernal equinox;

       -  The z-axis is going through the centre of the Earth and the North
          Pole, aligned with the Earth rotational axis;

       -  The y-axis completes the right-handed coordinate system;

       -  The origin is the center of mass of the Earth.


    Parameters
    ----------
    geodetic : numpy.array
       3-dimensional float precision array containing the geodetic
       geographical coordinates [longitude, latitude, height] of a given
       point on the Earth, referred to the WGS84 system. Angles are in
       degrees, distances in meters.

    utc_time : datetime
       Input UTC time.

    Returns
    -------
    numpy.array
       3-dimensional float precision array containing a vector [x, y, z] with
       the Cartesian coordinates of the input point ``geodetic``, in meters.

    Examples
    --------
    >>> import datetime
    >>> date = datetime.datetime(2009, 4, 1, 20, 30, 40)
    >>> geo2xyz([5.1234, 51.456, 120.3], date)
        array([-3185497.79488643, 2390259.0192752 , 4965407.41821367])
    >>> date = datetime.datetime(1972, 2, 28, 4, 30, 40)
    >>> geo2xyz([-13.1234, -21.456, -5.3], date)
        array([-5055593.98867633, -3116098.69270354, -2318455.50442173])
    """

    #
    # Get the Earth longitude corresponding to the LMST at the input
    # utc_time, in radians.
    #
    lmst_lon = np.radians(lmst(utc_time, geodetic[0]))

    #
    # Convert geodetic to geocentric coordinates
    #
    geocentric = detic2centric(geodetic)

    #
    # Get the Earth radius at the computed geocentric latitude
    #
    radius = radius_earth(geocentric[1])

    #
    # Convert the geocentric latitude to radians
    #
    lat = np.radians(geocentric[1])

    #
    # Convert the geocentric coordinates to Cartesian coordinates.
    #
    xyz = np.array([
        (radius + geocentric[2]) * np.cos(lat) * np.cos(lmst_lon),
        (radius + geocentric[2]) * np.cos(lat) * np.sin(lmst_lon),
        (radius + geocentric[2]) * np.sin(lat)
    ])

    return xyz


def xyz2geo(rectan, utc_time):
    """
    Returns spherical geodetic geographical coordinates (WGS84 system)
    from orthogonal inertial xyz-coordinates

    Parameters
    ----------
    rectan : numpy.array
       3-dimensional float precision geocentric Cartesian [x, y, z]
       coordinates in meters.

    utc_time : datetime
       Input time in UTC.

    Returns
    -------
    numpy.array
       3-dimensional float precision vector containing the geodetic
       [lon, lat, height] coordinates (degrees, degrees, meters) in WGS84

    Examples
    --------
    >>> import datetime
    >>> import numpy
    >>> date = datetime.datetime(2009, 8, 12, 0, 0)
    >>> position = numpy.array([20920.5267177, -23234.598789, -50034.8376732])
    >>> xyz2geo(position, date)
        array([-8.57570131, -58.1726947, -6303735.71])
    >>> date = datetime.datetime(2009, 4, 1, 12, 12, 12)
    >>> xyz2geo(geo2xyz([10.0, 20.0, 30.0], date), date)
        array([10.0, 20.0, 30.0])

    """

    #
    # Get the length of the input cartesian vector
    #
    length = norm(rectan)

    #
    # Compute geocentric coordinates
    #
    geocentric = np.zeros(3)
    geocentric[0] = np.degrees(np.arctan2(rectan[1], rectan[0])) - \
                    gmst(utc_time)
    geocentric[1] = np.degrees(np.arcsin(rectan[2] / length))
    geocentric[2] = length - radius_earth(geocentric[1])

    #
    # Convert to geodetic coordinates
    #
    geodetic = centric2detic(geocentric)

    #
    # Normalize the longitude!
    #
    geodetic[0] %= 360.0

    if geodetic[0] > 180.0:
        geodetic[0] -= 360.0

    return geodetic


def sphere_distance(equ1, equ2):
    """
    Returns the great-circle distance between two points on a sphere,
    using the "Haversine" formula.

    Parameters
    ----------
    equ1 : numpy.array
       2-dimensional float precision array containing the spherical
       coordinates in degrees of the first point. These spherical coordinates
       may correspond to either [right ascension, declination] or
       [longitude, latitude].

    equ2 : numpy.array
       2-dimensional float precision array containing the spherical
       coordinates in degrees of the second point. These spherical coordinates
       may correspond to either [right ascension, declination] or
       [longitude, latitude].

    Returns
    -------
    float
       Float precision number giving great-circle distance between ``equ1``
       and ``equ2`` in degrees.

    Examples
    --------
    >>> sphere_distance([0.0, 0.0], [0.0, 0.0])
        0.0
    >>> sphere_distance([0.0, 0.0], [0.0, 90.0])
        90.0
    >>> sphere_distance([-90.0, 0.0], [0.0, 90.0])
        90.0
    >>> sphere_distance([-1.5, 50.5], [1.5, 52.5])
        2.7359091499035597
    >>> sphere_distance([0.0, 1.0/3600.0], [1.0/3600.0, 0.0])
        0.00039283710065842365
    """
    #
    # Convert input latitudes to radians
    #
    lat_1 = np.radians(equ1[1])
    lat_2 = np.radians(equ2[1])

    #
    # Get the differences between the longitudes and latitudes,
    # in radians.
    #
    d_lon = np.radians(equ2[0] - equ1[0])
    d_lat = lat_2 - lat_1

    #
    # Compute the angular separation between the two points.
    #
    angle = np.sin(d_lat/2.0)**2.0 + \
            np.cos(lat_1) * np.cos(lat_2) * np.sin(d_lon/2.0)**2.0

    #
    # Compute the great circle distance corresponding to the obtained angle.
    #
    result = 2.0 * np.arctan2(np.sqrt(angle), np.sqrt(1.0 - angle))

    return np.degrees(result)


def delta_lon(sph_dist, lat1, lat2):
    """
    Return the difference in longitude given the spherical distance between
    two points and their latitudes.

    Given a spherical distance and two latitudes, return the corresponding
    difference in longitude, this is useful to put a point at an exact
    distance from another point (e.g. used to simulate errors).

    Parameters
    ----------
    sph_dist : float
       Spherical distance between two points, in degrees.

    lat1 : float
       Latitude of the first point, in degrees.

    lat2: float
       Latitude of the second point, in degrees.

    Returns
    -------
    float
       Difference in longitude between the first point and second point.

    Raises
    ------
    ValueError
       if the Harversine formula returns a value that is not between 0
       and 1, i.e. if it is not possible to obtain the distance between
       the two input latitudes.

    Examples
    --------
    >>> delta_lon(1.0, 0.0, 0.0)
        1.0
    >>> delta_lon(10.0, 20.0, 30.0)
        0.0
    >>> dlon = delta_lon(10.0, 29.0, 30.0)
    >>> round(sphere_distance([5.0, 29.0], [5.0 + dlon, 30.0]), 7)
        10.0
    >>> dlon = delta_lon(60.0, 49.0, 55.0)
    >>> round(sphere_distance([5.0, 49.0], [5.0 + dlon, 55.0]), 7)
        60.0

    Notes
    -----
    The Harversine formula is an approximation when applied to the Earth,
    which is not a perfect sphere. The Earth radius varies from the equator
    to the poles. In addition, the radius of curvature of a north-south
    line on Earth's surface is approximately 1% greated at the poles than
    at the equator, so the Harversine formula has a minimum error of
    0.5%.

    """

    #
    # The difference in longitude needs to take latitude into account as we
    # are on a sphere. The formula below is derived from the Haversine formula
    # which relates spherical coordinates to great circle distance.
    #
    haversine = (np.sin(np.radians(sph_dist) / 2.0)**2.0 -
                 np.sin(np.radians(lat2 - lat1)/2.0)**2.0) / \
                (np.cos(np.radians(lat1)) *
                 np.cos(np.radians(lat2)))

    if -1e-20 < haversine < 0.0:
        # Special case to avoid crash: rounding errors may cause negative
        # numbers close to 0
        lon_difference = 0.0
    elif haversine < 0:
        # Impossible input!
        # delta_lon = None
        msg = "Impossible to get distance {0} between lat {1} and lat {2}: " \
              "d_lon > 180 deg.".format(sph_dist, lat1, lat2)
        logging.error(msg)
        raise ValueError(msg)
    else:
        if haversine > 1:
            # Delta lon larger than 180
            # delta_lon = None
            msg = "Impossible to get distance {0} between lat {1} and lat " \
                  "{2}: d_lon < -180 deg.".format(sph_dist, lat1, lat2)
            logging.error(msg)
            raise ValueError(msg)
        else:
            lon_difference = \
               2.0 * np.arctan2(np.sqrt(haversine),
                                np.sqrt(1.0 - haversine))

    #
    # Return the longitude difference in degrees.
    #
    return np.degrees(lon_difference)


def equ_disturb(equ, error_deg, direction="random"):
    """
    Disturb equatorial coordinates with a certain error (great circle distance)
    in a random or given direction (clockwise; north=0, east=90, ...)

    Parameters
    ----------
    equ : numpy.array
       2-dimensional float precision array containing the equatorial
       coordinates [right ascension, declination] in decimal degrees.

    error_deg : float
       Error to be introduced in degrees.

    direction : float
       Direction in degrees to introduce the error (clockwise; north=0,
       east=90, ...)

    Returns
    -------
    numpy.array
       2-dimensional float precision array containing the disturbed equatorial
       coordinates [right ascension, declination] in decimal degrees.

    Examples
    --------
    >>> disturbance = equ_disturb([10.0, 89.0], 0.1)
    >>> round(sphere_distance([10.0, 89.0], disturbance), 7)
        0.10000000000000001
    >>> disturbance = equ_disturb([60.0, 20.2], 0.01)
    >>> round(sphere_distance([60.0, 20.2], disturbance), 7)
        0.01
    >>> equ_disturb([20.0,30.0], 1.0, 270.0)
        array([ 20.0, 29.0])

    """
    if direction == "random":
        direction = random.uniform(0, 360.0)

    #
    # The error in declination is straightforward
    #
    e_dec = np.sin(np.radians(direction)) * error_deg
    if 90 < direction < 270.0:
        e_dec = -e_dec

    #
    # The error in right ascension needs to take declination into account,
    # since it is computed on a sphere.
    #
    e_ra = delta_lon(error_deg, equ[1], equ[1] + e_dec)
    if 90 < direction < 270.0:
        e_ra = -e_ra

    #
    # Return the disturbed coordinates
    #
    return np.array([equ[0] + e_ra, equ[1] + e_dec])
