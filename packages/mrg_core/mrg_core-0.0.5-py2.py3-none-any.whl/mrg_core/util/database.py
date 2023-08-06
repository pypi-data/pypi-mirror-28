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
""" High level database connection interface """

from __future__ import print_function

import logging
import datetime
from collections import OrderedDict

from future.utils import iteritems

try:
    import MySQLdb
    import MySQLdb.cursors as MySQLdb_cursors
except ImportError as imp_exc:
    try:
        import pymysql as MySQLdb
        import pymysql.cursors as MySQLdb_cursors
    except ImportError as imp_exc:
        print('WARNING: pip install MySQL-python')
        print('or')
        print('WARNING: pip install PyMySQL')


class SQLException(Exception):
    """ SQL error generated after an SQL bad statement is executed. """


class DatabaseConnectionException(Exception):
    """ The base exception class for the DatabaseConnection class. """


def extract_from_url(url):
    """ Extracts information from a URL  and fills the passed kwargs dict
    with the key values extracted.

    Reference: http://docs.sqlalchemy.org/en/latest/core/engines.html

    :param str url:
    :return: key/value pairs for:
        'db_engine', 'db_host', 'db_port', 'db_usr', 'db_pwd'
    :rtype: dict
    """
    kwargs = {}
    protocol, rest = url.split('://', 1)
    kwargs['db_engine'] = protocol
    if '/' in rest:
        rest, kwargs['db_name'] = rest.split('/', 1)

    if '@' in rest:
        uid_pwd, host = rest.split('@')
        kwargs['db_usr'], kwargs['db_pwd'] = uid_pwd.split(':')
    else:
        host = rest

    if ':' in host:
        kwargs['db_host'], kwargs['db_port'] = host.split(':', 1)
    elif host:
        kwargs['db_host'], kwargs['db_port'] = host, '0'

    return kwargs


