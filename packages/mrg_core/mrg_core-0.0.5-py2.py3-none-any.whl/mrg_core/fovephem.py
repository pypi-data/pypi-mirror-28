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
""" Ephemeris calculation for a camera's field of view with respect to the
Sun and Moon rising and setting times.
"""
from __future__ import print_function

import os
import sys
import logging
import argparse
import datetime
import time
import shlex
from io import open

try:
    import ephem
except ImportError:
    print('pip install ephem')
    sys.exit(-1)

from mrg_core.util import fov
from mrg_core.util import config
from mrg_core.mml.metlog import MetLogFile


def execute(opts):
    """
    :param Namespace opts: this is the argparse command line arguments consolidated
        with the arguments the location attributes from the metrec log file and the
        user defined configuration file.
    """
    cam = fov.FOV(latitude=opts.latitude,
                  longitude=opts.longitude,
                  height=opts.height,
                  min_lunar_angle=opts.minLunarAngle,
                  horizon=opts.horizon)

    # if opts.format:
    #     cam.format = opts.format
    #
    if opts.fovEpoch:
        cam.set_equatorial_fov(opts.fovRA, opts.fovDEC, opts.fovEpoch)
    else:
        cam.set_horizontal_fov(opts.fovAzimuth, opts.fovElevation)

    date = ephem.Date(opts.date)
    date_end = ephem.Date(opts.dateEnd)

    cam.compute(date, 30)

    if opts.isCorrected:
        now = datetime.datetime.now()
        if now > cam.sun_set_time.datetime():
            logging.warning('the date correction is being ignored and reset to '
                            'today\'s date, since the current time exceeds the '
                            'sun set time.')
            date = ephem.Date(now)
            cam.compute(date, 30)

    fov_output_types = {
        'csv': fov.FOVOutputCSV,
        'xml': fov.FOVOutputXML,
        'html': fov.FOVOutputHTML,
    }
    formatter = fov_output_types[opts.outputType](cam)

    t_0 = time.clock()

    date0 = date
    while date0 <= date_end:
        gti = cam.compute(date0, 30)
        formatter.process(date0, gti)
        date0 = ephem.Date(date0 + 1)

    t_1 = time.clock()
    logging.debug('Finished processing in %d seconds', (t_1 - t_0))

    if opts.outputDir:
        out_path = os.path.join(opts.outputDir, 'fov.' + opts.outputType)
        with open(out_path, 'w', encoding='utf-8') as file_obj:
            file_obj.write(u'' + formatter.to_string())
    else:
        print(formatter.to_string())

    t_2 = time.clock()
    logging.debug('Finished writing xml file in %d seconds', (t_2 - t_1))


def get_metrec_settings(metrec_log_file, opts):
    """ Load the metrec log session file and parse the header information
    to retrieve the field of view and location settings.

    :param str metrec_log_file: the path to the metrec log file, or None
        to ignore this routine.
    :param Namespace opts: the argparse parser options
    """
    if metrec_log_file:
        logging.debug('Parsing metrec log file: %s', opts.metrec)
        session = MetLogFile(opts.metrec)
        headers = session.header
        time_parts = headers['Reference_date'] + headers['Reference_time']
        opts.fovEpoch = '%04d-%02d-%02d %02d:%02d:%02d' % tuple(time_parts)
        opts.minLunarAngle = str(headers['MinimumLunarDistance'])
        opts.horizon = str(headers['MaximumSolarAltitude'])
        opts.height = str(headers['Altitude'])
        opts.latitude = str(headers['Latitude'])
        opts.longitude = str(headers['Longitude'])
        opts.fovRA = str(headers['Center_of_plate_RA'])
        opts.fovDEC = str(headers['Center_of_plate_DE'])


def translate_settings(opts):
    """ Converts date options if they are set to 'today'. Also
    checks if the dateEnd option is an integer offset.

    :param Namespace opts: the argparse parser options
    """
    try:
        offset = int(opts.dateEnd)
    except ValueError:
        offset = 0
    opts.format = opts.format.replace('\\n', '\n')
    opts.isCorrected = False

    if opts.date == 'today':
        now = datetime.datetime.now()
        if opts.dateCorr > 0:
            if 0 <= now.hour <= opts.dateCorr:
                now = now + datetime.timedelta(days=-1)
                opts.isCorrected = True
        opts.date = now.strftime("%Y/%m/%d")
        opts.dateEnd = opts.date

    if opts.dateEnd == 'today':
        opts.dateEnd = str(datetime.date.today()).replace('-', '/')

    if offset > 0:
        opts.dateEnd = ephem.Date(opts.date) + offset


