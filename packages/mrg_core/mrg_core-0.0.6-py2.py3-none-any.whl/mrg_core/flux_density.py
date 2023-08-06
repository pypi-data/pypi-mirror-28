# -*- coding: cp1252 -*-
# --------------------------------------------------------------------------------------------------
#   Copyright 2016 SCI-S, ESA (European Space Agency)
#       Sam Leakey <Sam.Leakey@esa.int>
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
# --------------------------------------------------------------------------------------------------
#
# TO CHECK - Which column width were you using? It would read nicer if the # ---- are the length of
# your used width. I am using 100 columns, this is also what the comment lines are aligned to.
# Please stick to one width (i.e. if you keep 100, which I recommend, shorten everything that
# goes outside it. DVK, 18 Nov 2016
#
#  End goal:
#  Will be an extensively refactored version of code that was initially written by Sandra Drolshagen and Jana Kretschmer
#  which, in turn, was based on code by Esther Drolshagen and Theresa Ott. The intention is that this script will
#  replace CILBO_debiasing_Drolshagen_Kretschmer in the MRG repository and more closely integrate with exisiting MRG
#  routines for data reading. All criticism and suggestions very much welcomed.
#
#
#  Version info:
#  V0.1, 2016-10-10, plots Gruen interplanetary meteoroid flux model to be used as reference.
#  V0.2, 2016-11-  , ... in progress.
#
#
#  Current state:
#  Plots reference flux model, reads data into pandas dataframe, acts on that data to generate more useful values
#  (e.g. absolute magnitudes, meteor velocities, geodetic distances).
#
#
#  To do list (roughly in order of priority):
#  * Complete per_station_manipulation function so that all necessary values for
#    analysis are stored.
#  * Revise parts of per_station manipulation to prevent unequal DataFrame length
#    errors occuring in all_station_manipulation.
#  * Create new data frame to store those values which are to be carried forwards
#    for use in the analysis/plotting stage of the program.
#  * Implement calling the reading routine directly from interface.py to replace
#    its copied/pasted inclusion in this file.
#  * Implement command line parsing for data reading (directory, date range, etc.)
#    and writing (csv files, plots, etc.).
#  * Begin replication of CILBO_debiasing_Drolshagen_Kretschmer's functionality.
#  * Investigate DK's suggestion of storing data in 'some kind of Python file' for
#    faster reading.
#
#
#  Long-term adds:
#  * Ability to import reduced 'historic' DAF data when running this script on new DAF files, i.e., when reading in new
#    DAF files, only having to reduce the new data to add it to the existing dataset.
# --------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------
# Import required libraries
# --------------------------------------------------------------------------------------------------
from __future__ import print_function

import numpy as np
import pandas as pd

from mrg_core.util.interface import read_daf_files


# --------------------------------------------------------------------------------------------------
# Initialise global constants
# --------------------------------------------------------------------------------------------------
# Temporary boolean switch for plots
PLOT_CUM_FLUX_DENSITY = False


