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
Tool to manage the VMO database . Functions available are:

    * create new database
    * drop database
    * create new reporter
    * list databases
    * count the records in each table of the VMO database

The command line usages is::

    usage: vmodbadmin.py [-h] [-c CONFIG] [-n DB_NAME] [-u DB_ADMIN_USR]
                         [-p DB_ADMIN_PWD] [-v]
                         [{create,drop,count,list,reporter}]

    VMO database manager

    positional arguments:
      {create,drop,count,list,reporter}

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            The configuration settings file. (default:
                            settings.py)
      -n DB_NAME, --name DB_NAME
                            The database name. (default: None)
      -u DB_ADMIN_USR, --username DB_ADMIN_USR
                            The database admin user. (default: None)
      -p DB_ADMIN_PWD, --password DB_ADMIN_PWD
                            The database admin user password. (default: None)
      -v, --verbose         Log with verbosity. (default: False)


Examples
--------

Create a VMO database::

    python vmodbadmin.py create -n vmo5 -u root -p lab****

Delete a VMO database::

    python vmodbadmin.py drop -n vmo5 -u root -p lab****

List existing database::

    python vmodbadmin.py list -u root -p lab****

Count records in database::

    python vmodbadmin.py count -n vmo5 -u root -p lab****

Add a new reporter::

    python vmodbadmin.py reporter -n vmo5 -u root -p lab****

    Please enter the following required fields:
    First name: Detlef
    Last name): Koschny
    Email: detlef.koschny@esa.int
    Country Code: NL
    Successfully inserted new reporter.
"""
from __future__ import print_function

import argparse
import getpass

from future.builtins import input

from mrg_core.util import config
from mrg_core.database.importer import Settings
from mrg_core.database.importer import VMODatabaseManager


def execute_command(opts):
    """ Execute the import command.

    :param Namespace opts: the option settings from argparse.
    """

    Settings.init_logger(level=opts.verbose)
    # if opts.command != 'list':
    #     assert opts.db_name, '--name is a required parameter'
    # assert opts.db_admin_usr, '--username is a required parameter'
    # assert opts.db_admin_pwd, '--password is a required parameter'
    #
    # db_conn = VMODatabaseManager(opts.db_name)
    kwargs = dict(opts.__dict__)
    del kwargs['verbose']
    del kwargs['config']
    del kwargs['command']
    # user name and password default to the database name
    if not kwargs['db_user']:
        kwargs['db_user'] = kwargs['db_name']
    if not kwargs['db_password']:
        kwargs['db_password'] = kwargs['db_name']

    db_conn = VMODatabaseManager(**kwargs)
    if opts.command == 'create':
        db_conn.create()
        db_conn.import_schema()

    elif opts.command == 'reporter':
        db_conn.reporter()

    elif opts.command == 'drop':
        result = db_conn.get_table_counts(opts.db_name)
        count = sum(result.values())
        print('The "%s" database has %d records.' % (opts.db_name, count))
        answer = input('Are you sure you want to delete this database (y/n)? ')
        if answer == 'y':
            db_conn.drop()
            print('Database deleted')

    elif opts.command == 'list':
        databases = db_conn.get_databases()
        for name in databases:
            print(name)

    elif opts.command == 'clear':
        db_conn.clear()

    elif opts.command == 'count':
        result = db_conn.get_table_counts(opts.db_name)
        for table in result:
            print('%-30s\t%d' % (table, result[table]))

    else:
        print('ERROR: "%s" invalid command.' % opts.command)

    db_conn.close()


def main():
    """ Main entry point of script """
    parser = argparse.ArgumentParser(description='VMO database manager',
                                     # formatter_class=argparse.ArgumentDefaultsHelpFormatter
                                     )

    parser.add_argument('command', choices=['create',
                                            'reporter',
                                            'drop',
                                            'list',
                                            'count',
                                            'clear'])

    parser.add_argument('-c', '--config', dest='config', type=str,
                        # default='settings.py',
                        help='The configuration settings file.')

    parser.add_argument('-n', '--name', dest='db_name', required=1,
                        help='The database name.')

    parser.add_argument('--host', dest='db_host', default='localhost',
                        help='The database server address.')

    parser.add_argument('--port', dest='db_port', default=0,
                        help='The database server port.')

    parser.add_argument('-e', '--engine', dest='db_engine', default='mysql',
                        help='The database type [mysql, sqlite].')

    parser.add_argument('-U', '--vmo-username', dest='db_user', default=None,
                        help='The vmo database manager.')

    parser.add_argument('-P', '--vmo-password', dest='db_password', default=None,
                        help='The database manager user password.')

    parser.add_argument('-u', '--username', dest='db_admin_user', default=None, required=1,
                        help='The database admin (root) user.')

    parser.add_argument('-p', '--password', dest='db_admin_password',
                        help='The database admin user password.')

    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='Log with verbosity.')

    opts = parser.parse_args()

    if opts.command == 'create':
        if not opts.db_user:
            opts.db_user = opts.db_name

        if opts.db_user and not opts.db_password:
            opts.db_password = getpass.getpass('Enter %s database password:' % opts.db_name)

    if opts.db_admin_user and not opts.db_admin_password:
        opts.db_admin_password = getpass.getpass('Enter admin password:')
    # config.get_settings(opts.config, opts, parser)
    # config.load_password_parameters(opts)

    execute_command(opts)


if __name__ == '__main__':
    main()
