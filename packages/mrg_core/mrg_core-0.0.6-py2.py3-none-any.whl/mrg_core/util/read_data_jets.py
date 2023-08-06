"""
   Module for reading DAF files in a format required by the analysis software
   for determination of flux density as written by Jana, Esther, Theresa and
   Sandra (JETS).
"""
# ----------------------------------------------------------------------------------------------
# Import required libraries
#  ----------------------------------------------------------------------------------------------
import logging
import os

import numpy as np

import mrg.analysis.mots3.mots3_testroutine as mots_ex


# ----------------------------------------------------------------------------------------------
# Define needed routines - these should go to the 'util' directory, e.g. in astro.py. To be
# checked
# ----------------------------------------------------------------------------------------------
def lon_lat_dist(lon1, lon2, lat1, lat2):
    """
    Returns the distance between two points from the geodetic coordinates
    given in meters. Also returns flags to indicate whether the meteor was
    moving from west to east/north to south (or the other way).

    :param float lon1: Geodetic longitude of the first point.
    :param float lon2: Geodetic longitude of the second point.
    :param float lat1: Geodetic latitude of the first point.
    :param float lat2: Geodetic latitude of the first point.

    :return: Distance between two points from their geodetic coordinates, given
             in meters, a flag that indicates whether the meteor was moving
             from West to East or the other way, and a flag that indicates
             whether the meteor was flying from North to Sourth (or other way).
    :rtype: tuple

    """

    west_to_east = -1
    north_to_south = -1

    # compare the position of the lon of both cameras to check e to w or w to e
    # if lon1 < lon2 ->  E to W (west_to_east bleibt -1)
    if (abs(lon2) - abs(lon1)) < 0:
        west_to_east = 1

    # compare pos of lat to check N to S or S to N
    # if lat1 < lat2 -> S to N (north_to south bleibt -1)
    if (abs(lat2) - abs(lat1)) < 0:
        north_to_south = 1

    # calculate and define values in radians:
    dlon = np.deg2rad(lon2 - lon1)
    dlat = np.deg2rad(lat2 - lat1)
    lat1 = np.deg2rad(lat1)
    lat2 = np.deg2rad(lat2)

    radius_earth = 6371000.      # Earth radius in m

    angle = abs((np.sin(dlat / 2))**2 + np.cos(lat1) * np.cos(lat2) * (np.sin(dlon/2))**2)
    haversine = 2 * np.arcsin(min(1, np.sqrt(angle)))
    dist = radius_earth * haversine

    return dist, west_to_east, north_to_south


def save_time_absmag_2matrix(time, magnitude, x_pos, y_pos, abs_error):
    """
    Returns an Nx6 matrix with the time, intensity, x-position, y-position,
    error in the intensity computation and absolute magnitude from the input
    ``time``, ``magnitude``, ``x_pos``, ``y_pos`` and ``abs_error`` values.

    :param ndarray time:
    :param ndarray magnitude:
    :param ndarray x_pos:
    :param ndarray y_pos:
    :param ndarray abs_error:
    :return: Nx6 matrix with the time, intensity, x-position, y-position,
             error in the intensity computation and absolute magnitude.
    :rtype: ndarray
    """
    # Save all time and absolute magnitude values are saved in
    # a matrix tim_ma_val_1 for ICC7 detections and
    # tim_ma_val_2 for ICC9 detections

    tim_ma_val = np.zeros((len(time), 6))

    for row, time_value in enumerate(time):
        # tim_ma_val = np.zeros((len(timevalues),2))

        tim_ma_val[row, 0] = time_value

        # calculate intensity using the absolute magnitude
        tim_ma_val[row, 1] = 525. * 10 ** (-0.4 * magnitude[row])
        tim_ma_val[row, 2] = x_pos[row]
        tim_ma_val[row, 3] = y_pos[row]
        # tim_ma_val_1[i, 4] = 0.9210340372*abs[i] * 0.3981071706**magnvalues[i]
        # calculate error of the intensity
        tim_ma_val[row, 4] = abs(-0.4 * 525. *
                                 10 ** (-0.4 * magnitude[row]) *
                                 np.log(10)) * abs_error[row]
        tim_ma_val[row, 5] = magnitude[row]

    return tim_ma_val