# --------------------------------------------------------------------------------------------------
# Define functions
# --------------------------------------------------------------------------------------------------
def per_station_manipulation(df):
    """
    Performs math operations on one station's data at a time. Raw data optical are converted to more useful forms:
    e.g.apparent to absolute magnitude. Then positional and trajectory data are operated on. Finally unrequired
    columns are then deleted.

    All equations/constants are lifted from read_data_JETS. The 'intg_luminosity_err' calculation needs attention,
    see note below.

    :param df: dataframe containing DAF data from one station.
    :return:
    """

    # --------------------------------------------------------------------------------------------------
    # Operations on: magnitude, luminosity and their errors
    # --------------------------------------------------------------------------------------------------
    # Convert apparent magnitude ('Bright') to absolute magnitude (abs_mag).
    df['abs_mag'] = (df['Bright'] + 2.5 * np.log10((100 ** 2) / ((df['dist'] / 1000) ** 2))) - 0.25

    # Note the brightest absolute magnitude.
    df['max_mag'] = df['abs_mag'].min()

    # Calculate the error in absolute magnitude. Note error in apparent magnitude is 1, and in distance is 0.001(km)
    df['abs_mag_err'] = 1 + (5 / (df['dist'] / 1000) * 0.001)

    # Calculate the meteor luminosity from absolute magnitude.
    df['luminosity'] = 525 * 10 ** (-0.4 * df['abs_mag'])

    # Calculate the error in luminosity.
    df['luminosity_err'] = abs(-0.4 * df['luminosity'] * np.log(10) * df['abs_mag_err'])

    # Calculate the integrated luminosity of each meteor.
    # TO CHECK - This may not be good enough - what if one frame is missing? My feeling is that
    # we have to read in the individual times here and possibly interpolate missing frames.
    # DVK, 18 Nov 2016
    df['intg_luminosity'] = df['luminosity'].sum() * 0.04

    # !!! Needs attention.
    # Calculate the integrated luminosity error. read_data_JETS method, yields errors an order of magnitude greater
    # than the integrated luminosity (!?)
    df['intg_luminosity_err'] = df['luminosity'] * df['luminosity_err']

    # Possible alternative to above: calculate the integrated luminosity error in the same way as the integrated
    # luminosity was calculated.
    # df['intg_luminosity_err'] = df['luminosity_err'].sum() * 0.04

    # --------------------------------------------------------------------------------------------------
    # Operations on: position, distance travelled and velocity
    # --------------------------------------------------------------------------------------------------
    # Calculate the difference in the longitude [rad] of each meteor between the first and last frames.
    df['dlon'] = np.radians((df['lon'].iloc[0]) - (df['lon'].iloc[-1]))

    # Calculate the difference in the latitude [rad] of each meteor between the first and last frames.
    df['dlat'] = np.radians((df['lat'].iloc[0]) - (df['lat'].iloc[-1]))

    # Define the latitude [rad] at the start and end of each observation as being the first and last values stored.
    df['lat_start'] = np.radians((df['lat'].iloc[0]))
    df['lat_end'] = np.radians((df['lat'].iloc[-1]))

    # Calculate geodetic distance [m] between the latitudes and longitudes of the meteor in the first and last frame
    # using the haversine formula. Store the result in the data frame under the header 'geodetic_dist'
    x = abs((np.sin(df['dlat'] / 2.)) ** 2 + np.cos(df['lat_start']) * np.cos(df['lat_end'])
            * (np.sin(df['dlon'] / 2.)) ** 2)
    y = 2 * np.arcsin(np.sqrt(x))
    # Radius of Earth = 6371000 m
    # @TO CHECK - don't write 6371000 [m] The square brackets don't
    # belong there. '[]' stands for 'unit of'. I.e. you can write [E] = J meaning 'Unit of energy
    # is Joule. The other way around is not correct, even though often (wrongly) used.
    # DVK, 18 Nov 2016.
    df['geodetic_dist'] = 6371000. * y

    # Calculate the distance travelled [m] using the difference in altitude ('h') [m] between first and last frames.
    dist = np.sqrt(df['geodetic_dist'] ** 2 + ((df['h'].iloc[0] - df['h'].iloc[-1])**2))

    # Calculate the difference in time [s] between between the first and last frames.
    df['time_diff'] = abs(df['Time'].iloc[0] - df['Time'].iloc[-1])

    # Calculate the average velocity [m/s] with which the meteor covered this distance.
    df['vel'] = dist / df['time_diff']

    # --------------------------------------------------------------------------------------------------
    # Dataframe housekeeping: deleting unnecessary columns and duplicate rows, sorting, renaming
    # @TO CHECK - the following is a bit dubious, which columns are you dropping? I suggest to
    # add some explanation somewhere.
    # --------------------------------------------------------------------------------------------------
    # Delete multiple groups of columns that are not required.
    df.drop(df.columns[:2], inplace=True, axis=1)
    #
    # Dropping columns above shifts column index so column labels to be dropped below are shifted accordingly.
    # Useful revision would be to execute all drops at same time using original rather than shifted column labels but
    # unsure of the syntax.
    df.drop(df.columns[1:13], inplace=True, axis=1)

    # Delete rows where geodetic distance is a duplicate of the previous row (keep first instance of each geodectic dist
    # and hence one record of all data required for plotting each meteor).
    df.drop_duplicates(['geodetic_dist'], inplace=True)

    # One final drop of unrequired columns.
    df.drop(df.columns[8:14], inplace=True, axis=1)

    # Sort the dataframe by advancing date.
    df.sort_values(by='DateTime', inplace=True)


