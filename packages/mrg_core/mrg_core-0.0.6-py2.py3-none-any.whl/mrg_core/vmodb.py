#!/usr/bin/env python
#   --------------------------------------------------------------------------
#   Copyright 2013 SRE-F, ESA (European Space Agency)
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
Tool to manage the VMO database. Functions available are:

    * validate sessions before import into database
    * import sessions into the database
    * remove sessions from database

The command line usages is::

    usage: vmodb.py [-h] [-c CONFIG] [-r MML_REPORTER] -d DIRECTORY [-o OUTPUT]
                    [-A] [-C] [-F] [-S] [-v]
                    [{validate,import,remove,export}]

    VMO database import script

    positional arguments:
      {validate,import,remove,export}

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            The configuration settings file. (default:
                            settings.py)
      -r MML_REPORTER, --reporter MML_REPORTER
                            The observer code located in the shared_observer
                            table. (default: None)
      -d DIRECTORY, --directory DIRECTORY
                            The input directory to process. (default: None)
      -o OUTPUT, --output OUTPUT
                            The log output file. (default: /tmp/vmodb.txt)
      -A, --auto-remove     If the entry already exists in the database, then
                            remove it. (default: False)
      -C, --commit          Commit changes to the database and add or remove any
                            data files. (default: False)
      -F, --sync-files      Copy/remove the data files into the http directory.
                            Example: /export/vmoftp/CAM/METREC/2016/20160701/ICC7
                            (default: False)
      -S, --skip-existing   If the entry already exists in the database, then skip
                            it. (default: False)
      -v, --verbose         Log with verbosity. (default: False)


Examples
--------

Import into VMO database (the /commit/ and /skip-existing/ flags are on)::

    python vmodb.py import -c settings_mine.txt -r KOSDE -d C:/cilbo_test/data_vmo/ICC7/201607?? -CS


MySQL Queries
-------------

Select statement to join all meteor position information::

    USE vmo3;

    SELECT *
    FROM cam_pos
        INNER JOIN cam_meteor on cam_meteor.meteor_code=cam_pos.meteor_code
        INNER JOIN cam_period on cam_period.entry_code=cam_meteor.entry_code
        INNER JOIN cam_session on cam_session.entry_code=cam_period.entry_code

    WHERE system_code='ICC7'
    ;