def parse_data_line(line):
    """
    Returns the time, absolute magnitude, x-position, y-position and the error
    in the calculation of the absolute magnitude, from an DAF-file input
    ``line``.

    :param str line: DAF file data line.

    :return: the time, absolute magnitude, x-position, y-position and the
             error in the calculation of the absolute magnitude.
    :rtype: tuple

    :raises RuntimeWarning:
       if the input ``line`` does not contain a valid distance value.

    """

    items = line.split()

    # Check if the distance is provided in the line. If not, raise
    # exception.
    if items[10] == '----.-':
        logging.warning('Line %s does not provide distance value', line)
        raise RuntimeWarning('Line %s does not provide distance value' % line)

    dist = float(items[10]) / 1000
    # convert the observed magnitude to the absolute magnitude
    magn = (float(items[2]) + 2.5 * np.log10((100 ** 2) / (dist ** 2))) - 0.25

    # calculation of error for absolute mag taking into account
    # that the error in the observed magnitude is 1, and the error distance
    # is 0.001
    error = 1 + 5 / dist * 0.001

    return float(items[1]), magn, items[3], items[4], error


def process_data_block(lines, startline):
    """
    Returns the time values, absolute magnitudes, x and y positions and the
    estimation of the error in the computation of the absolute magnitudes
    for the complete data block from a DAF file contained in a list of
    read ``lines`` from the starting line ``startline``.

    :param list lines: DAF file lines read in a list of str.
    :param int startline: First line for the data block to be processed.

    :return: the time values, absolute magnitudes, x and y positions and the
             estimation of the error in the computation of the absolute
             magnitudes.
    :rtype: tuple

    """
    timevalues = []
    abs_err = []
    magnvalues = []
    x_val = []
    y_val = []
    while startline < len(lines):
        next_line = lines[startline]

        if next_line.find('  ') != -1:
            try:
                (time, magn, x_coor, y_coor, error) = \
                    parse_data_line(next_line)
            except RuntimeWarning:
                continue

            abs_err.append(error)
            # save all timevalues of ICC7 in timevalues_1
            timevalues.append(time)
            # save all magnitude values of ICC7 in timevalues_1
            magnvalues.append(magn)
            x_val.append(x_coor)
            y_val.append(y_coor)
            startline += 1

        else:
            # All values for the camera are saved.
            break

    return timevalues, magnvalues, x_val, y_val, abs_err


def abs_magnitude_at100km(magnitude, distance):
    """
    Returns the absolute magnitude at a distance of 100 km.

    :param float magnitude: maximum (measured?) magnitude.
    :param float distance: distance in km.
    :return: Absolute magnitude at a distance of 100 km.
    :rtype: float

    """
    return magnitude + 2.5 * np.log10((100**2) / distance ** 2) - 0.25


def compute_integrated_power(lines, start):
    """

    :param list lines: lines of daf file
    :param int start: first line for DAF record
    :return: Integrated power in W for the camera that recorded the meteor being
             represented by the current DAF data block, and the maximum error in
             the estimation of the integrated power.
    :rtype: tuple
    """
    (times, magnitudes, x_val, y_val, err) = process_data_block(lines, start)

    # now all time and absolute magnitude values are saved in
    # a matrix tim_ma_val_1 for ICC7 detections and
    # tim_ma_val_2 for ICC9 detections
    tim_ma_val = save_time_absmag_2matrix(times, magnitudes, x_val, y_val, err)

    # If meteors detected and the edges are not wanted
    # to be sorted out
    integral = np.sum(tim_ma_val[:, 1]) * 0.04

    error = []
    for point in tim_ma_val:
        # ICC7 errors for integral
        error.append(point[1] * point[4])

    return integral, max(error)