def all_station_manipulation(df_1, df_2):
    """
    Performs math operations on both station's data together to calculate the differences between them, average and
    maximum values. These results are currently appended to the dataframe of station_1 but will eventually be stored in
    their own dataframe.

    All equations/constants are lifted from read_data_JETS.

    :param df_1: dataframe containing DAF data from station_1
    :param df_2: dataframe containing DAF data from station_2
    :return:
    """

    # Calculate the absolute difference in meteor velocity [m/s] as seen from each station.
    df_1['vel_diff'] = abs(df_1['vel'] - df_2['vel'])

    # Calculate the average meteor velocity [m/s] as seen from both stations.
    df_1['vel_avg'] = (df_1['vel'] + df_2['vel']) / 2

    # Calculate the difference in maximum absolute magnitude of each meteor as seen by each station.
    df_1['max_abs_mag_diff'] = df_1['max_mag'] - df_2['max_mag']

    # !!! Needs attention
    # Lifted from read_data_JETS, but I don't see how the brightest meteor magnitude as seen by either station can be
    # used as the average. Unless it's an assumption somewhere in SD and JK's thesis that I haven't seen.
    # Calculate the average absolute magnitude of each meteor.
    df_1['avg_abs_mag'] = df_1['max_mag'].where(df_1['max_mag'] < df_2['max_mag'], df_2['max_mag'])

    # @TO CHECK - indeed they use the larger value. The term 'average' is not good... The reason is
    # that sometimes meteors are not fully in the field of view of one camera. Then the integrated
    # value is of course smaller. DVK, 18 Nov 2016.

    # Reassign the integrated luminosity for each meteor as the largest value determined by each station.
    df_1['intg_luminosity'] = df_1['intg_luminosity']\
        .where(df_1['intg_luminosity'] > df_2['intg_luminosity'], df_2['intg_luminosity'])

    # Reassign the integrated luminosity error for each meteor as the largest value determined by each station.
    df_1['intg_luminosity_err'] = df_1['intg_luminosity_err']\
        .where(df_1['intg_luminosity_err'] > df_2['intg_luminosity_err'], df_2['intg_luminosity_err'])

    # Return only df_1 as all required values are now stored there.
    return df_1


def read_data(indir):
    """
    Reads the data from all DAF files contained in subdirectories of user defined input directory 'indir' into one large
    array using routine from interface.py and then converts it to pandas dataframes. Calls functions to operate on
    dataframes, calculating associciated parameters. Sorts out non-physical results.

    Wishlist:
            - implement parsing of indir and outdir from command line

    :param indir: path of input folder. Usually itself with subfolders of observation dates which contain the DAF files.
    :return all_station_1: one dataframe containing all information required for analyses (minus shower/sporadic labels)
    """

    # Initialse empty lists
    all_df_1 = []
    all_df_2 = []

    data = read_daf_files(indir)

    # For loop to enter data structure created above, now in observation date folder containing the night's DAF files.
    for night in range(len(data)):
        # Create pandas data frame to store trajectory information for each meteor.
        df_1 = pd.DataFrame(data[night][0])
        df_2 = pd.DataFrame(data[night][1])

        # Create list of all dataframes.
        all_df_1.append(df_1)
        all_df_2.append(df_2)

        # Call per_data_manipulation function on each dataframes. Returns altered dataframe with added columns
        # calculated from raw data (e.g. absolute magnitude from apparent) and unnecessary columns deleted.
        per_station_manipulation(df_1)
        per_station_manipulation(df_2)

        # Call all_station_manipulation function on both dataframes. Returns both dataframes with new values appended
        # to df_1.
        all_station_manipulation(df_1, df_2)

    # Concatenate all dataframes from loop to one new dataframe.
    df = pd.concat(all_df_1, ignore_index=True)

    # Give index column title: 'Meteor'
    df.index.names = ['Meteor']

    # Housekeeping: count how many meteors are recorded with non-physical velocities or absolute magnitudes.
    sorted_out = len(df[((df['vel_avg'] < 10000) | (df['vel_avg'] > 72000) | (df['avg_abs_mag'] < -6))])

    # Housekeeping: remove meteors with non-physical velocities or absolute magnitudes.
    df = df[((df['vel_avg'] > 10000) & (df['vel_avg'] < 72000) & (df['avg_abs_mag'] > -6))]

    # Housekeeping: reset index after removing rows.
    df.reset_index(drop=True, inplace=True)

    # (temporary) Save new dataframe to csv file for clearer visual assessment than terminal.
    df.to_csv(r'E:\test_output\processed_data.csv')

    mass_tau(df)

    mass_halliday(df)

    return df, sorted_out