class DatabaseConnection(object):
    """ This class manages as database connection and ensures that
    the connection remains valid even after a connection timeout.

    """
    def __init__(self, vault, **kwargs):
        # reference:
        # http://docs.sqlalchemy.org/en/latest/core/engines.html

        # 'sqlite:////absolute/path/to/foo.db'
        # r'sqlite:///C:\path\to\foo.db'
        #
        # mysql://{user}:{passwd}@{host}:{port}/{db}
        #
        if 'db_url' in kwargs:
            kwargs.update(extract_from_url(kwargs['db_url']))
            if 'db_usr' not in kwargs and 'db_pwd' not in kwargs:
                kwargs['db_pwd'] = kwargs['db_name']
                kwargs['db_usr'] = kwargs['db_name']

        elif 'url' in kwargs:
            kwargs.update(extract_from_url(kwargs['url']))

        if vault is not None:
            kwargs['db_usr'] = vault.evaluate_key(kwargs, 'db_usr')
            kwargs['db_pwd'] = vault.evaluate_key(kwargs, 'db_pwd')

        self.callback = lambda: None
        self._con = None
        self._cursor = None
        self._reuse_cursor = True
        self._engine = kwargs.get('db_engine', '')

        if 'mysql' in self._engine:
            self._module = MySQLdb
            self._sql_version = 'SELECT VERSION()'
            self._con_kwargs = {
                'host': kwargs.get('db_host', None),
                'port': int(kwargs.get('db_port', '0')),
                'db': kwargs.get('db_name', None),
                'user': kwargs.get('db_usr', None),
                'passwd': kwargs.get('db_pwd', None),
                'cursorclass': MySQLdb_cursors.DictCursor,
            }
            self._db_name = kwargs.get('db_name', None)
        #
        # elif self._engine == 'sqlite':
        #     class DictConnection(sqlite.Connection):
        #         """ Create a connection which returns it's records as dictionaries """
        #         def __init__(self, *args, **con_kwargs):
        #             super(DictConnection, self).__init__(*args, **con_kwargs)
        #             self.row_factory = sqlite.Row
        #
        #     self._module = sqlite
        #     self._sql_version = 'SELECT SQLITE_VERSION()'
        #     self._con_kwargs = {
        #         'database': kwargs.get('database', None),
        #         'factory': DictConnection,
        #     }
        else:
            raise DatabaseConnectionException('Unsupported database engine')

    @property
    def database(self):
        """ Retrieve the database name.

        :return: the database name
        :rtype: str
        """
        return self._db_name

    @property
    def conn(self):
        """ Retrieve the SQL client connection.

        :return: the underlying SQL database client connection.
        :rtype: Connection
        """
        return self._con

    def close(self):
        """ Close the database to any further communication. """
        if self._cursor:
            self._cursor.close()

        if self._con:
            self._con.close()
            self._con = None

    def commit(self):
        """ Flush any modifications made to the database to make them persistent.
        """
        if self._con:
            self._con.commit()

    def rollback(self):
        """ Do not flush or commit changes. Revert the database to the BEGIN
        of transaction point.
        """
        if self._con:
            self._con.rollback()

    def init_db_connection(self):
        """ Initialize and open the database to communication. If the database
        is already open, a quick test is done on it to ensure that the
        connection has not gone stale. If this is the case, the connection
        will be re-established. """

        def new_connection():
            """ Create new database connection. """
            try:
                copy_kwargs = dict(self._con_kwargs)
                copy_kwargs['passwd'] = '*********'
                copy_kwargs['user'] = '********'
                logging.debug('opening database connection: %s', repr(copy_kwargs))
                self._con = self._module.connect(**self._con_kwargs)
            except self._module.Error as ex2:
                raise DatabaseConnectionException(str(ex2))

        def test_connection():
            """ Test the new / existing database connection. """
            result = False
            if self._cursor is not None:
                return True
            try:
                cursor = self._con.cursor()
                cursor.execute(self._sql_version)
                results = cursor.fetchone()
                if results:
                    result = True
                cursor.close()
            except self._module.Error as ex3:
                raise DatabaseConnectionException(str(ex3))
            return result

        if self._con is None:
            new_connection()

        if not test_connection():
            new_connection()

    def get_column_names(self, table_name):
        """ Convenience routines to retrieve the table column names and attributes.

        :param str table_name: the database table name.
        :return: list of table column fields
        :rtype: list
        """
        if '.' in table_name:
            schema_name, table_name = table_name.split('.', 1)
            sql_select = "SELECT column_name from INFORMATION_SCHEMA.COLUMNS " \
                         "WHERE table_schema='%s' and table_name='%s';" % (schema_name, table_name)
        else:
            sql_select = "SELECT column_name from INFORMATION_SCHEMA.COLUMNS " \
                         "WHERE table_name='%s';" % table_name

        rows = self.execute(sql_select)
        fields = []
        for row in rows:
            fields.append(row['column_name'])

        return fields

    @staticmethod
    def log_record(row, max_length=16):
        """ Make a copy of the row, but crop out long texts.

        :param dict row: the row to normalize for logging (print)
        :param int max_length: only log the first N characters of the column value.
        :return: dict, a copy of the row but sanitized for logging.
        :rtype: dict
        """
        result = {}
        for column in row:
            value = row[column]
            if isinstance(value, datetime.date):
                value = value.strftime('%Y-%m-%d')
            elif isinstance(value, datetime.datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, str):
                if '\n' in value:
                    value = value.split('\n')[0]
                if len(value) > 16:
                    value = value[0:max_length] + '...'
            result[column] = value
        return result

    def execute_insert(self, table, row):
        """ Convenience routine to generate a SQL INSERT statement
        based on dictionary key/value pairs.

        :param str table: the database table name.
        :param dict row: the record.
        """
        cols = []
        vals = []
        for key, val in iteritems(row):
            if val is None:
                continue

            if val == 'NOW()' or val == 'NULL':
                frmt = "%s"
            elif val == 'true':
                val = '1'
                frmt = "%s"
            elif val == 'false':
                val = '0'
                frmt = "%s"
            else:
                frmt = "'%s'"

            cols.append(key)
            vals.append(frmt % val)

        sql = "INSERT INTO %s (%s) VALUES (%s);" % (table, ','.join(cols), ','.join(vals))
        self.execute(sql)

    def execute_delete(self, sql_delete):
        """ Execute a DELETE sql statement and return the number of
        records effected.

        :param str sql_delete: the DELETE SQL statement.
        :return: the number of records deleted.
        :rtype: int
        """
        records = self.execute(sql_delete)
        if len(records):
            return records[0]
        else:
            return 0

    def get_table_counts(self, db_name):
        """ Retrieve the number of records for every table in the
        specified database.

        NOTE: this is MySQL specific.

        :param str db_name: the database name.
        :return: an order dictionary of table/count pairs.
        :rtype: OrderedDict
        """
        # reference:
        # http://stackoverflow.com/questions/286039/get-record-counts-for-all-tables-in-mysql-database
        sql = "SELECT "
        sql += "CONCAT("
        sql += "'SELECT \"',"
        sql += "table_name,"
        sql += "'\" AS table_name, COUNT(*) AS exact_row_count FROM `',"
        sql += "table_schema,"
        sql += "'`.`',"
        sql += "table_name,"
        sql += "'` UNION '"
        sql += ")"
        sql += "FROM "
        sql += "INFORMATION_SCHEMA.TABLES "
        sql += "WHERE "
        sql += "table_schema = '%s';" % db_name
        result = self.execute(sql)
        line = ''
        for entry in result:
            line += entry[list(entry.keys())[0]] + '\n'
        line = line.strip()
        line = line.strip('UNION')
        line += '\n'
        rows = self.execute(line)

        count = OrderedDict()
        # {u'exact_row_count': 0, u'table_name': 'camera_cam_camera'}
        for entry in rows:
            count[entry['table_name']] = entry['exact_row_count']
        return count

    def execute_get_count(self, sql_select):
        """ Execute a SELECT COUNT SQL statement and return the
        number of records counted.

        :param str sql_select: the SELECT COUNT(*) SQL statement.
        :return: the number of records counted.
        :rtype: int
        """
        row = self.execute_get_row(sql_select)
        return row[list(row.keys())[0]]

    def execute_get_row(self, sql_select):
        """ Retrieve first record.

        :param str sql_select: the SELECT SQL statement.
        :return: a dictionary if the record was found, else None
        :rtype: dict
        """
        rows = self.execute(sql_select, limit=1)
        if len(rows):
            return rows[0]
        return None

    def execute_file(self, sql_file):
        """ Execute a series of SQL statements stored in a file such as a
        is produced by a mysqldump command.

        :param str sql_file: the file to load.
        """
        with open(sql_file) as file_obj:
            sql = file_obj.read()
            self.execute(sql)

    def _acquire_cursor(self):
        """ Create or retrieve a database cursor to execute an
        SQL statement with.

        :return: the database cursor.
        :rtype: Cursor
        """
        if self._reuse_cursor:
            if self._cursor is None:
                self._cursor = self._con.cursor()
            cur = self._cursor
        else:
            cur = self._con.cursor()
        return cur

    def _release_cursor(self, cur):
        """ Release the resources used by the cursor retrieved
        with :func:`_acquire_cursor`.

        :param Cursor cur: the cursor to close.
        """
        if cur and not self._reuse_cursor:
            cur.close()

    @staticmethod
    def _collect_records(stmt, cur, single, records):
        """ Collect the records to return in the :func:`execute` method.

        :param str stmt: the SQL statement executed in the cursor object.
        :param Cursor cur: the database connection cursor object.
        :param bool single: True if the first record is to be returned,
            otherwise all records will be retrieved from the cursor.
        :param list records: the bucket list to fill. This is the
            output object.
        """
        if stmt.upper().startswith('DELETE'):
            records.append(cur.rowcount)

        if stmt.upper().startswith('SELECT') \
                or stmt.upper().startswith('SHOW'):
            rows = []
            if single:
                row = cur.fetchone()
                if row:
                    rows.append(row)
            else:
                rows = cur.fetchall()
            # log.debug('Returned: %d rows', len(rows))
            for row in rows:
                records.append(dict(row))
                # log.debug('Row: %s', repr(self.log_record(records[-1])))

    def execute(self, sql_stmt, limit=-1):
        """ Execute an SQL SELECT statement(s), and return the records as
        a list of dict.

        :param str sql_stmt: the semi-colon delimited SQL statement(s).
        :param int limit: the number of rows to return. -1 is all records.
        :return: a list of dictionaries
        :rtype: list
        :raises DatabaseConnectionException: if there are database
            connectivity errors.
        :raises SQLException: if the the SQL executed has errors.
        """
        self.init_db_connection()
        records = []
        try:
            cur = self._acquire_cursor()
            sql_statements = sql_stmt.split(';')
            for stmt in sql_statements:
                stmt = stmt.strip()
                if stmt:
                    try:
                        cur.execute(stmt)
                    except MySQLdb.Error as exc:
                        logging.debug('SQL: %s', stmt)
                        raise SQLException(str(exc))
                    single = limit == 1
                    self._collect_records(stmt, cur, single, records)
                    logging.debug('Rows: %3d, SQL: %s', len(records), stmt)

        except self._module.Error as ex:
            raise DatabaseConnectionException(str(ex))
        finally:
            self._release_cursor(cur)

        self.callback()

        return records
