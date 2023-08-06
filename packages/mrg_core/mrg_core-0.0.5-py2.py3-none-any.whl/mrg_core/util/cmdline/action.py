""" Module for extended type of actions to be taken for different command
    line arguments that are available in the MRG extension of the argparse
    standard library.

"""
import argparse
from datetime import datetime
import os

import sqlalchemy


class CheckDate(argparse.Action):
    """
    Class that supports the argument parsing of the command line input dates.

    The ``init`` method checks that no arguments are passed onto the class,
    while the ``call`` method checks that the date is valid and returns a
    datetime object.
    """

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs is not allowed")
        super(CheckDate, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):

        # Check if the date valid
        try:
            date = datetime.strptime(values, '%Y%m%d')
        except ValueError:
            exit('ValueError: Input date <%s> for command line option "%s" '
                 'does not follow the YYYYMMDD format.'
                 % (values, option_string))
        else:
            setattr(namespace, self.dest, date.strftime('%Y%m%d'))


class CheckDir(argparse.Action):
    """
    Class that supports the argument checking of the command line directories.

    The ``init`` method checks that no arguments are passed onto the class,
    while the ``call`` method checks that the directory provided in the
    command line exists and returns the validated directory path.
    """

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs is not allowed")
        super(CheckDir, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):

        #
        # Check that the directory exists
        #
        if os.path.isdir(values):
            setattr(namespace, self.dest, values)
        else:
            exit('IOError: Directory <%s> provided in command line option '
                 '"%s" does not exist.' % (values, option_string))


class CheckSrc(argparse.Action):
    """
    Class that supports the argument checking of the command line data sources.

    The ``init`` method checks that no arguments are passed onto the class,
    while the ``call`` method checks that the data source provided in the
    command line exists and returns the validated source.
    """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs is not allowed")
        super(CheckSrc, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):

        if '://' in values:
            # Check that the driver is not MySQLdb
            if 'MySQLdb' in values:
                exit('NotSupported: The driver MySQLdb is not supported. Use '
                     'pymysql instead.')

            # Check that we have connection to the DB
            try:
                connection = sqlalchemy.create_engine(values).connect()
                connection.execute("SELECT * FROM country")
            except (ImportError, sqlalchemy.exc.NoSuchModuleError) as exc:
                exit('ImportError: The dialect+driver combination provided '
                     'in the Source URI <{0}> provided in command line option '
                     '"{1}" is not supported. {2}.'
                     ''.format(values, option_string, exc))
            except (ValueError, sqlalchemy.exc.ArgumentError):
                exit('ValueError: Source URI <{}> provided in command line '
                     'option "{}" is not properly formed.'
                     ''.format(values, option_string))
            except sqlalchemy.exc.OperationalError:
                exit('IOError: Data source addressed by URI <{}> in command '
                     'line option "{}" is not reachable.'
                     ''.format(values, option_string))
            else:
                connection.close()
                setattr(namespace, self.dest, values)

        else:
            # Check that the directory exists
            if os.path.isdir(values):
                setattr(namespace, self.dest, values)
            else:
                exit('IOError: Directory <{}> provided in command line '
                     'option "{}" does not exist.'.format(values,
                                                          option_string))
