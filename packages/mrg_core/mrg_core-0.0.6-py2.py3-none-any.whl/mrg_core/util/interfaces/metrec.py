""" MRG MetRec File System Interface
"""
from datetime import datetime
from datetime import timedelta
import logging
import os

import numpy as np
import pandas as pd
from pandas import DataFrame


from mrg_core.util.interfaces import MetRecInfFile
from mrg_core.util.interfaces import MetRecLogFile
from mrg_core.util.diriter import SystemSessionIterator


class MRGMetRec(object):
    """
    This class provides the implementation of the file system interface,
    following the directory structure and file formats defined for the
    MRG and MetRec respectively.

    Parameters
    ----------
    path: str
       Root path for the MRG directory.  The MRG directory structure is
       defined as path/<system_code>/YYMMDD/, where <system_code> is the
       code of the camera system used to obtain an observation, and
       YYMMDD is the session date (year, month, day).

    """
    def __init__(self, path):
        self._path = path

    def get_parallel_events(self, sys_a, sys_b, begdate, enddate, delta):
        """
        Returns a Panda's DataFrames with all times (as datetime objects)
        of meteor detection events recorded simultaneously by the camera
        systems ``sys_a`` and ``sys_b`` between the dates ``begdate`` and
        ``enddate``.  A meteor detection event will be considered to have
        been recorded simultaneously by the two camera system if the absolute
        time difference between the recorded time from each camera is less
        than the given ``delta`` seconds, i.e.::

             | time_system_a - time_system_b | < delta

        Parameters
        ----------
        sys_a: str
           Code of the first camera system used to obtain the simultaneous
           observation.
        sys_b: str
           Code of the first camera system used to obtain the simultaneous
           observation.
        begdate: datetime
           Start date for the search of parallel observations, in UTC.
        enddate: datetime
           End date for the search of parallel directories, in UTC.
        delta: int
           Maximum allowable time different between the recording times of a
           given meteor from the camera systems ``sys_a`` and ``sys_b`` to
           consider the event to be a simultaneous observation of the meteor.

        Returns
        -------
        DataFrame
           providing the complete list of times of meteor detection events
           recorded simultaneously by the camera system ``sys_a`` and
           ``sys_b``, where the first DataFrame's column ("time_a") contains
           the recorded time for the parallel observation as obtained by the
           camera system ``sys_a``, and the second DataFrame' column
           ("time_b") contains the equivalent for ``sys_b``.

        """
        # Find the directories that contain potential parallel meteor
        # detections, within the requested time range.
        fromdate = begdate.strftime('%Y%m%d')  # beddate str (YYYYMMDD format)
        todate = enddate.strftime('%Y%m%d')    # enddate str (YYYYMMDD format)
        parallel_dirs = self._parallel_dirs(sys_a, sys_b, fromdate, todate)

        events = DataFrame(columns=['time_a', 'time_b'])
        for (path1, path2, _, logfile) in parallel_dirs:
            # Find the times for meteors which were seen by both cams and
            # append the result to the existing DataFrame.
            events = events.append(
                self._parallel_events(path1, path2, logfile, delta))

        # Filter the whole data set using the begdate and enddate provided by
        # the user.
        return events[(events['time_a'] >= begdate) &
                      (events['time_a'] <= enddate) &
                      (events['time_b'] >= begdate) &
                      (events['time_b'] <= enddate)]

    def get_position(self, system, event):
        """
        Returns a Pandas' data-frame that contains the following columns for
        the meteor observation that was recorded at the input date/time:
           - pos_no:  number of the position data record, counted from 1.  It
                      corresponds with the frame number of a given observation
                      from MetRec.
           - time:    Time of the position, accurate to one frame/exposure, in
                      Universal time.
           - mag:     The apparent magnitude of the meteor at this position.
           - pos_x:   Horizontal position of the meteor within the exposure.
                      This should be a relative value between 0 and 1.
           - pos_y:   Vertical position of the meteor within the exposure.
                      This should be a relative value between 0 and 1.
           - pos_ra:  Right ascension of the meteor, in decimal degrees.
           - pos_dec: Declination of the meteor, in decimal degrees.

        Parameters
        ----------
        system: str
           Code of the camera system used to obtain the observation.
        event: datetime
           Time when the meteor was first detected, in Universal Time.

        Returns
        -------
        DataFrame
           Panda's DataFrame that contains as many rows as data points
           recorded in the observation.  For each data point, the position
           number, the time, the magnitude of the meteor, the location in x,y
           coordinates within the frame and the right ascension and
           declination of the meteor are provided.

        """
        labels = ['pos_no', 'time', 'mag', 'pos_x', 'pos_y',
                  'pos_ra', 'pos_dec']

        # Create the complete path to the MetRec INF file.
        filename = self._create_path(system, event)

        # If there is no file associated with the requested event, return an
        # empty DataFrame.
        if not filename:
            return DataFrame(columns=labels)

        # Parse the file.
        inf_file = MetRecInfFile(path=filename, camera=system)

        # Create a Pandas' DataFrame with the usable data.
        result = DataFrame([row for row in inf_file.rawdata if row['use']])

        # Rename DataFrame's column to match the MRG database schema.
        result = result.rename(columns={'#': 'pos_no', 'bright': 'mag',
                                        'x': 'pos_x', 'y': 'pos_y',
                                        'alpha': 'pos_ra', 'delta': 'pos_dec',
                                        'time': 'seconds', 'timestamp': 'time'})

        # Filter out the columns that are not currently required.
        result = result[labels]

        # Force the "time" column to be datetime64[ns] data type.
        result['time'] = pd.to_datetime(result['time'])  # .astype('datetime64[ns]')

        # Convert the units of pos_ra from decimal hours to decimal degrees
        result['pos_ra'] = result['pos_ra'] / 24.0 * 360.0

        # Modify the position # (pos_no) to start from 1 and be continuous.
        result['pos_no'] = range(1, len(result) + 1)
        # Force the "pos_no" column to be int64 data type.
        result['pos_no'] = result['pos_no'].astype('int64')

        return result

    def _create_path(self, system, event):
        """
        Returns the path to the INF file that contains the data corresponding
        to the ``event`` recorded by the camera ``system``.

        Depending on where MetRec has been used to record the data, a file for
        a given date could be stored in the directory of the previous date.
        This is the case when an observational session starts before UTC
        midnight and runs into the next day.

        Sometimes it is also possible that the MetRec Log file (from where
        generally an event is selected) rounds up the time of a meteor while
        the INF file name doesn't.

        Parameters
        ----------
        system: str
           Code of the camera system used to obtain the observation.
        event: datetime
           Time when the meteor was first detected, in Universal Time.

        Returns
        -------
        str or NoneType
           Path (absolute or relative) to the INF file that contains the data
           associated with the requested ``event`` for the camera ``system``.

        """
        # Create folder names based on the provided date or one day earlier.
        dirs = [event.strftime('%Y%m%d'),
                (event - timedelta(days=1)).strftime('%Y%m%d')]
        # Create file names based on the provided time or one second earlier.
        names = [event.strftime('%H%M%S.inf'),
                 (event - timedelta(seconds=1)).strftime('%H%M%S.inf')]

        # Check for the existence of the file, in the following order:
        #   1. Folder and name based on the provided date/time
        #   2. Folder based on one day earlier, name based on provided time.
        #   3. Folder based on provided date, name based on one sec earlier.
        #   4. Folder and name based on day earlier/sec earlier.
        for name in names:
            for folder in dirs:
                path = os.path.join(self._path, system, folder, name)
                if os.path.exists(path):
                    return path

        # If everything fails, return None
        return None

    def _parallel_dirs(self, cam1, cam2, begdate, enddate):
        """
        Generator protected method that creates an iterator that produces a
        sequence of parallel directories found for the dates between
        ``begdate`` and ``enddate`` and the camera systems ``cam1`` and
        ``cam2``.

        Parameters
        ----------
        cam1: str
           Camera system #1 identifier, e.g. 'ICC7' or 'ICC9'.
        cam2: str
           Camera system #2 identifier, e.g. 'ICC7' or 'ICC9'.
        begdate: str
           Start date for the search of parallel directories. ``begdate`` shall
           conform to the YYYYMMDD format.
        enddate: str
           End date for the search of parallel directories. ``enddate`` shall
           conform to the YYYYMMDD format.

        Yields
        ------
        tuple
           Every time the method is called, it returns  tuple
           (path1, path2, date, logfile) where ``path1`` is the path
           corresponding to the camera system #1, ``path2`` is the path
           corresponding to the camera system #2, for the given ``date``.
           ``logfile`` is the file name of the corresponding MetRec Log File
           found in both ``path1`` and ``path2`` directories.

        """

        # Use Pandas' DataFrames to find parallel directories.
        srcs = DataFrame([item for item in SystemSessionIterator(self._path)],
                         columns=['path', 'year', 'date', 'camera'])

        # Filter the data within the DataFrame, by date and camera systems.
        dirs = srcs[(srcs['date'] <= enddate) & (srcs['date'] >= begdate) &
                    ((srcs['camera'] == cam1) | (srcs['camera'] == cam2))]

        # Keep the rows that have the same 'date' value and sort the values by
        # date first, and then by camera system.
        parl = dirs[
            dirs.duplicated(subset='date', keep=False)
        ].sort_values(['date', 'camera'], ascending=[True, True])

        i = 0
        while i < len(parl):
            logfile = parl.iloc[i]['date'] + '.log'
            if (os.path.isfile(os.path.join(parl.iloc[i]['path'], logfile)) and
                    os.path.isfile(os.path.join(parl.iloc[i+1]['path'], logfile))):

                yield (parl.iloc[i]['path'], parl.iloc[i+1]['path'],
                       parl.iloc[i]['date'], logfile)
            else:
                logging.error('MetRec Log File %s is not present in either %s or '
                              '%s input directories', logfile,
                              parl.iloc[i]['path'], parl.iloc[i+1]['path'])

            i += 2

    @staticmethod
    def _parallel_events(path1, path2, logfile, delta):
        """
        Returns a Panda's DataFrame with all the date and times of parallel
        events recorded by two camera systems, A (with data stored in
        ``path1``) and B (with data stored in ``path2``) and a common
        ``logfile``.  A meteor detection event will be considered to have been
        recorded simultaneously by the two camera system if the absolute time
        difference between the recorded time from each camera is less than the
        given ``delta`` seconds, i.e.::

             | time_system_A - time_system_B | < delta


        Parameters
        ----------
        path1: str
           Path (absolute or relative) to the directory where the recorded
           data for the camera system A is stored.
        path2: str
           Path (absolute or relative) to the directory where the recorded
           data for the camera system B is stored.
        logfile: str
           The file name of the MetRec Log File found in both ``path1`` and
           ``path2`` directories.
        delta: int
           Maximum allowable time different between the recording times of a
           given meteor from the camera systems A (associated with ``path1``)
           and B (associated with ``path2``) to consider the event to be a
           simultaneous observation of the meteor.

        Yields
        ------
        DataFrame
           providing the complete list of times of meteor detection events
           recorded simultaneously, where the first column is a datetime
           object that provides the date/time recorded by the camera system A
           and the second column, the date/time recorded by the camera system
           B, for the identified parallel event.

        """
        session_c1 = MetRecLogFile(path=os.path.join(path1, logfile))
        session_c2 = MetRecLogFile(path=os.path.join(path2, logfile))

        # Get the meteor detection event DataFrames for each camera system and
        # make their index the 'timestamp'
        events_c1 = session_c1.meteors.set_index('timestamp')
        events_c2 = session_c2.meteors.set_index('timestamp')

        # Create an auxiliary DataFrame where the index (rows) are the
        # timestamps from the meteor events from camera system 1, and the
        # columns, the timestamps for the meteor events from camera system 2,
        # and each cell is either True(False) depending on whether the
        # difference between the two timestamps is less(more) than the delta secs
        events = DataFrame({
            col: abs(events_c1.index.values - col) <= np.timedelta64(delta, 's')
            for col in events_c2.index.values
        }, index=events_c1.index.values)

        # Create a  DataFrame stacking the columns as inner-indexes.
        events = events.stack().to_frame()

        # Filter by the columns that are True and unstack the indexes in order
        # to build the output DataFrame. Note that the outer index is the
        # timestamp for the camera system 1, and the inner is the one for
        # camera system 2.
        events = events[events[0]].reset_index().rename(
            columns={'level_0': 'time_a', 'level_1': 'time_b'})

        # Return the DateFrame.
        return events[['time_a', 'time_b']]