def flux_density_gruen(m):
    """
    Flux density as given by Gruen (1985). May eventually be moved to a util file.

    :param float m: mass in grams
    :return: Number of objects per metre squared per second
    """
    n = (2.2e3 * m ** 0.306 + 15.) ** (-4.38) \
        + 1.3e-9 * (m + 1e11 * m ** 2 + 1e27 * m ** 4) ** (-0.36) \
        + 1.3e-16 * (m + 1e6 * m ** 2) ** (-0.85)
    return n


# --------------------------------------------------------------------------------------------------
# Prepare parameters for plots
# --------------------------------------------------------------------------------------------------

def mass_tau(df):
    """
    Returns a calculated meteor mass as derived from using a constant luminous efficiency and the error in this value.

    :param df: dataframe containing all processed DAF data
    :return:
    """

    # Set constant luminous efficiency (tau).
    tau = 0.007

    # Calculate new value for meteor integrated luminosities using scatter plot fit parameters from
    # CILBO_debiasing_Drolshagen_Kretschmer. Unsure of exact origin, these exact values do not appear in SD and JK's
    # thesis.
    intg_luminosity = 10 ** (-0.39026606 * df['avg_abs_mag'] + 1.96769668) * 2.5

    # Calculate meteor mass [kg].
    mass = (2. / (tau * df['vel_avg'] ** 2)) * intg_luminosity

    # Calculate error in meteor mass.
    mass_err = abs(4 * tau ** (-1) * df['vel_avg'] ** (-3) * intg_luminosity) \
        + abs(2 * tau ** (-1) * df['vel_avg'] ** (-2) * df['intg_luminosity_err'])

    return mass, mass_err


def mass_halliday(df):
    """
    Returns a calculated meteor mass as derived by Halliday and the error in this value. This scheme uses a constant tau
    of 0.04 for meteors with velocities lower than or equal to 36km/s. For velocities greater than this a velocity-
    dependant relationship is used.

    :param df: dataframe containing all processed DAF data
    :return:
    """

    # Calculate new values for meteors' integrated luminosities using 'scatter plot fit parameters'. This is lifted
    # from CILBO_debiasing_Drolshagen_Kretschmer. I have so far been unable to locate the source of the parameters.
    intg_luminosity = 10 ** (-0.39026606 * df['avg_abs_mag'] + 1.96769668) * 2.5

    # 1. Divide meteors in required velocity bands.
    vel_1 = df.loc[(df['vel_avg'] <= 36000), 'vel_avg']

    vel_2 = df.loc[(df['vel_avg'] > 36000), 'vel_avg']

    # 2. Calculate the velocity dependant tau values for each velocity bracket
    tau_1 = 0.04

    tau_2 = 0.069 * (36 / (vel_2 / 1000)) ** 2

    # 3. Calculate the associated meteor mass [kg] for each velocity band using appropriate tau value.
    mass_1 = (2. / (tau_1 * vel_1 ** 2)) * intg_luminosity

    mass_2 = (2. / (tau_2 * vel_2 ** 2)) * intg_luminosity

    # 4. Calculate the associated uncertainty in meteor mass [kg] for each velocity band using appropriate tau value.
    mass_err_1 = abs(4. * tau_1 ** (-1) * vel_1 ** (-3) * intg_luminosity) \
        * 1 + abs(2. * tau_1 ** (-1) * vel_1 ** (-2) * df['intg_luminosity_err'])

    mass_err_2 = abs(4. * tau_2 ** (-1) * vel_2 ** (-3) * intg_luminosity) \
        * 1 + abs(2. * tau_2 ** (-1) * vel_2 ** (-2) * df['intg_luminosity_err'])

    # 5. Join the mass and uncertainty of 'vel_1' and 'vel_2' band meteors into one series each
    mass = mass_1.fillna(mass_2)
    mass_err = mass_err_1.fillna(mass_err_2)

    return mass, mass_err


