""" MRG Virtual Interface
"""
from datetime import datetime

from mrg_core.util.interfaces.metrec import MRGMetRec
from mrg_core.util.interfaces.mrgsql import MRGSQL


class MRGVirtualIF(object):
    """
    This class implements a virtual interface that serves as middleware to
    access, using the same methods both an underlying database or a file
    system.  Currently, it is designed to work with a MySQL, SQLite database
    or with a file system following the standard MRG MetRec directory
    structure.

    Parameters
    ----------
    location: str
       Root path for the MRG source data directory or  Database string URI.

       The MRG directory structure is defined as path/<system_code>/YYMMDD/,
       where <system_code> is the code of the camera system used to obtain
       an observation, and YYMMDD is the session date (year, month, day).

       The typical form of a database URI is:

          dialect+driver://username:password@host:port/database

       In the case of MySQL, the preferred dialect+driver is "mysql+mysqldb:"
       while for SQLite, "sqlite:" should be used.  Note that if an
       absolute path is to be used for SQLite, the following URI should
       be used:

          sqlite:////absolute/path/to/database

       For a relative path, the following URI should be used instead:

          sqlite:///relative/path/to/database

    """
    def __init__(self, location):
        if '://' in location:
            self._data = MRGSQL(url=location)
        else:
            self._data = MRGMetRec(path=location)

    def get_parallel_observation(self, sys_a, sys_b, begdate, enddate, delta):
        """
        Generator method that creates an iterator that produces a tuple of
        Panda's DataFrames with the data obtained simultaneously by the camera
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

        Yields
        ------
        tuple
           Every time this method is called, it returns a tuple
           (DataFrame, DataFrame) where the first DataFrame contains the
           recorded data for the parallel observation as obtained by the
           camera system ``sys_a``, and the second DataFrame contains the
           equivalent for ``sys_b``.

        """
        # Find the events recorded by the two camera systems simultaneously.
        events = self._data.get_parallel_events(sys_a, sys_b,
                                                begdate, enddate, delta)

        # Return, for each of the parallel events found for the current
        # date, a tuple with two DataFrames, if the position data (INF
        # file) exists.
        for time_sys_a, time_sys_b in events.itertuples(index=False):
            dfa = self.get_position(sys_a, time_sys_a)
            dfb = self.get_position(sys_b, time_sys_b)

            if len(dfa) and len(dfb):
                yield dfa, dfb

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
        return self._data.get_position(system, event)