def get_maximum_mag_dis(mag_dist):
    """
    Returns the maximum magnitude and maximum distance from those in the
    input mag_dist matrix.

    :param list mag_dist: 2-dimensional list, where the first dimension is the
                list of absolute magnitudes and the second dimension is the
                corresponding distances.
    :return: two floating point values, the first being the maximum magnitude,
             and the second the maximum distance. These values do not need to
             correspond to each other.
    :rtype: tuple

    """
    mag_dist_wo_zeros = [item[:] for item in mag_dist if item[1] != 0]

    sorted_mag_dist = sorted(mag_dist_wo_zeros,
                             key=lambda element:
                             (element[0], element[1]))

    return sorted_mag_dist[0][0], sorted_mag_dist[0][1]


def compute_velocity(time_a, point_a, time_b, point_b):
    """
    Returns the velocity of a meteor given two points and their corresponding
    times.

    :param float time_a: time, in seconds, corresponding to the point_a.
    :param tuple point_a: position of the point_a, in geodetic longitude,
                latitude and altitude (in degrees and meters).
    :param float time_b: time, in seconds, corresponding to the point_b.
    :param tuple point_b: position of the point_b, in geodetic longitude,
                latitude and altitude (in degrees and meters).
    :return: velocity of a meteor given two points and their corresponding
             times, flag indicating if the meteor flies north-to-south and
             flag indicating if the meteor flies west-to-east.
    :rtype: tuple
    """
    delta_time = abs(time_a - time_b)

    dist_lon_lat, west_to_east, north_to_south = \
        lon_lat_dist(point_a[0], point_b[0], point_a[1], point_b[1])

    diff_dist_1 = np.sqrt(dist_lon_lat ** 2 +
                          ((point_a[2] - point_b[2]) ** 2))

    return diff_dist_1 * 0.001 / delta_time, north_to_south, west_to_east