def mass_ceplecha(df):
    """
    Calculates meteor mass as derived by the Ceplecha luminous efficiency scheme. This scheme divides meteors by
    velocity into four bands:

        vel_1: 10km/s < vel_avg <= 12.5km/s
        vel_2: 12.5km/s < vel_avg <= 17km/s
        vel_3: 17km/s < vel_avg <= 27km/s
        vel_4: 27km/s < vel_avg <= 72km/s

    and then calculates a velocity-dependant tau-function for each. These are then combined to give the masses of
    meteors in each velocity band. These values are then recombined in one series 'mass' and returned.

    Numbers appended to variables denote the velocity band to which the value belongs.

    :param df: dataframe containing all processed DAF data
    :return:
    """

    # Calculate new values for meteors' integrated luminosities using 'scatter plot fit parameters'. This is lifted
    # from CILBO_debiasing_Drolshagen_Kretschmer. I have so far been unable to locate the source of the parameters.
    intg_luminosity = 10 ** (-0.39026606 * df['avg_abs_mag'] + 1.96769668) * 2.5

    # 1. Divide meteors in velocity [m/s] bands.
    vel_1 = df.loc[(df['vel_avg'] <= 12500), 'vel_avg']

    vel_2 = df.loc[(df['vel_avg'] > 12500) & (df['vel_avg'] <= 17000), 'vel_avg']

    vel_3 = df.loc[(df['vel_avg'] > 17000) & (df['vel_avg'] <= 27000), 'vel_avg']

    vel_4 = df.loc[(df['vel_avg'] > 27000) & (df['vel_avg'] <= 72000), 'vel_avg']

    # 2. Calculate the velocity dependant tau values for each velocity band as per (Drolshagen & Kretschmer, 2015).
    tau_1 = 10. ** (-15.6 + 2.92 * np.log10(vel_1 / 1000)) * 15 * 1e9

    tau_2 = 10. ** (-13.24 + 0.77 * np.log10(vel_2 / 1000)) * 15 * 1e9

    tau_3 = 10. ** (-12.5 + 0.17 * np.log10(vel_3 / 1000)) * 15 * 1e9

    tau_4 = 10. ** (-13.69 * np.log10(vel_4 / 1000)) * 15 * 1e9

    # 3. Calculate the associated meteor mass for each velocity band using appropriate tau value.
    mass_1 = (2. / (tau_1 * vel_1 ** 2)) * intg_luminosity

    mass_2 = (2. / (tau_2 * vel_2 ** 2)) * intg_luminosity

    mass_3 = (2. / (tau_3 * vel_3 ** 2)) * intg_luminosity

    mass_4 = (2. / (tau_4 * vel_4 ** 2)) * intg_luminosity

    # 4. Join the masses of meteors from all velocity bands into one series 'mass'.
    mass = mass_1.fillna(mass_2).fillna(mass_3).fillna(mass_4)

    return mass


def mass_verniani(df):
    """
    Calculates meteor mass as derived by the Verniani scheme (Verniani, 1973). Velocities are converted into cgs units.
    The mass of the incoming meteors are the calculated in [g]. These masses are then converted to [kg] and returned.

    :param df: dataframe containing all processed DAF data
    :return:
    """

    # Convert velocities from [m/s] to [cm/s].
    vel_cgs = df['vel_avg'] * 100

    # Calculate mass of meteors [g].
    mass_cgs = 10 ** (-(df['avg_abs_mag'] - 64.09 + 10 * np.log10(vel_cgs)) / 2.5)

    # Convert mass from [g] to [kg]
    mass = mass_cgs * (10 ** (-3))

    return mass


def mass_weryk(df):
    """
    Calculates meteor mass as derived by the Weryk luminous efficiency scheme. Parameters as determined
    :param df:
    :return:
    """

    # Define some parameters as determined by fits to data (Weryk, 2013)
    tau_0 = 2.321882e-6
    vel_0 = 11484.8
    exp = 0.971

    # Select only velocities greater than zero point velocity parameter.
    vel = df.loc[(df['vel_avg'] > vel_0) & (df['vel_avg'] <= 72000), 'vel_avg']

    # Calculate the tau value from Weryk parameters.
    tau = tau_0 * (df['vel_avg'] - vel_0) ** exp

    # Calculate the assoicated mass for each meteor velocity and magnitude
    mass = (2. / (tau * vel ** 2)) * df['avg_abs_mag']

    return mass


