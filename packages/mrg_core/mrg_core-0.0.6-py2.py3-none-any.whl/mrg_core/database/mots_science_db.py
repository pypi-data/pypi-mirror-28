"""
mots_science_db.py
Contact: Thomas Albin - tho.albin@gmail.com or albin@irs.uni-stuttgart.de

This routine computes saves all orbit elements in an SQLite Database. The .orb files are computed
with mots_orbit.py and mots_comporb.py

This program has only simple and rudimentary features. It can be easily extended, e.g. adding lists
for LIC1 and LIC2.

    Version         Date            Editor          Comment
    -------------------------------------------------------
    0.1             18.01.2016      Thomas Albin    Code written and debug. First tries.
    0.2             19.01.2016      Thomas Albin    Adding comments    
    0.3             01.03.2016      Thomas Albin    Adding Eclip Radiant values
    0.31            12.03.2016      Thomas Albin    Add sort
    0.40            13.03.2016      Thomas Albin    Added radiant in ECSC

"""


# ==================================================================================================
# Import modules
# glob:                     useful to get directory name or to search for file name paths
# pickle:                   has powerful saving and reading functions
# sqlite3:                  a module to generate and communicate with SQLite Databases (DB)
# numpy:                    module for numerical purposes
import sys
import glob
import pickle
import sqlite3
import numpy as np


def to_unicode(s):
    if sys.version_info >= (3, 0):
        if isinstance(s, bytes):
            return s.decode('utf-8')
        else:
            return s
    else:
        return s.decode('utf-8')

# =================================================================================================
# Define the cilbo_meteor_db
class cilbo_meteor_db:
    """
    Class to generate and update a CILBO science DB. Currently, all paths are hard-coded, since the
    code runs only idust.irs.uni-stuttgart.de.

    The "output" is the science db in:
    /home/albin/MeteorScience/CILBO-Database/cilbo_science.db.

    Additionally, 2 text files contain all .orb path names which are saved in the database:
    /home/albin/MeteorScience/CILBO-Database/cilbo_science_db_icc7.txt
    /home/albin/MeteorScience/CILBO-Database/cilbo_science_db_icc9.txt

    All .orb files are currently saved in:
    /home/albin/MeteorScience/CILBO-Data/Orbits/*/*7.orb
    /home/albin/MeteorScience/CILBO-Data/Orbits/*/*9.orb

    Parameters:
    -----------
        None (check Info Header)

    Properties / Returned Values:
    -----------------------------
        None (check Info Header)
    """


