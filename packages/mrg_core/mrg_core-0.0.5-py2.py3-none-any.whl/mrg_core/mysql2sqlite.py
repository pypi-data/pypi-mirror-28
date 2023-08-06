#   --------------------------------------------------------------------------
#   Copyright 2017 SRE-F, ESA (European Space Agency)
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
#   --------------------------------------------------------------------------
""" This script converts a mysql dump file to a SQLite3 database.

To dump a mysql database use the command line::

    # export/import schema into sqlite
    mysqldump -uvmo -pvmopass --no-data -r vmo_schema.sql vmo
    python mysql2sqlite.py -i vmo_schema.sql -o vmo.db -v -y

    # export/import lookup table data
    mysqldump -uvmo -pvmopass --no-create-info -r vmo_data_init.sql vmo \
        country entry_source entry_status
    python mysql2sqlite.py -i vmo_data_init.sql -o vmo.db

Command line usage::

    $ python mysql2sqlite.py -h
    usage: mysql2sqlite.py [-h] -i INPUT_FILE -o OUTPUT_FILE [-y] [-v]

    MySQL dump to Sqlite3 database converter

    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT_FILE, --input-file INPUT_FILE
                            the mysql dump file. (default: None)
      -o OUTPUT_FILE, --output-file OUTPUT_FILE
                            the mysql dump file. (default: None)
      -y, --overwrite       Overwrite existing sqlite database. (default: False)
      -v, --verbose         Log with verbosity. (default: False)

"""

from __future__ import print_function

import sys
import os
import re

import logging
import shlex
import argparse

import sqlite3


def mysql_to_sqlite_syntax(sql):
    """ Convert the mysql sql syntax to sqlite compatible syntax.

    :param str mysql_sql:
    :return: the sqlite sql statement(s)
    """

    # TODO: there may be compatibility issues with the following,
    # - regular expressions are case sensitive
    # - back quotes are expected for table and column names
    # - there may be line termination character differences depending on O/S.
    # - this routine has only been tested on MySQL 5.7.16, for Win64

    sql = re.sub(r'^LOCK TABLES.*\n?', '', sql, flags=re.MULTILINE)
    sql = re.sub(r'^UNLOCK TABLES.*\n?', '', sql, flags=re.MULTILINE)
    sql = re.sub(r'^\) ENGINE.*\n?', ');\n', sql, flags=re.MULTILINE)
    sql = re.sub(r'unsigned NOT NULL AUTO_INCREMENT', 'NOT NULL', sql,
                 flags=re.MULTILINE)

    # extract the table and key lines from the mysql dump
    table_keys_expr = r'^CREATE TABLE `(?P<table>.*)`.*\n?|' \
                      r'^  (?P<unique>.*)KEY `(?P<id>.*)` \(`(?P<key>.*)`.*\n?'
    table_keys_re = re.compile(table_keys_expr, flags=re.MULTILINE)
    result = [entry.groupdict() for entry in table_keys_re.finditer(sql)]

    curr_table = None
    indexes = []
    for entry in result:
        if entry['table']:
            curr_table = entry['table']
        else:
            if entry['key'] == 'prefix`(255),`prefix_no':
                # TODO: VMO specific!!!
                entry['key'] = 'prefix`,`prefix_no'
                # continue
            entry['table'] = curr_table
            if entry['unique']:
                idx = 'CREATE UNIQUE INDEX `{id}` ON {table} (`{key}`);'.format(**entry)
            else:
                idx = 'CREATE INDEX `{id}` ON {table} (`{key}`);'.format(**entry)
            logging.debug(idx)
            indexes.append(idx)

    # remove the KEY and UNIQUE KEY lines
    sql = re.sub(r',\r?\n  .*KEY `.*` \(.*\)', '', sql, flags=re.MULTILINE)

    # append the CREATE INDEX lines to the end of the SQL
    sql += '\n' + '\n'.join(indexes)
    logging.info('Found %d indexes', len(indexes))

    # replace any encoded single quotes and replace them with forward ticks.
    quotes_len = sql.count("\\'")
    if quotes_len:
        logging.warning('Escaping %d single quote to 2 single quote '
                        'characters', quotes_len)
    sql = sql.replace("\\'", "''")

    return sql


def mysqldump_to_sqlite(mysql_dump_file, sqlite_file, overwrite=False):
    """ Routine to convert a mysql dump file to an sqlite3 database.

    :param str mysql_dump_file: the path to the mysql dump file
    :param str sqlite_file: the path to the
    :param bool overwrite:
    :raises sqlite3.DatabaseError:
    """

    # Delete the existing database if specified
    if os.path.isfile(sqlite_file):
        if overwrite:
            os.remove(sqlite_file)
        else:
            logging.info('Sqlite database already exists. Appending to it.')

    # check that the dump file exists
    if not os.path.isfile(mysql_dump_file):
        raise sqlite3.DatabaseError('mysql dump file does not exist: %s'
                                    % mysql_dump_file)

    with open(mysql_dump_file, 'rb') as file_obj:
        sql = file_obj.read()

    sql = mysql_to_sqlite_syntax(sql)

    if logging.root.getEffectiveLevel() == logging.DEBUG:
        debug_file = sqlite_file + '.debug'
        if os.path.exists(debug_file):
            os.remove(debug_file)
        with open(debug_file, 'wb') as file_obj:
            file_obj.write(sql)

    try:
        sqlite3.complete_statement(sql)
    except sqlite3.DatabaseError:
        raise

    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    try:
        cursor.executescript(sql)
    except sqlite3.DatabaseError:
        raise
    finally:
        cursor.close()


def main(cmdline=None):
    """ The main entry point for this script.

    :param str cmdline: if set, then this command line string will override
        the console command line input. Useful for debugging.
    """
    args = shlex.split(cmdline) if cmdline else None
    desc = 'MySQL dump to Sqlite3 database converter'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-i', '--input-file', required=True,
                        help='the mysql dump file.')
    parser.add_argument('-o', '--output-file', required=True,
                        help='the sqlite output file.')
    parser.add_argument('-y', '--overwrite', action='store_true',
                        help='Overwrite existing sqlite database.')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='Log with verbosity.')
    opts = parser.parse_args(args)

    logging.basicConfig(level=[logging.INFO, logging.DEBUG][opts.verbose])

    try:
        mysqldump_to_sqlite(opts.input_file, opts.output_file, opts.overwrite)
        return 0
    except sqlite3.DatabaseError as exc:
        logging.exception(exc)
        return -1


if __name__ == '__main__':
    sys.exit(main())