def bin_mass(mass):
    """
    Function to bin the mass into logarithmic bins

    just give the mass values to the function and the min_range
    of each bin as well as the corresponding number in it is returned
    moreover the number has been cummulated already

    :param mass:
    :return:
        hist_mass
        min_bin_edges
        cum_hist_mass
    """
    range_min = min(mass)
    range_max = max(mass)

    bins = np.logspace(-10, 3, 50)

    new_bins = []

    for i in range(len(bins) - 1, 0, -1):

        if bins[i] > range_min:
            new_bins = new_bins + [bins[i]]
            i += 1
        else:
            new_bins = new_bins + [range_min]
            break

    new_bins_2 = []
    for i in range(len(new_bins) - 1, 0, -1):
        if new_bins[i] < range_max:
            new_bins_2 = new_bins_2 + [new_bins[i]]
            i += 1
        else:
            new_bins_2 = new_bins_2 + [range_max]
            break

    min_bin_edges = new_bins_2[0:-1]
    max_bin_edges = new_bins_2[1:int(len(new_bins_2))]

    hist_mass = []
    for i in range(len(min_bin_edges)):
        min_bin = min_bin_edges[i]
        max_bin = max_bin_edges[i]
        number_in_range = 0

        for j in range(0, len(mass)):
            if min_bin < mass[j] <= max_bin:
                number_in_range += 1

        hist_mass = hist_mass + [number_in_range]
        i += 1

    hist_mass[0] += 1

    # Cumulative Histogram Masses
    cum_hist_mass = np.cumsum(hist_mass[::-1])[::-1]

    return hist_mass, min_bin_edges, cum_hist_mass


# --------------------------------------------------------------------------------------------------
# Plot the flux densities
# --------------------------------------------------------------------------------------------------

# To do:    add flux densities from other luminous efficiences
#           specify dir for saving plots
#

def plot_flux_densities():
    import matplotlib.pyplot as plt

    # Generate the Gruen interplanetary meteoroid flux model for reference
    exponent = np.linspace(-6, 2, num=40, endpoint=False)
    masses_Gruen = 10. ** exponent

    gruenflux = []
    for mass in masses_Gruen:
        gruenflux.append(flux_density_gruen(mass))

    fig, flu = plt.subplots()

    # --------------------------------- Gruen flux as a reference ----------------------------------
    masses_Gruen *= 1e-3
    flu.loglog(masses_Gruen, gruenflux, 'g', linewidth=4, linestyle='--', label="Gruen (1985)")
    flu.set_xscale('log', nonposx='clip')
    flu.set_yscale('log', nonposy='clip')
    flu.set_xlabel('Meteoroid mass in kg')
    flu.set_ylabel(r'Cumulative number per $\mathregular{m^{2}s}$')
    flu.set_xlim(1e-8, 1e0)
    flu.set_ylim(1e-17, 1e-9)
    flu.grid(True)
    flu.legend()
    plt.show()


def run():
    # Quick and dirty 'run the script' on sample dataset
    indir = r"E:\tests"

    # Call read_data to read DAF files into a pandas dataframe and operate on it to obtain further data values.
    df, sorted_out = read_data(indir)

    # Call mass_tau to evaluate the mass as per the constant luminous efficiency scheme obtained by taking "a mean value of
    # [those] presented by [Hill et al., 2005] and [Ceplecha & McCrosky 1976]" (Drolshagen & Kretschmer, 2015).
    tau_mass, tau_mass_err = mass_tau(df)

    # Call mass_halliday to evaluate the mass as per the luminous efficiency scheme of Halliday et al. (1996).
    halliday_mass, halliday_mass_err = mass_halliday(df)

    # Call mass_ceplecha to evaluate the meteor mass as per the scheme of Ceplecha & McCrosky (1976).
    ceplecha_mass = mass_ceplecha(df)


    # Call mass_verniani to evaluate the meteor mass as per the scheme of Verniani (1973).
    verniani_mass = mass_verniani(df)

    # Call mass_weryk to evaluate the meteor mass as per the scheme of Weryk (2013).
    weryk_mass = mass_weryk(df)

    bin_mass(verniani_mass)

if __name__ == '__main__':
    # TODO: implement a proper argument parser and command line interface
    if PLOT_CUM_FLUX_DENSITY:
        plot_flux_densities()
    else:
        run()