# -------------------------------------------------------------------------------------------------
    # __init__ - Initiate the class
    # Input: None (see description above)
    def __init__(self):
        # Set paths of the DB, path containing txt files and orb files
        self.db_path = '/home/albin/MeteorScience/CILBO-Database/cilbo_science.db'
        self.icc7_list = '/home/albin/MeteorScience/CILBO-Database/cilbo_science_db_icc7.txt'
        self.icc9_list = '/home/albin/MeteorScience/CILBO-Database/cilbo_science_db_icc9.txt'
        self.icc7_orb = '/home/albin/MeteorScience/CILBO-Data/Orbits/*/*7.orb'
        self.icc9_orb = '/home/albin/MeteorScience/CILBO-Data/Orbits/*/*9.orb'


        # Find the DB
        db_file = glob.glob(self.db_path)


        # If the database exists, the array contains the path to the file. Thus, if the length of
        # the array is greater the 0, connect to the DB and set the cursor. Else, Create Database
        # from scratch
        if len(db_file) > 0:
            self.con_cilbo = sqlite3.connect(self.db_path)
            self.cur_cilbo = self.con_cilbo.cursor()


        # If no DB has been found generate a DB from scratch
        if len(db_file) == 0:
            # Generate the path containing files
            np.savetxt(self.icc7_list, [])
            np.savetxt(self.icc9_list, [])


            # Create database (by connecting to an empty file)
            self.con_cilbo = sqlite3.connect(self.db_path)


            # Set cursor
            self.cur_cilbo = self.con_cilbo.cursor()


            # Define the table for the ICC7 data: cilbo_icc7
            # Set a primary key
            create_table_cilbo_icc7 = 'CREATE TABLE cilbo_icc7(' \
                                      'meteor_id INTEGER PRIMARY KEY, ' \
                                      'cam1_frames_bias INTEGER, ' \
                                      'cam1_frames INTEGER, ' \
                                      'cam2_frames_bias INTEGER, ' \
                                      'cam2_frames INTEGER, ' \
                                      'et4spice1 INTEGER, ' \
                                      'utc4spice1 TEXT, ' \
                                      'et4spice2 INTEGER, ' \
                                      'utc2spice2 TEXT, ' \
                                      'seeds INTEGER, ' \
                                      'vel_type TEXT, ' \
                                      \
                                      'appmag_median FLOAT, ' \
                                      'appmag_median_mad FLOAT, ' \
                                      'appmag_mean FLOAT, ' \
                                      'appmag_mean_std FLOAT, ' \
                                      'appmag_max FLOAT, ' \
                                      \
                                      'measure_acc_cam1 FLOAT, ' \
                                      'measure_acc_cam FLOAT, ' \
                                      'fit_cam1_astrometry_dist_max_median FLOAT, ' \
                                      'fit_cam1_astrometry_dist_max_median_mad FLOAT, ' \
                                      'fit_cam1_astrometry_dist_bias_max FLOAT, ' \
                                      'fit_cam1_astrometry_dist_unbiased_max FLOAT, ' \
                                      'fit_cam1_astrometry_dist_median FLOAT, ' \
                                      'fit_cam1_astrometry_dist_median_mad FLOAT, ' \
                                      'fit_cam1_astrometry_dist_mean FLOAT, ' \
                                      'fit_cam1_astrometry_dist_mean_std FLOAT, ' \
                                      'fit_cam2_astrometry_dist_max_median FLOAT, ' \
                                      'fit_cam2_astrometry_dist_max_median_mad FLOAT, ' \
                                      'fit_cam2_astrometry_dist_bias_max FLOAT, ' \
                                      'fit_cam2_astrometry_dist_unbiased_max FLOAT, ' \
                                      'fit_cam2_astrometry_dist_median FLOAT, ' \
                                      'fit_cam2_astrometry_dist_median_mad FLOAT, ' \
                                      'fit_cam2_astrometry_dist_mean FLOAT, ' \
                                      'fit_cam2_astrometry_dist_mean_std FLOAT, ' \
                                      \
                                      'vel_norm_mean FLOAT, ' \
                                      'vel_norm_mean_std FLOAT, ' \
                                      'vel_norm_median FLOAT, ' \
                                      'vel_norm_median_mad FLOAT, ' \
                                      \
                                      'altitude_median FLOAT, ' \
                                      'altitude_median_mad FLOAT, ' \
                                      'altitude_mean FLOAT, ' \
                                      'altitude_mean_std FLOAT, ' \
                                      \
                                      'zenith_distance_median FLOAT, ' \
                                      'zenith_distance_median_mad FLOAT, ' \
                                      'zenith_distance_mean FLOAT, ' \
                                      'zenith_distance_mean_std FLOAT, ' \
                                      'angular_dist_median, ' \
                                      'angular_dist_median_mad, ' \
                                      'angular_dist_mean, ' \
                                      'angular_dist_mean_std, ' \
                                      \
                                      'radiant_ra_median FLOAT, ' \
                                      'radiant_ra_median_mad FLOAT, ' \
                                      'radiant_dec_median FLOAT, ' \
                                      'radiant_dec_median_mad FLOAT, ' \
                                      'radiant_ra_mean FLOAT, ' \
                                      'radiant_ra_mean_std FLOAT, ' \
                                      'radiant_dec_mean FLOAT, ' \
                                      'radiant_dec_mean_std FLOAT, ' \
                                      'radiant_cov_ra_dec BLOB, ' \
                                      \
                                      'radiant_ecsc_long_median FLOAT, ' \
                                      'radiant_ecsc_long_median_mad FLOAT, ' \
                                      'radiant_ecsc_lat_median FLOAT, ' \
                                      'radiant_ecsc_lat_median_mad FLOAT, ' \
                                      'radiant_ecsc_long_mean FLOAT, ' \
                                      'radiant_ecsc_long_mean_std FLOAT, ' \
                                      'radiant_ecsc_lat_mean FLOAT, ' \
                                      'radiant_ecsc_lat_mean_std FLOAT, ' \
                                      'radiant_cov_ecsc_long_lat BLOB, ' \
                                      \
                                      'radiant_eclip_long_mean FLOAT, ' \
                                      'radiant_eclip_long_std FLOAT, ' \
                                      'radiant_eclip_lat_mean FLOAT, ' \
                                      'radiant_eclip_lat_std FLOAT, ' \
                                      'radiant_eclip_long_median FLOAT, ' \
                                      'radiant_eclip_long_mad FLOAT, ' \
                                      'radiant_eclip_lat_median FLOAT, ' \
                                      'radiant_eclip_lat_mad FLOAT, ' \
                                      'radiant_cov_eclip_long_lat BLOB, ' \
                                      \
                                      'meteor_appmax_cam_distance_median FLOAT, ' \
                                      'meteor_appmax_cam_distance_median_mad FLOAT, ' \
                                      'meteor_appmax_cam_distance_mean FLOAT, ' \
                                      'meteor_appmax_cam_distance_mean_std FLOAT, ' \
                                      'abs_mag_median FLOAT, ' \
                                      'abs_mag_median_mad FLOAT, ' \
                                      'abs_mag_mean FLOAT, ' \
                                      'abs_mag_mean_std FLOAT, ' \
                                      \
                                      'q_earth_mean FLOAT, ' \
                                      'q_earth_mean_std FLOAT, ' \
                                      'e_earth_mean FLOAT, ' \
                                      'e_earth_mean_std FLOAT, ' \
                                      'a_earth_mean FLOAT, ' \
                                      'a_earth_mean_std FLOAT, ' \
                                      'i_earth_mean FLOAT, ' \
                                      'i_earth_mean_std FLOAT, ' \
                                      'lnode_earth_mean FLOAT, ' \
                                      'lnode_earth_mean_std FLOAT, ' \
                                      'argp_earth_mean FLOAT, ' \
                                      'argp_earth_mean_std FLOAT, ' \
                                      'mzero_earth_mean FLOAT, ' \
                                      'mzero_earth_mean_std FLOAT, ' \
                                      \
                                      'q_earth_median FLOAT, ' \
                                      'q_earth_median_mad FLOAT, ' \
                                      'e_earth_median FLOAT, ' \
                                      'e_earth_median_mad FLOAT, ' \
                                      'a_earth_median FLOAT, ' \
                                      'a_earth_median_mad FLOAT, ' \
                                      'i_earth_median FLOAT, ' \
                                      'i_earth_median_mad FLOAT, ' \
                                      'lnode_earth_median FLOAT, ' \
                                      'lnode_earth_median_mad FLOAT, ' \
                                      'argp_earth_median FLOAT, ' \
                                      'argp_earth_median_mad FLOAT, ' \
                                      'mzero_earth_median FLOAT, ' \
                                      'mzero_earth_median_mad FLOAT, ' \
                                      'tzero_earth FLOAT, ' \
                                      \
                                      'conics_earth_cov BLOB, ' \
                                      \
                                      'q_helio_mean FLOAT, ' \
                                      'q_helio_mean_std FLOAT, ' \
                                      'e_helio_mean FLOAT, ' \
                                      'e_helio_mean_std FLOAT, ' \
                                      'a_helio_mean FLOAT, ' \
                                      'a_helio_mean_std FLOAT, ' \
                                      'i_helio_mean FLOAT, ' \
                                      'i_helio_mean_std FLOAT, ' \
                                      'lnode_helio_mean FLOAT, ' \
                                      'lnode_helio_mean_std FLOAT, ' \
                                      'argp_helio_mean FLOAT, ' \
                                      'argp_helio_mean_std FLOAT, ' \
                                      'mzero_helio_mean FLOAT, ' \
                                      'mzero_helio_mean_std FLOAT, ' \
                                      \
                                      'q_helio_median FLOAT, ' \
                                      'q_helio_median_mad FLOAT, ' \
                                      'e_helio_median FLOAT, ' \
                                      'e_helio_median_mad FLOAT, ' \
                                      'a_helio_median FLOAT, ' \
                                      'a_helio_median_mad FLOAT, ' \
                                      'i_helio_median FLOAT, ' \
                                      'i_helio_median_mad FLOAT, ' \
                                      'lnode_helio_median FLOAT, ' \
                                      'lnode_helio_median_mad FLOAT, ' \
                                      'argp_helio_median FLOAT, ' \
                                      'argp_helio_median_mad FLOAT, ' \
                                      'mzero_helio_median FLOAT, ' \
                                      'mzero_helio_median_mad FLOAT, ' \
                                      'tzero_helio FLOAT, ' \
                                      \
                                      'conics_helio_cov BLOB, ' \
                                      \
                                      'earth_bound_orbit_prob FLOAT, ' \
                                      \
                                      'tisserand_median FLOAT, ' \
                                      'tisserand_median_mad FLOAT, ' \
                                      'lz_median FLOAT, ' \
                                      'lz_median_mad FLOAT, ' \
                                      'delaunay_var_median FLOAT, ' \
                                      'delaunay_var_median_mad FLOAT, ' \
                                      \
                                      'tisserand_mean FLOAT, ' \
                                      'tisserand_mean_std FLOAT, ' \
                                      'lz_mean FLOAT, ' \
                                      'lz_mean_std FLOAT, ' \
                                      'delaunay_var_mean FLOAT, ' \
                                      'delaunay_var_mean_std FLOAT)'


            # Execute the SQL command to generate the table
            #
            self.cur_cilbo.execute(create_table_cilbo_icc7)
            self.con_cilbo.commit()


            # Define the table for the ICC9 data: cilbo_icc9
            # Set a primary key
            create_table_cilbo_icc9 = 'CREATE TABLE cilbo_icc9(' \
                                      'meteor_id INTEGER UNIQUE, ' \
                                      'cam1_frames_bias INTEGER, ' \
                                      'cam1_frames INTEGER, ' \
                                      'cam2_frames_bias INTEGER, ' \
                                      'cam2_frames INTEGER, ' \
                                      'et4spice1 INTEGER, ' \
                                      'utc4spice1 TEXT, ' \
                                      'et4spice2 INTEGER, ' \
                                      'utc2spice2 TEXT, ' \
                                      'seeds INTEGER, ' \
                                      'vel_type TEXT, ' \
                                      \
                                      'appmag_median FLOAT, ' \
                                      'appmag_median_mad FLOAT, ' \
                                      'appmag_mean FLOAT, ' \
                                      'appmag_mean_std FLOAT, ' \
                                      'appmag_max FLOAT, ' \
                                      \
                                      'measure_acc_cam1 FLOAT, ' \
                                      'measure_acc_cam2 FLOAT, ' \
                                      'fit_cam1_astrometry_dist_max_median FLOAT, ' \
                                      'fit_cam1_astrometry_dist_max_median_mad FLOAT, ' \
                                      'fit_cam1_astrometry_dist_bias_max FLOAT, ' \
                                      'fit_cam1_astrometry_dist_unbiased_max FLOAT, ' \
                                      'fit_cam1_astrometry_dist_median FLOAT, ' \
                                      'fit_cam1_astrometry_dist_median_mad FLOAT, ' \
                                      'fit_cam1_astrometry_dist_mean FLOAT, ' \
                                      'fit_cam1_astrometry_dist_mean_std FLOAT, ' \
                                      'fit_cam2_astrometry_dist_max_median FLOAT, ' \
                                      'fit_cam2_astrometry_dist_max_median_mad FLOAT, ' \
                                      'fit_cam2_astrometry_dist_bias_max FLOAT, ' \
                                      'fit_cam2_astrometry_dist_unbiased_max FLOAT, ' \
                                      'fit_cam2_astrometry_dist_median FLOAT, ' \
                                      'fit_cam2_astrometry_dist_median_mad FLOAT, ' \
                                      'fit_cam2_astrometry_dist_mean FLOAT, ' \
                                      'fit_cam2_astrometry_dist_mean_std FLOAT, ' \
                                      \
                                      'vel_norm_mean FLOAT, ' \
                                      'vel_norm_mean_std FLOAT, ' \
                                      'vel_norm_median FLOAT, ' \
                                      'vel_norm_median_mad FLOAT, ' \
                                      \
                                      'altitude_median FLOAT, ' \
                                      'altitude_median_mad FLOAT, ' \
                                      'altitude_mean FLOAT, ' \
                                      'altitude_mean_std FLOAT, ' \
                                      \
                                      'zenith_distance_median FLOAT, ' \
                                      'zenith_distance_median_mad FLOAT, ' \
                                      'zenith_distance_mean FLOAT, ' \
                                      'zenith_distance_mean_std FLOAT, ' \
                                      'angular_dist_median, ' \
                                      'angular_dist_median_mad, ' \
                                      'angular_dist_mean, ' \
                                      'angular_dist_mean_std, ' \
                                      \
                                      'radiant_ra_median FLOAT, ' \
                                      'radiant_ra_median_mad FLOAT, ' \
                                      'radiant_dec_median FLOAT, ' \
                                      'radiant_dec_median_mad FLOAT, ' \
                                      'radiant_ra_mean FLOAT, ' \
                                      'radiant_ra_mean_std FLOAT, ' \
                                      'radiant_dec_mean FLOAT, ' \
                                      'radiant_dec_mean_std FLOAT, ' \
                                      'radiant_cov_ra_dec BLOB, ' \
                                      \
                                      'radiant_ecsc_long_median FLOAT, ' \
                                      'radiant_ecsc_long_median_mad FLOAT, ' \
                                      'radiant_ecsc_lat_median FLOAT, ' \
                                      'radiant_ecsc_lat_median_mad FLOAT, ' \
                                      'radiant_ecsc_long_mean FLOAT, ' \
                                      'radiant_ecsc_long_mean_std FLOAT, ' \
                                      'radiant_ecsc_lat_mean FLOAT, ' \
                                      'radiant_ecsc_lat_mean_std FLOAT, ' \
                                      'radiant_cov_ecsc_long_lat BLOB, ' \
                                      \
                                      'radiant_eclip_long_mean FLOAT, ' \
                                      'radiant_eclip_long_std FLOAT, ' \
                                      'radiant_eclip_lat_mean FLOAT, ' \
                                      'radiant_eclip_lat_std FLOAT, ' \
                                      'radiant_eclip_long_median FLOAT, ' \
                                      'radiant_eclip_long_mad FLOAT, ' \
                                      'radiant_eclip_lat_median FLOAT, ' \
                                      'radiant_eclip_lat_mad FLOAT, ' \
                                      'radiant_cov_eclip_long_lat BLOB, ' \
                                      \
                                      'meteor_appmax_cam_distance_median FLOAT, ' \
                                      'meteor_appmax_cam_distance_median_mad FLOAT, ' \
                                      'meteor_appmax_cam_distance_mean FLOAT, ' \
                                      'meteor_appmax_cam_distance_mean_std FLOAT, ' \
                                      'abs_mag_median FLOAT, ' \
                                      'abs_mag_median_mad FLOAT, ' \
                                      'abs_mag_mean FLOAT, ' \
                                      'abs_mag_mean_std FLOAT, ' \
                                      \
                                      'q_earth_mean FLOAT, ' \
                                      'q_earth_mean_std FLOAT, ' \
                                      'e_earth_mean FLOAT, ' \
                                      'e_earth_mean_std FLOAT, ' \
                                      'a_earth_mean FLOAT, ' \
                                      'a_earth_mean_std FLOAT, ' \
                                      'i_earth_mean FLOAT, ' \
                                      'i_earth_mean_std FLOAT, ' \
                                      'lnode_earth_mean FLOAT, ' \
                                      'lnode_earth_mean_std FLOAT, ' \
                                      'argp_earth_mean FLOAT, ' \
                                      'argp_earth_mean_std FLOAT, ' \
                                      'mzero_earth_mean FLOAT, ' \
                                      'mzero_earth_mean_std FLOAT, ' \
                                      \
                                      'q_earth_median FLOAT, ' \
                                      'q_earth_median_mad FLOAT, ' \
                                      'e_earth_median FLOAT, ' \
                                      'e_earth_median_mad FLOAT, ' \
                                      'a_earth_median FLOAT, ' \
                                      'a_earth_median_mad FLOAT, ' \
                                      'i_earth_median FLOAT, ' \
                                      'i_earth_median_mad FLOAT, ' \
                                      'lnode_earth_median FLOAT, ' \
                                      'lnode_earth_median_mad FLOAT, ' \
                                      'argp_earth_median FLOAT, ' \
                                      'argp_earth_median_mad FLOAT, ' \
                                      'mzero_earth_median FLOAT, ' \
                                      'mzero_earth_median_mad FLOAT, ' \
                                      'tzero_earth FLOAT, ' \
                                      \
                                      'conics_earth_cov BLOB, ' \
                                      \
                                      'q_helio_mean FLOAT, ' \
                                      'q_helio_mean_std FLOAT, ' \
                                      'e_helio_mean FLOAT, ' \
                                      'e_helio_mean_std FLOAT, ' \
                                      'a_helio_mean FLOAT, ' \
                                      'a_helio_mean_std FLOAT, ' \
                                      'i_helio_mean FLOAT, ' \
                                      'i_helio_mean_std FLOAT, ' \
                                      'lnode_helio_mean FLOAT, ' \
                                      'lnode_helio_mean_std FLOAT, ' \
                                      'argp_helio_mean FLOAT, ' \
                                      'argp_helio_mean_std FLOAT, ' \
                                      'mzero_helio_mean FLOAT, ' \
                                      'mzero_helio_mean_std FLOAT, ' \
                                      \
                                      'q_helio_median FLOAT, ' \
                                      'q_helio_median_mad FLOAT, ' \
                                      'e_helio_median FLOAT, ' \
                                      'e_helio_median_mad FLOAT, ' \
                                      'a_helio_median FLOAT, ' \
                                      'a_helio_median_mad FLOAT, ' \
                                      'i_helio_median FLOAT, ' \
                                      'i_helio_median_mad FLOAT, ' \
                                      'lnode_helio_median FLOAT, ' \
                                      'lnode_helio_median_mad FLOAT, ' \
                                      'argp_helio_median FLOAT, ' \
                                      'argp_helio_median_mad FLOAT, ' \
                                      'mzero_helio_median FLOAT, ' \
                                      'mzero_helio_median_mad FLOAT, ' \
                                      'tzero_helio FLOAT, ' \
                                      \
                                      'conics_helio_cov BLOB, ' \
                                      \
                                      'earth_bound_orbit_prob FLOAT, ' \
                                      \
                                      'tisserand_median FLOAT, ' \
                                      'tisserand_median_mad FLOAT, ' \
                                      'lz_median FLOAT, ' \
                                      'lz_median_mad FLOAT, ' \
                                      'delaunay_var_median FLOAT, ' \
                                      'delaunay_var_median_mad FLOAT, ' \
                                      \
                                      'tisserand_mean FLOAT, ' \
                                      'tisserand_mean_std FLOAT, ' \
                                      'lz_mean FLOAT, ' \
                                      'lz_mean_std FLOAT, ' \
                                      'delaunay_var_mean FLOAT, ' \
                                      'delaunay_var_mean_std FLOAT, ' \
                                      'FOREIGN KEY(meteor_id) REFERENCES cilbo_icc7(meteor_id))'


            # Execute the SQL command to generate the table
            #
            self.cur_cilbo.execute(create_table_cilbo_icc9)
            self.con_cilbo.commit()