"""
from __future__ import print_function

import argparse
import sys
import logging
import time
import datetime
import os

from mrg_core.util import config
from mrg_core.database.importer import Settings
from mrg_core.database.importer import DatabaseConnection
from mrg_core.database.importer import DirectoryProcessor


def check_reporter(db_conn, reporter):
    """ Tests if the reported is listed in the observer table. This
    is needed for `import` command.

    :param DatabaseConnection db_conn: the database connection
    :param str reporter: the reporter code, i.e. ANON, SMIHA, KOSDE"""
    sql_select = "SELECT * FROM observer WHERE observer_code = '%s'" % reporter
    row = db_conn.execute_get_row(sql_select)
    if row is None:
        print('ERROR: reported does not exist.')
        print('Please use the following script to register a new reporter,')
        print('  python vmodbadmin.py reporter')
        sys.exit(-1)


def execute_command(opts):
    """ Execute the import command.

    :param Namespace opts: the option settings from argparse.
    """
    time_0 = time.time()
    Settings.init_logger(log_file=opts.output, level=opts.verbose)

    if opts.command in ['validate', 'import', 'remove']:
        if Settings.db_conn is None:
            # user name and password default to the database name
            Settings.db_conn = DatabaseConnection(vault=None, **opts.__dict__)
        Settings.skip_existing = opts.skip_existing
        # Settings.mml_cmdline = opts.mml_cmdline
        Settings.mml_reporter = opts.mml_reporter
        Settings.commit = opts.commit
        Settings.sync_files = opts.sync_files

    if not opts.command:
        print('ERROR: command missing')

    elif opts.command == 'export':
        pass

    elif opts.command == 'validate':
        print('processing directory:', opts.directory)
        Settings.summary_only = True
        check_reporter(Settings.db_conn, Settings.mml_reporter)
        processor = DirectoryProcessor(opts.directory, opts.mml_save, opts.remove_empty_positions)
        processor.process_directory_tree(continue_from_path=None)

    elif opts.command == 'import':
        print('processing directory:', opts.directory)
        Settings.summary_only = False
        check_reporter(Settings.db_conn, Settings.mml_reporter)
        processor = DirectoryProcessor(opts.directory, opts.mml_save, opts.remove_empty_positions)
        processor.process_directory_tree(continue_from_path=None)

    elif opts.command == 'remove':
        # NOTE: this only effects the copied files in the directory:
        #   /export/vmoftp/CAM/METREC
        # even when the input directory is used.
        # NO RAW "SOURCE" DATA WILL EVER BE DELETED!
        print('processing directory:', opts.directory)
        Settings.summary_only = False
        processor = DirectoryProcessor(opts.directory)
        processor.remove()

    time_d = time.time() - time_0
    print('Finished in: %s' % str(datetime.timedelta(seconds=time_d)))


def main():
    """ Main entry point of script. """
    config_file = None
    for i, arg in enumerate(sys.argv):
        if arg == '-c' or arg == '--config':
            if i+1 < len(sys.argv):
                config_file = sys.argv[i+1]
    opts = config.get_settings(config_file)
    # NOTE: the opts dict should be used to set default values in the ArgumentParser

    parser = argparse.ArgumentParser(description='VMO database import script',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('command', nargs='?',
                        choices=['validate', 'import', 'remove', 'export'])

    parser.add_argument('-db', '--db-url', dest='db_url',
                        help='The database url. Format: mysql://<uid>:<pwd>@<host>:<port>/<dbname>'
                             'Example: mysql:///vmo4')

    parser.add_argument('-c', '--config', dest='config', type=str,
                        # default='settings.py',
                        help='The configuration settings file.')

    parser.add_argument('-r', '--reporter', dest='mml_reporter', type=str,
                        default='ANON', required=False,
                        # required='reporter' not in opts,
                        help='The observer code located in the observer table.')

    parser.add_argument('-d', '--directory', dest='directory', type=str,
                        required='directory' not in opts,
                        help='The input directory to process.')

    parser.add_argument('-B', '--session-begin', dest='session_begin', type=str,
                        help='The night session YYYYMMDD start date.')

    parser.add_argument('-E', '--session-end', dest='session_end', type=str,
                        help='The night session YYYYMMDD end date.')

    parser.add_argument('-o', '--output', dest='output', type=str,
                        default='/tmp/vmodb.txt',
                        help='The log output file.')

    parser.add_argument('-A', '--auto-remove', dest='auto_remove', action='store_true',
                        help='If the entry already exists in the database, then remove it.')

    parser.add_argument('-C', '--commit', dest='commit', action='store_true',
                        help='Commit changes to the database and add or remove any data files.')

    parser.add_argument('-F', '--sync-files', dest='sync_files', action='store_true',
                        help='Copy/remove the data files into the http directory. '
                             'Example: /export/vmoftp/CAM/METREC/2016/20160701/ICC7')

    parser.add_argument('-S', '--skip-existing', dest='skip_existing', action='store_true',
                        help='If the entry already exists in the database, then skip it.')

    parser.add_argument('-M', '--mml-save', dest='mml_save', action='store_true',
                        help='Save the XML mml file (useful for debugging).')

    parser.add_argument('-R', '--remove-empty-positions', dest='remove_empty_positions', action='store_true',
                        help='Does not import meteors that have no positions associated with it.')

    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='Log with verbosity.')

    opts = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)-7s %(message)s',
                        level=[logging.INFO, logging.DEBUG][opts.verbose])
    if opts.config:
        config.get_settings(opts.config, opts)
        config.load_password_parameters(opts)

    if opts.session_begin and opts.session_end:
        date_0 = datetime.datetime.strptime(opts.session_begin, '%Y%m%d')
        date_1 = datetime.datetime.strptime(opts.session_end, '%Y%m%d')
        directory = opts.directory
        date_i = date_0
        while date_i <= date_1:
            night = date_i.strftime('%Y%m%d')
            opts.directory = os.path.join(directory, night)
            execute_command(opts)
            date_i += datetime.timedelta(days=1)
    else:
        execute_command(opts)


if __name__ == '__main__':
    main()
