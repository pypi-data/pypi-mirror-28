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
This module contains all the numerical analysis and conversion routines for
the VMO toolkit.
"""
# disabling the 'eval-used' pylint warning. I know what I'm doing - ignore this.
# pylint: disable=W0123

# disabling the 'invalid-name' pylint warning. It's too awkward for numerical computations.
# pylint: disable=C0103

import os
import glob

from math import floor
from math import sin
from math import asin
from math import cos
from math import tan
from math import atan2
from math import pi

from six import string_types


def evaluate(val):
    """ Attempts to convert the passed value to a float or int, else
    the mighty eval is called.

    :param str val:
    :return: returns the evaluated result
    :rtype: object
    :raises ValueError:
    """
    if not isinstance(val, string_types):
        raise ValueError('expected a str type. val: %s' % repr(val))

    try:
        if '.' in val:
            return float(val)
        else:
            return int(val)
    except ValueError:
        try:
            return eval(val)
        except TypeError as exc:
            # occurs if expr is not a str type
            raise ValueError(str(exc))
        except NameError as exc:
            raise ValueError(str(exc))
        except SyntaxError as exc:
            raise ValueError(str(exc))


def to_rad(deg):
    """ Convert argument from degrees to radians.

    :param float deg:
    :return: the deg argument as radians.
    :rtype: float
    """
    return deg * pi / 180.0


def to_deg(rad):
    """ Convert argument from radians to degrees.

    :param float rad:
    :return: the rad argument as degrees.
    :rtype: float
    """
    return rad * 180.0 / pi


def hour_to_deg(hour):
    """ Convert argument from hours to degrees.

    :param float hour:
    :return: the hour argument as degrees.
    :rtype: float
    """
    return float(hour) * 360.0 / 24.0


def julian_day(year, month, date, hour, minute, second):
    """ Convert a Gregorian Date to the corresponding Julian Day.
    Algorithm taken from 'Astronomical Algorithms', Jean Meeus, p61
    """

    # dt = datetime(year, month, date, hour, minute, second)
    day = float(date) + float(hour)/24 + float(minute)/(24*60) + float(second)/(24*60*60)
    # January and February have to be considered as 13th and 14th month in the algorithm
    if month == 1 or month == 2:
        month += 12
        year -= 1

    A = floor(year / 100.0)
    B = 2.0 - A + floor(A / 4.0)
    jd = floor(365.25 * (year + 4716)) + floor(30.6001 * (month + 1)) + day + B - 1524.5
    return jd


def equ2hor(time_tuple, lon, lat, ra, dec):
    """ Convert equatorial to horizon coordinates

    :param tuple time_tuple: (yyyy, mm, dd, HH, MM, SS)
    :param float lon: in degrees
    :param float lat: in degrees
    :param float ra: in degrees
    :param float dec: in degrees
    :return:
    :rtype: float
    """

    # Greenwich Mean Sidereal Time (Meeus formula 11.4)
    d = julian_day(*time_tuple) - 2451545.0
    T = d / 36525.0
    gmst = 280.46061837 + (360.98564736629 * d) + \
            (0.000387933 * (T**2)) - ((T**3) / 38710000.0)

    # Local Mean Sidereal Time (LMST) in decimal degrees
    lmst = gmst + lon

    # Hour Angle in radians
    hour_angle = to_rad(lmst) - to_rad(ra)
    alt = to_deg(asin(sin(to_rad(lat)) * sin(to_rad(dec)) +
                      cos(to_rad(lat)) * cos(to_rad(dec)) * cos(hour_angle)))
    az = 180.0 + to_deg(atan2(sin(hour_angle),
                              cos(hour_angle) * sin(to_rad(lat)) -
                              tan(to_rad(dec)) * cos(to_rad(lat))))
    return alt, az


def to_file_system_case(path):
    """ Convert the specified file path to the case-corrected file system
    entry. This is only relevant to Window's systems.

    :path str path: the file path that is to be case corrected.
    :return: the path that exactly matches the file in the file system.
    :rtype: str
    """

    def get_ignore_case_pattern(pattern):
        """ Converts the base directory (or file) to an
        none case sensitive patten for use with the glob module.

        :param str pattern:
        :return: the new pattern
        :rtype: str
        """

        def either(char_in):
            """ Translate character to case-insensitive wildcard
            expression. Example: 'a' => '[aA]'
            :param str char_in:
            :return: the 4 character wild card expression.
            :rtype: str
            """
            chars_case = '[%s%s]' % (char_in.lower(), char_in.upper())
            return chars_case if char_in.isalpha() else char_in

        root_dir, base_name = os.path.split(path)
        base_name = ''.join([either(char) for char in base_name])
        pattern = os.path.join(root_dir, base_name)
        return pattern

    path_pattern = get_ignore_case_pattern(path)
    result = glob.glob(path_pattern)
    return result and result[0] or path


def is_close(a, b, rel_tol=1e-09, abs_tol=0.0):
    """ Test if 2 floating point numbers are nearly equal.
    """
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