def main(cmdline):
    """ Entry point of script that handles the command line interface.

    :param str cmdline: optional. Used for debugging.
    """
    parser = argparse.ArgumentParser('Field of View for Sun and Moon')

    parser.add_argument('-c', '--config', dest='config',
                        help='the configuration file to be used if no other parameters '
                             'are provided.')

    group1 = parser.add_argument_group('Observer Options')
    group1.add_argument('-x', '--longitude', dest='longitude',
                        help='The longitude of the observer in "deg:min:sec.dec" format.')
    group1.add_argument('-y', '--latitude', dest='latitude',
                        help='The latitude of the observer in "deg:min:sec.dec" format.')
    group1.add_argument('-z', '--height', dest='height', type=float,
                        help='The height above sea level of the observer in meters.')
    group1.add_argument('-m', '--min-lunar-angle', dest='minLunarAngle', default='90:0',
                        help='the minimum angular distance the moon can reach the camera\'s '
                             'FOV in degrees.')
    group1.add_argument('-r', '--horizon', dest='horizon', default='-0:34',
                        help='the offset horizon angle for which the Sun\'s rising and setting '
                             'times are calculated.')
    group1.add_argument('-d', '--date', dest='date',
                        default='today', help='The date in "yyyy/mm/dd" format.')
    group1.add_argument('-D', '--date-end', dest='dateEnd', default='today',
                        help='The date in "yyyy/mm/dd" format or an integer offset from --date.')
    group1.add_argument('--date-corr', dest='dateCorr', type=int, default=0,
                        help='0=disabled or 1..12. Only used for "today" date. Offsets the '
                             'date by -1 days if the current time is less than the correction '
                             'date hour.')

    group2 = parser.add_argument_group('Field of View Options',
                                       'use either: az+el, or ra+dec+epoch')
    group2.add_argument('--fov-azimuth', dest='fovAzimuth', default='0:0:0',
                        help='the azimuth pointing direction of the camera\'s field of view '
                             'in "deg:min:sec.dec" format.')
    group2.add_argument('--fov-elevation', dest='fovElevation', default='90:0:0',
                        help='the elevation pointing direction of the camera\'s field of view '
                             'in "deg:min:sec.dec" format.')
    group2.add_argument('--fov-epoch', dest='fovEpoch',
                        help='The date that the reference image was taken.')
    group2.add_argument('--fov-ra', dest='fovRA',
                        help='The right ascension of the FOV at rhe given epoch.')
    group2.add_argument('--fov-dec', dest='fovDEC',
                        help='The declination of the FOV at the given epoch.')
    group2.add_argument('--metrec', dest='metrec',
                        help='The metrec configuration file.')

    group3 = parser.add_argument_group('Output Options')
    group3.add_argument('-o', '--output-dir', dest='outputDir',
                        help='The directory to save formatted output to. '
                             'The directory must exist.')
    group3.add_argument('-t', '--output-type', dest='outputType', default='xml',
                        help='The file output format: xml or csv.')
    group3.add_argument('-f', '--format', dest='format', default='# %-15s= %s\n',
                        help='The property listing format.')
    group3.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='Prints lunar trajectory info to the console window.')

    if cmdline:
        cmdline = shlex.split(cmdline)
    opts = parser.parse_args(cmdline)

    logging.basicConfig(level=[logging.WARNING, logging.DEBUG][opts.verbose])

    config.get_settings(opts.config, opts, parser)
    get_metrec_settings(opts.metrec, opts)
    translate_settings(opts)

    if opts.latitude is None:
        logging.error('latitude is not specified.')
    elif opts.longitude is None:
        logging.error('longitude is not specified.')
    else:
        execute(opts)


if __name__ == "__main__":
    # cmdline_in = r'--date 2016/07/18 --verbose 1
    #      --metrec ../tests/unittests/test_data/ICC7/20160215/20160215.log ' \
    #      r'--min-lunar-angle 30 --height 30 --horizon -8 --date-end 10 --output-type csv'
    main(None)
