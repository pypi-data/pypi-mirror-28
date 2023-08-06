""" MRG SQL Interface
"""
from datetime import datetime
import re

import pandas

_TDIFF = {
    'sqlite': "strftime('%s',cam1.time) - strftime('%s',cam2.time)",
    'mysql': "cam1.time - cam2.time"
}


class MRGSQL(object):
    """
    This class provides the implementation of the database interface, in
    accordance with the database schema described in the WGN, The Journal
    of the IMO 38:1 (2010).

    Parameters
    ----------
    url: str
       Database string URI.  The typical form of a database URI is:

          dialect+driver://username:password@host:port/database

       In the case of MySQL, the preferred dialect+driver is "mysql+mysqldb:"
       while for SQLite, "sqlite:" should be used.  Note that if an
       absolute path is to be used for SQLite, the following URI should
       be used:

          sqlite:////absolute/path/to/database

       For a relative path, the following URI should be used instead:

          sqlite:///relative/path/to/database

    """
    def __init__(self, url):

        # Extract the 'dialect' from the URI.
        self._db = re.split(r'[+:]', url, maxsplit=1)[0]
        self._con = url

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
        ------
        DataFrame
           providing the complete list of times of meteor detection events
           recorded simultaneously by the camera system ``sys_a`` and
           ``sys_b``, where the first DataFrame's column ("time_a") contains
           the recorded time for the parallel observation as obtained by the
           camera system ``sys_a``, and the second DataFrame' column
           ("time_b") contains the equivalent for ``sys_b``.

        """
        # Find the parallel events on the database
        events = pandas.read_sql(
            sql='SELECT cam1.time as time_a, cam2.time as time_b '
                'FROM '
                '(SELECT meteor_code, system_code, time '
                ' FROM cam_meteor INNER JOIN cam_session '
                ' WHERE cam_session.system_code="{0}" '
                ' AND cam_session.entry_code=cam_meteor.entry_code '
                ' AND cam_meteor.time <= "{1}" '
                ' AND cam_meteor.time >= "{2}") cam1 '
                'JOIN '
                '(SELECT meteor_code, system_code, time '
                ' FROM cam_meteor INNER JOIN cam_session '
                ' WHERE cam_session.system_code="{3}" '
                ' AND cam_session.entry_code=cam_meteor.entry_code '
                ' AND cam_meteor.time <= "{1}" '
                ' AND cam_meteor.time >= "{2}") cam2 '
                'ON ABS({4}) <= {5} '.format(sys_a, enddate, begdate,
                                             sys_b, _TDIFF[self._db], delta),
            con=self._con)

        return events

    def get_position(self, system, event):
        """
        Returns a Pandas' data-frame that contains the following columns for
        the meteor observation that was recorded by the camera ``system`` at
        the input date/time ``event``:
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

        This interface provides the same data-frame as the file parser class
        MetRecInfFile.

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
        # SQLite does not store times as datetime64[ns].  Force the column
        # "time" to be datatime64[ns] data type.
        result = pandas.read_sql(
            sql='SELECT pos_no, cam_pos.time, cam_pos.mag, '
                'pos_x, pos_y, pos_ra, pos_dec '
                'FROM cam_session INNER JOIN cam_meteor '
                'INNER JOIN cam_pos '
                'WHERE cam_session.system_code="{}" AND '
                'cam_session.entry_code=cam_meteor.entry_code AND '
                'cam_meteor.time="{}" AND '
                'cam_meteor.meteor_code=cam_pos.meteor_code'
                ''.format(system, event),
            con=self._con,
            parse_dates=['time'])

        return result