def process_meteor_data(lines):
    """
    Returns the processed data for the meteor described by the DAF file
    provided in the 'input' lines.

    :param list lines: list of lines (str) as read from a valid DAF file.
    :return:
       Meteor:
             [0] Date
             [1] Appearance time, hours - as recorded by station 2
             [2] Appearacne time, minutes - as recorded by station 2
             [3] Appearance time, seconds - as recorded by station 2
             [4] velocity 1
             [5] velocity 2
             [6] delta velocity
             [7] mean velocity in km/s
             [9] maximum magnitude 1
             [9] maximum distance 1
             [10] maximum magnitude 2
             [11] maximum distance 2
             [12] new magnitude 1 (I guess 'new' means 'absolute' - dvk)
             [13] new magnitude 2 (I guess 'new' means 'absolute' - dvk)
             [14] delta magnitude
             [15] new mean magnitude (ibid)
             [16] first character of shower abbreviation of camera 1
             [17] second character of shower abbreviation of camera 1
             [18] third character of shower abbreviation of camera 1
             [19] first character of shower abbreviation of camera 2
             [20] second character of shower abbreviation of camera 2
             [21] third character of shower abbreviation of camera 2
             [22] flag indicating north-to-south movement
             [23] flag indicating east-to-west movement
             [24] average (of what? - dvk)
             [25] Integrated power in W (tbc), larger one of the two cameras
             [26] ThreeP integral (not sure what this means, dvk)
             [27] error of integral, average
       north_to_south: flag indicating north-to-south movement
       west_to_east: flag indicating east-to-west movement
    :rtype: tuple

    """
    mag_dist = np.zeros((1000, 2))
    j = 0
    shower = []

    #
    # process meteor data
    #
    for idx, line in enumerate(lines):

        # The following line contains an error. It should be instead of LogFile,
        # AppearanceDate.
        if line.startswith('AppearanceDate:'):
            date = line.split()[1].split('.')

        elif line.startswith('AppearanceTime:'):
            appear_time = line.split()[1]

        elif line.startswith('Shower:'):
            # This is new in V1.1. It used to come from a separate file. I keep the
            # variable naming from JETS to make it easier to trace it to their code.
            shower.append(line.split()[1])

        # When line starts with !### we have a new table, with its header.
        elif line.startswith('!###'):

            # Check if the meteor data has 2 lines (or less?), excluding the header.
            if int(idx + 4) == len(lines) or lines[idx + 4].strip() == '':
                three_lines = 1
            else:
                three_lines = 2

            # point1 (lon1, lat1, h_1)
            point1 = (float(lines[idx + three_lines].split()[8]),
                      float(lines[idx + three_lines].split()[9]),
                      float(lines[idx + three_lines].split()[5]))
            time_sec_1 = float(lines[idx + three_lines].split('  ')[1])

        elif line.find(' 0.') != -1 and not line.startswith('Accuracy'):
            items = line.split()

            # distance = items[10]
            if items[10] == '----.-':
                continue

            # Magnitude: items[2]; distance: items[10]
            mag_dist[j, 0] = items[2]
            mag_dist[j, 1] = float(items[10]) / 1000

            j += 1

            # point2 = (lon2, lat2, h_2)
            point2 = (float(items[8]), float(items[9]), float(items[5]))
            time_sec_2 = float(line.split('  ')[1])

            # three_lines is equal to 2 when the meteor data block has more than 3 lines
            # and is equal to 1 when the meteor data block has 3 lines or less.
            # Last line of meteor data block
            if (idx < len(lines) - three_lines
                    and lines[idx + three_lines].strip() == ''):

                integral7 = compute_integrated_power(lines, idx - j + 1)

                vel_1, north_to_south, west_to_east = \
                    compute_velocity(time_sec_1, point1, time_sec_2, point2)

                max_mag_dist_1 = get_maximum_mag_dis(mag_dist)
                mag_dist = np.zeros((1000, 2))

                # In order to read all lines in the next iteration, we need to take into
                # account if we are in a three-line meteor or not. If we are, then we
                # will have one line less read.
                j = 2 - three_lines

            # Last data point in the file. [JDR] This was - three_lines, which indicated
            # that it should remove the last line from the record, if this has more than
            # three lines.
            elif idx >= len(lines) - 1:

                integral9 = compute_integrated_power(lines, idx - j + 2)

                vel_2, north_to_south, west_to_east = \
                    compute_velocity(time_sec_1, point1, time_sec_2, point2)

                max_mag_dist_2 = get_maximum_mag_dis(mag_dist)

    # Absolute Magnitude (at 100 km) with distances in km.
    # max_mag_dist[0] = magnitude; max_mag_dist[1] = distance.
    new_mag_1 = abs_magnitude_at100km(max_mag_dist_1[0], max_mag_dist_1[1])
    new_mag_2 = abs_magnitude_at100km(max_mag_dist_2[0], max_mag_dist_2[1])

    meteor = [
        int(date[2] + date[1] + date[0]),  # date in YYYYMMDD format
        int(appear_time[0:2]),  # appear_time_h
        int(appear_time[3:5]),  # appear_time_m,
        int(appear_time[6:8]),  # appear_time_s,
        vel_1,
        vel_2,
        vel_1 - vel_2,  # delta_vel
        (vel_1 + vel_2) / 2,  # vel_mean,
        max_mag_dist_1[0],  # maximum magntiude from station 1
        max_mag_dist_1[1],  # maximum distance from station 1
        max_mag_dist_2[0],  # maximum magntiude from station 2
        max_mag_dist_2[1],  # maximum distance from station 2
        new_mag_1,
        new_mag_2,
        new_mag_1 - new_mag_2,
        min(new_mag_1, new_mag_2),
        ord(shower[0][0]),
        ord(shower[0][1]),
        ord(shower[0][2]),
        ord(shower[1][0]),
        ord(shower[1][1]),
        ord(shower[1][2]),
        north_to_south,
        west_to_east,
        (integral7[0] + integral9[0]) / 2,  # average: integral[0] = integrated PWR
        max(integral7[0], integral9[0]),  # larger_integral
        (integral7[0] + integral9[0]) / 2,  # three_p_integral = average
        max(integral7[1], integral9[1])]  # error_int_average: integral[1] = error integrated PWR

    return meteor, north_to_south, west_to_east