# -------------------------------------------------------------------------------------------------
    # update - Update the DB with the CILBO data
    # Input: self
    def update(self):
        # Get paths of all science data
        orbit_paths_icc7 = glob.glob(self.icc7_orb)
        orbit_paths_icc9 = glob.glob(self.icc9_orb)
        # Get paths of all path containing files
        cilbo_data_icc7 = np.loadtxt(self.icc7_list, dtype = 'object')
        cilbo_data_icc9 = np.loadtxt(self.icc9_list, dtype = 'object')


        # Build difference quantity of both arrays. Result: Science data paths which have not been
        # added yet to the database
        # ICC7:
        if len(cilbo_data_icc7) > 0:
            icc7_paths = set(cilbo_data_icc7) ^ set(orbit_paths_icc7)
            icc7_paths = np.array(list(icc7_paths))
            icc7_paths = np.sort(list(icc7_paths))
        elif len(cilbo_data_icc7) == 0:
            icc7_paths = orbit_paths_icc7
        # ICC9:
        if len(cilbo_data_icc9) > 0:
            icc9_paths = set(cilbo_data_icc9) ^ set(orbit_paths_icc9)
            icc9_paths = np.array(list(icc9_paths))
            icc9_paths = np.sort(list(icc9_paths))
        elif len(cilbo_data_icc9) == 0:
            icc9_paths = orbit_paths_icc9


        # Set the paths as instance
        self.icc7_paths = np.sort(icc7_paths)
        self.icc9_paths = np.sort(icc9_paths)


        # Generate the INSERT SQL commands for both ICC7 tables. The number of variables are 136
        nr_of_entries = '?, ' * 158
        icc7_insert_command = 'INSERT OR IGNORE INTO cilbo_icc7 VALUES(' + nr_of_entries[:-2] + ')'
        icc9_insert_command = 'INSERT OR IGNORE INTO cilbo_icc9 VALUES(' + nr_of_entries[:-2] + ')'


        # For loop: Open each orb file individually (ICC7), parse the data and save them in the
        # science DB
        orb_counter = 0
        for orb_path_for7 in self.icc7_paths:
            # Print status
            orb_counter += 1
            print('Now preparing: ' + orb_path_for7)
            print('Nr: ' + str(orb_counter) + ' of ' + str(len(self.icc7_paths)))


            # Open the current orb file
            icc7_data = pickle.load(open(orb_path_for7))
            # Parse the path of the file and generate and individual PRIMARY KEY for the table
            # Format: YYYYMMDDhhmmss
            # YYYY: Year
            # MM:   Month
            # DD:   Day
            # hh:   Hour
            # mm:   Minute
            # ss:   Second
            meteor_id_temp = orb_path_for7.split('/')
            meteor_id = int(meteor_id_temp[-2] + meteor_id_temp[-1].split('_')[0])


            # Generate the data array which will be saved in the database
            db_data = (meteor_id,
                       int(icc7_data['cam1_frames_bias']),
                       int(icc7_data['cam1_frames']),
                       int(icc7_data['cam2_frames_bias']),
                       int(icc7_data['cam2_frames']),
                       int(icc7_data['et4spice1']),
                       str(icc7_data['utc4spice1']),
                       int(icc7_data['et4spice2']),
                       str(icc7_data['utc4spice2']),
                       int(icc7_data['seeds']),
                       str(icc7_data['vel']),

                       float(icc7_data['appmag_median']),
                       float(icc7_data['appmag_median_mad']),
                       float(icc7_data['appmag_mean']),
                       float(icc7_data['appmag_mean_std']),
                       float(icc7_data['appmag_max']),

                       float(icc7_data['measure_acc_cam1']),
                       float(icc7_data['measure_acc_cam2']),
                       float(icc7_data['fit_cam1_astrometry_dist_max_median']),
                       float(icc7_data['fit_cam1_astrometry_dist_max_median_mad']),
                       float(icc7_data['fit_cam1_astrometry_dist_bias_max']),
                       float(icc7_data['fit_cam1_astrometry_dist_unbiased_max']),
                       float(icc7_data['fit_cam1_astrometry_dist_median']),
                       float(icc7_data['fit_cam1_astrometry_dist_median_mad']),
                       float(icc7_data['fit_cam1_astrometry_dist_mean']),
                       float(icc7_data['fit_cam1_astrometry_dist_mean_std']),
                       float(icc7_data['fit_cam2_astrometry_dist_max_median']),
                       float(icc7_data['fit_cam2_astrometry_dist_max_median_mad']),
                       float(icc7_data['fit_cam2_astrometry_dist_bias_max']),
                       float(icc7_data['fit_cam2_astrometry_dist_unbiased_max']),
                       float(icc7_data['fit_cam2_astrometry_dist_median']),
                       float(icc7_data['fit_cam2_astrometry_dist_median_mad']),
                       float(icc7_data['fit_cam2_astrometry_dist_mean']),
                       float(icc7_data['fit_cam2_astrometry_dist_mean_std']),

                       float(icc7_data['vel_norm_mean']),
                       float(icc7_data['vel_norm_mean_std']),
                       float(icc7_data['vel_norm_median']),
                       float(icc7_data['vel_norm_median_mad']),

                       float(icc7_data['altitude_median']),
                       float(icc7_data['altitude_median_mad']),
                       float(icc7_data['altitude_mean']),
                       float(icc7_data['altitude_mean_std']),

                       float(icc7_data['zenith_distance_median']),
                       float(icc7_data['zenith_distance_median_mad']),
                       float(icc7_data['zenith_distance_mean']),
                       float(icc7_data['zenith_distance_mean_std']),
                       float(icc7_data['angular_dist_median']),
                       float(icc7_data['angular_dist_median_mad']),
                       float(icc7_data['angular_dist_mean']),
                       float(icc7_data['angular_dist_mean_std']),

                       float(icc7_data['radiant_ra_median']),
                       float(icc7_data['radiant_ra_median_mad']),
                       float(icc7_data['radiant_dec_median']),
                       float(icc7_data['radiant_dec_median_mad']),
                       float(icc7_data['radiant_ra_mean']),
                       float(icc7_data['radiant_ra_mean_std']),
                       float(icc7_data['radiant_dec_mean']),
                       float(icc7_data['radiant_dec_mean_std']),
                       to_unicode(icc7_data['radiant_cov_ra_dec']),

                       float(icc7_data['radiant_ecsc_long_median']),
                       float(icc7_data['radiant_ecsc_long_median_mad']),
                       float(icc7_data['radiant_ecsc_lat_median']),
                       float(icc7_data['radiant_ecsc_lat_median_mad']),
                       float(icc7_data['radiant_ecsc_long_mean']),
                       float(icc7_data['radiant_ecsc_long_mean_std']),
                       float(icc7_data['radiant_ecsc_lat_mean']),
                       float(icc7_data['radiant_ecsc_lat_mean_std']),
                       to_unicode(icc7_data['radiant_cov_ecsc_long_lat']),

                       float(icc7_data['radiant_eclip_long_mean']),
                       float(icc7_data['radiant_eclip_long_std']),
                       float(icc7_data['radiant_eclip_lat_mean']),
                       float(icc7_data['radiant_eclip_lat_std']),
                       float(icc7_data['radiant_eclip_long_median']),
                       float(icc7_data['radiant_eclip_long_mad']),
                       float(icc7_data['radiant_eclip_lat_median']),
                       float(icc7_data['radiant_eclip_lat_mad']),
                       to_unicode(icc7_data['radiant_cov_eclip_long_lat']),

                       float(icc7_data['meteor_appmax_cam_distance_median']),
                       float(icc7_data['meteor_appmax_cam_distance_median_mad']),
                       float(icc7_data['meteor_appmax_cam_distance_mean']),
                       float(icc7_data['meteor_appmax_cam_distance_mean_std']),
                       float(icc7_data['abs_mag_median']),
                       float(icc7_data['abs_mag_median_mad']),
                       float(icc7_data['abs_mag_mean']),
                       float(icc7_data['abs_mag_mean_std']),

                       float(icc7_data['q_earth_mean']),
                       float(icc7_data['q_earth_mean_std']),
                       float(icc7_data['e_earth_mean']),
                       float(icc7_data['e_earth_mean_std']),
                       float(icc7_data['a_earth_mean']),
                       float(icc7_data['a_earth_mean_std']),
                       float(icc7_data['i_earth_mean']),
                       float(icc7_data['i_earth_mean_std']),
                       float(icc7_data['lnode_earth_mean']),
                       float(icc7_data['lnode_earth_mean_std']),
                       float(icc7_data['argp_earth_mean']),
                       float(icc7_data['argp_earth_mean_std']),
                       float(icc7_data['mzero_earth_mean']),
                       float(icc7_data['mzero_earth_mean_std']),

                       float(icc7_data['q_earth_median']),
                       float(icc7_data['q_earth_median_mad']),
                       float(icc7_data['e_earth_median']),
                       float(icc7_data['e_earth_median_mad']),
                       float(icc7_data['a_earth_median']),
                       float(icc7_data['a_earth_median_mad']),
                       float(icc7_data['i_earth_median']),
                       float(icc7_data['i_earth_median_mad']),
                       float(icc7_data['lnode_earth_median']),
                       float(icc7_data['lnode_earth_median_mad']),
                       float(icc7_data['argp_earth_median']),
                       float(icc7_data['argp_earth_median_mad']),
                       float(icc7_data['mzero_earth_median']),
                       float(icc7_data['mzero_earth_median_mad']),
                       float(icc7_data['tzero_earth']),

                       to_unicode(icc7_data['conics_earth_cov']),

                       float(icc7_data['q_helio_mean']),
                       float(icc7_data['q_helio_mean_std']),
                       float(icc7_data['e_helio_mean']),
                       float(icc7_data['e_helio_mean_std']),
                       float(icc7_data['a_helio_mean']),
                       float(icc7_data['a_helio_mean_std']),
                       float(icc7_data['i_helio_mean']),
                       float(icc7_data['i_helio_mean_std']),
                       float(icc7_data['lnode_helio_mean']),
                       float(icc7_data['lnode_helio_mean_std']),
                       float(icc7_data['argp_helio_mean']),
                       float(icc7_data['argp_helio_mean_std']),
                       float(icc7_data['mzero_helio_mean']),
                       float(icc7_data['mzero_helio_mean_std']), \

                       float(icc7_data['q_helio_median']),
                       float(icc7_data['q_helio_median_mad']),
                       float(icc7_data['e_helio_median']),
                       float(icc7_data['e_helio_median_mad']),
                       float(icc7_data['a_helio_median']),
                       float(icc7_data['a_helio_median_mad']),
                       float(icc7_data['i_helio_median']),
                       float(icc7_data['i_helio_median_mad']),
                       float(icc7_data['lnode_helio_median']),
                       float(icc7_data['lnode_helio_median_mad']),
                       float(icc7_data['argp_helio_median']),
                       float(icc7_data['argp_helio_median_mad']),
                       float(icc7_data['mzero_helio_median']),
                       float(icc7_data['mzero_helio_median_mad']),
                       float(icc7_data['tzero_helio']), \

                       to_unicode(icc7_data['conics_helio_cov']),

                       float(icc7_data['earth_bound_orbit_prob']), \

                       float(icc7_data['tisserand_median']),
                       float(icc7_data['tisserand_median_mad']),
                       float(icc7_data['lz_median']),
                       float(icc7_data['lz_median_mad']),
                       float(icc7_data['delaunay_var_median']),
                       float(icc7_data['delaunay_var_median_mad']), \

                       float(icc7_data['tisserand_mean']),
                       float(icc7_data['tisserand_mean_std']),
                       float(icc7_data['lz_mean']),
                       float(icc7_data['lz_mean_std']),
                       float(icc7_data['delaunay_var_mean']),
                       float(icc7_data['delaunay_var_mean_std']))


            # Execute Insert SQL command with the data array
            self.cur_cilbo.execute(icc7_insert_command, db_data)
            self.con_cilbo.commit()


            # Save the used orb path in the txt file
            cilbo_icc7_db_list = open(self.icc7_list, 'a+')
            cilbo_icc7_db_list.write(orb_path_for7 + '\n')
            cilbo_icc7_db_list.close()


        # Print status
        print('ICC7: DONE')


        # For loop: Open each orb file individually (ICC7), parse the data and save them in the
        # science DB
        orb_counter = 0
        for orb_path_for9 in self.icc9_paths:
            # Print status
            orb_counter += 1
            print('Now preparing: ' + orb_path_for9)
            print('Nr: ' + str(orb_counter) + ' of ' + str(len(self.icc9_paths)))
            # Open the current orb file
            icc9_data = pickle.load(open(orb_path_for9))
            # Parse the path of the file and generate and individual FORGEIN KEY for the table (with
            # reference)
            # Format: YYYYMMDDhhmmss
            # YYYY: Year
            # MM:   Month
            # DD:   Day
            # hh:   Hour
            # mm:   Minute
            # ss:   Second
            meteor_id_temp = orb_path_for9.split('/')
            meteor_id = int(meteor_id_temp[-2] + meteor_id_temp[-1].split('_')[0])


            # Generate the data array which will be saved in the database
            db_data = (meteor_id,
                       int(icc9_data['cam1_frames_bias']),
                       int(icc9_data['cam1_frames']),
                       int(icc9_data['cam2_frames_bias']),
                       int(icc9_data['cam2_frames']),
                       int(icc9_data['et4spice1']),
                       str(icc9_data['utc4spice1']),
                       int(icc9_data['et4spice2']),
                       str(icc9_data['utc4spice2']),
                       int(icc9_data['seeds']),
                       str(icc9_data['vel']), \

                       float(icc9_data['appmag_median']),
                       float(icc9_data['appmag_median_mad']),
                       float(icc9_data['appmag_mean']),
                       float(icc9_data['appmag_mean_std']),
                       float(icc9_data['appmag_max']), \

                       float(icc9_data['measure_acc_cam1']),
                       float(icc9_data['measure_acc_cam2']),
                       float(icc9_data['fit_cam1_astrometry_dist_max_median']),
                       float(icc9_data['fit_cam1_astrometry_dist_max_median_mad']),
                       float(icc9_data['fit_cam1_astrometry_dist_bias_max']),
                       float(icc9_data['fit_cam1_astrometry_dist_unbiased_max']),
                       float(icc9_data['fit_cam1_astrometry_dist_median']),
                       float(icc9_data['fit_cam1_astrometry_dist_median_mad']),
                       float(icc9_data['fit_cam1_astrometry_dist_mean']),
                       float(icc9_data['fit_cam1_astrometry_dist_mean_std']),
                       float(icc9_data['fit_cam2_astrometry_dist_max_median']),
                       float(icc9_data['fit_cam2_astrometry_dist_max_median_mad']),
                       float(icc9_data['fit_cam2_astrometry_dist_bias_max']),
                       float(icc9_data['fit_cam2_astrometry_dist_unbiased_max']),
                       float(icc9_data['fit_cam2_astrometry_dist_median']),
                       float(icc9_data['fit_cam2_astrometry_dist_median_mad']),
                       float(icc9_data['fit_cam2_astrometry_dist_mean']),
                       float(icc9_data['fit_cam2_astrometry_dist_mean_std']), \

                       float(icc9_data['vel_norm_mean']),
                       float(icc9_data['vel_norm_mean_std']),
                       float(icc9_data['vel_norm_median']),
                       float(icc9_data['vel_norm_median_mad']), \

                       float(icc9_data['altitude_median']),
                       float(icc9_data['altitude_median_mad']),
                       float(icc9_data['altitude_mean']),
                       float(icc9_data['altitude_mean_std']), \

                       float(icc9_data['zenith_distance_median']),
                       float(icc9_data['zenith_distance_median_mad']),
                       float(icc9_data['zenith_distance_mean']),
                       float(icc9_data['zenith_distance_mean_std']),
                       float(icc9_data['angular_dist_median']),
                       float(icc9_data['angular_dist_median_mad']),
                       float(icc9_data['angular_dist_mean']),
                       float(icc9_data['angular_dist_mean_std']), \

                       float(icc9_data['radiant_ra_median']),
                       float(icc9_data['radiant_ra_median_mad']),
                       float(icc9_data['radiant_dec_median']),
                       float(icc9_data['radiant_dec_median_mad']),
                       float(icc9_data['radiant_ra_mean']),
                       float(icc9_data['radiant_ra_mean_std']),
                       float(icc9_data['radiant_dec_mean']),
                       float(icc9_data['radiant_dec_mean_std']),
                       to_unicode(icc9_data['radiant_cov_ra_dec']),

                       float(icc9_data['radiant_ecsc_long_median']),
                       float(icc9_data['radiant_ecsc_long_median_mad']),
                       float(icc9_data['radiant_ecsc_lat_median']),
                       float(icc9_data['radiant_ecsc_lat_median_mad']),
                       float(icc9_data['radiant_ecsc_long_mean']),
                       float(icc9_data['radiant_ecsc_long_mean_std']),
                       float(icc9_data['radiant_ecsc_lat_mean']),
                       float(icc9_data['radiant_ecsc_lat_mean_std']),
                       to_unicode(icc9_data['radiant_cov_ecsc_long_lat']),

                       float(icc9_data['radiant_eclip_long_mean']),
                       float(icc9_data['radiant_eclip_long_std']),
                       float(icc9_data['radiant_eclip_lat_mean']),
                       float(icc9_data['radiant_eclip_lat_std']),
                       float(icc9_data['radiant_eclip_long_median']),
                       float(icc9_data['radiant_eclip_long_mad']),
                       float(icc9_data['radiant_eclip_lat_median']),
                       float(icc9_data['radiant_eclip_lat_mad']),
                       to_unicode(icc9_data['radiant_cov_eclip_long_lat']),

                       float(icc9_data['meteor_appmax_cam_distance_median']),
                       float(icc9_data['meteor_appmax_cam_distance_median_mad']),
                       float(icc9_data['meteor_appmax_cam_distance_mean']),
                       float(icc9_data['meteor_appmax_cam_distance_mean_std']),
                       float(icc9_data['abs_mag_median']),
                       float(icc9_data['abs_mag_median_mad']),
                       float(icc9_data['abs_mag_mean']),
                       float(icc9_data['abs_mag_mean_std']), \

                       float(icc9_data['q_earth_mean']),
                       float(icc9_data['q_earth_mean_std']),
                       float(icc9_data['e_earth_mean']),
                       float(icc9_data['e_earth_mean_std']),
                       float(icc9_data['a_earth_mean']),
                       float(icc9_data['a_earth_mean_std']),
                       float(icc9_data['i_earth_mean']),
                       float(icc9_data['i_earth_mean_std']),
                       float(icc9_data['lnode_earth_mean']),
                       float(icc9_data['lnode_earth_mean_std']),
                       float(icc9_data['argp_earth_mean']),
                       float(icc9_data['argp_earth_mean_std']),
                       float(icc9_data['mzero_earth_mean']),
                       float(icc9_data['mzero_earth_mean_std']), \

                       float(icc9_data['q_earth_median']),
                       float(icc9_data['q_earth_median_mad']),
                       float(icc9_data['e_earth_median']),
                       float(icc9_data['e_earth_median_mad']),
                       float(icc9_data['a_earth_median']),
                       float(icc9_data['a_earth_median_mad']),
                       float(icc9_data['i_earth_median']),
                       float(icc9_data['i_earth_median_mad']),
                       float(icc9_data['lnode_earth_median']),
                       float(icc9_data['lnode_earth_median_mad']),
                       float(icc9_data['argp_earth_median']),
                       float(icc9_data['argp_earth_median_mad']),
                       float(icc9_data['mzero_earth_median']),
                       float(icc9_data['mzero_earth_median_mad']),
                       float(icc9_data['tzero_earth']), \

                       to_unicode(icc9_data['conics_earth_cov']),

                       float(icc9_data['q_helio_mean']),
                       float(icc9_data['q_helio_mean_std']),
                       float(icc9_data['e_helio_mean']),
                       float(icc9_data['e_helio_mean_std']),
                       float(icc9_data['a_helio_mean']),
                       float(icc9_data['a_helio_mean_std']),
                       float(icc9_data['i_helio_mean']),
                       float(icc9_data['i_helio_mean_std']),
                       float(icc9_data['lnode_helio_mean']),
                       float(icc9_data['lnode_helio_mean_std']),
                       float(icc9_data['argp_helio_mean']),
                       float(icc9_data['argp_helio_mean_std']),
                       float(icc9_data['mzero_helio_mean']),
                       float(icc9_data['mzero_helio_mean_std']), \

                       float(icc9_data['q_helio_median']),
                       float(icc9_data['q_helio_median_mad']),
                       float(icc9_data['e_helio_median']),
                       float(icc9_data['e_helio_median_mad']),
                       float(icc9_data['a_helio_median']),
                       float(icc9_data['a_helio_median_mad']),
                       float(icc9_data['i_helio_median']),
                       float(icc9_data['i_helio_median_mad']),
                       float(icc9_data['lnode_helio_median']),
                       float(icc9_data['lnode_helio_median_mad']),
                       float(icc9_data['argp_helio_median']),
                       float(icc9_data['argp_helio_median_mad']),
                       float(icc9_data['mzero_helio_median']),
                       float(icc9_data['mzero_helio_median_mad']),
                       float(icc9_data['tzero_helio']), \

                       to_unicode(icc9_data['conics_helio_cov']),

                       float(icc9_data['earth_bound_orbit_prob']), \

                       float(icc9_data['tisserand_median']),
                       float(icc9_data['tisserand_median_mad']),
                       float(icc9_data['lz_median']),
                       float(icc9_data['lz_median_mad']),
                       float(icc9_data['delaunay_var_median']),
                       float(icc9_data['delaunay_var_median_mad']), \

                       float(icc9_data['tisserand_mean']),
                       float(icc9_data['tisserand_mean_std']),
                       float(icc9_data['lz_mean']),
                       float(icc9_data['lz_mean_std']),
                       float(icc9_data['delaunay_var_mean']),
                       float(icc9_data['delaunay_var_mean_std']), )


            # Execute Insert SQL command with the data array
            self.cur_cilbo.execute(icc9_insert_command, db_data)
            self.con_cilbo.commit()


            # Save the used orb path in the txt file
            cilbo_icc9_db_list = open(self.icc9_list, 'a+')
            cilbo_icc9_db_list.write(orb_path_for9 + '\n')
            cilbo_icc9_db_list.close()

        # Print status
        print('ICC9: DONE')


# Update main routine
if True:
    database = cilbo_meteor_db()
    database.update()
    # Print status
    print('END OF MOTS_SCIENCE_DB.PY')