def read_data_jets(root, date_string):
    """
    Reading DAF files in a format required by the analysis software for determining flux density
    written by Jana, Esther, Theresa and Sandra(JETS).

    In the long run this should be replaced with routines from 'interface.py'. I also consider
    the file name a temporary one, once the JETS routines are compatible with the rest of our
    system we should get away from this name.

    2016-08-15, dvk V1.0 - taken out of CILBO_debiasing_Drolshagen_Kretschmer.py
    2016-08-16, dvk V1.1 - added reading of the shower from the DAF file rather than needing
                           the separate file det_both_cam.txt.

    params: array of string date_string: An array containing the dates to be considered.
            Example: ['20111213', 20111214', 20111215']

    Returns: list of list distance_velocity:
             [0] Date
             [1] Appearance time, hours - as recorded by station 2
             [2] Appearacne time, minutes - as recorded by station 2
             [3] Appearance time, seconds - as recorded by station 2
             [4] velocity 1
             [5] velocity 2
             [6] delta velocity
             [7] mean velocity in km/s
             [9] maximum magnitude 1
             [9] maximum distance 1
             [10] maximum magnitude 2
             [11] maximum distance 2
             [12] new magnitude 1 (I guess 'new' means 'absolute' - dvk)
             [13] new magnitude 2 (I guess 'new' means 'absolute' - dvk)
             [14] delta magnitude
             [15] new mean magnitude (ibid)
             [16] first character of shower abbreviation of camera 1
             [17] second character of shower abbreviation of camera 1
             [18] third character of shower abbreviation of camera 1
             [19] first character of shower abbreviation of camera 2
             [20] second character of shower abbreviation of camera 2
             [21] third character of shower abbreviation of camera 2
             [22] flag indicating north-to-south movement
             [23] flag indicating east-to-west movement
             [24] average (of what? - dvk)
             [25] Integrated power in W (tbc), larger one of the two cameras
             [26] ThreeP integral (not sure what this means, dvk)
             [27] error of integral, average
    """
    # ----------------------------------------------------------------------------------------------
    # set some variables
    # ----------------------------------------------------------------------------------------------
    n_meteors = 0
    logging.info('Assigning zeros to 28e5 data points')
    meteor_velocity = np.zeros((100000, 28))
    direction_north_to_south = []
    direction_west_to_east = []

    logging.info('Starting to read data')

    for filename in mots_ex.search_dir_by_dates(root, date_string[0], date_string[-1], '*.daf'):
        daf = open(filename)
        lines = daf.readlines()

        meteor, north_to_south, west_to_east = process_meteor_data(lines)

        direction_north_to_south.append(north_to_south)
        direction_west_to_east.append(west_to_east)

        meteor_velocity[n_meteors] = meteor
        n_meteors += 1

    logging.info('meteors read in and there are %d', n_meteors)

    # add a name tag shower or sporadics
    os.chdir(root)  # Path for Meteors detected by both cameras is needed

    logging.info('r = %d', n_meteors)
    # Eliminate all zeros, i.e. all meteors for which the
    # meteor_velocity[i][0] == 0
    distance_velocity = [item for item in meteor_velocity if item[0]]

    return distance_velocity, direction_north_to_south, direction_west_to_east
