# -*- coding: utf-8 -*-
import re

import pandas as pd
from dateutil import parser
from pandas import DataFrame

from sqlwriter.exceptions import SQLWriterException
from sqlwriter.utils.utils import chunks
from sqlwriter.utils.log.logging_mixin import LoggingMixin
from unidecode import unidecode


class SQLDataFrame(DataFrame):
    def __init__(self, *args, **kwargs):
        DataFrame.__init__(self, *args, **kwargs)

    def to_sql(self, conn, database, tablename, write_limit=200, truncate=False):
        writer = SQLWriter(conn, database, tablename, self.columns, write_limit, truncate)
        writer.write(self.values)
        writer.close()


class SQLWriter(LoggingMixin):
    '''Object that allows for the ease of writing data to SQL database

    Parameters
    ----------
    server : string
        Microsoft SQL Server configured in config.yaml
    database : string
        Target database on server
    table_name : string
        Target table in database
    cols : array-like
        Data columns to write to, should be contained in columns of target
        table. Length must match data row length.
    write_limit : int, default 200
        Determined by net_buffer_length and average row length.
        Not sure what this is in microsoft
    truncate : Boolean, default False
        Truncate the table before writing data
    logger : Python logging object, default None
        output information from mysql writer
    progress : boolean, default False
        optional argument for progress bar while writing to table
    '''

    def __init__(self, conn, database, table_name, cols,  write_limit=200, truncate=False):
        self.conn = conn
        self.curs = self.conn.cursor()
        self.flavor = re.findall(r"<type '(\w+)", str(self.conn.__class__))[0]
        self.database = database
        self.table_name = table_name
        self.db_table = self._get_db_table()
        self.cols = cols
        self.write_limit = write_limit
        self.truncate = truncate

        self.description = self._get_description()
        self.insert_part = 'INSERT INTO {} ('.format(self.db_table) + ','.join(cols) + ') VALUES '
        self.fields = self._make_fields()

    def _get_db_table(self):
        return '.'.join([self.database, self.table_name])

    def _get_description(self):
        """
        Selects 1 record from selected database table, and takes description
        from cursor object

        Returns
        -------
        desc : list
            list of tuples that describe each selected column
        """
        sql = {
            'pymssql': 'select top 1 %s from %s',
            'psycopg2': 'select %s from %s limit 1',
            'mysql': 'select %s from %s limit 1',
            'oracle': 'select %s from %s limit 1',
        }
        self.curs.execute(sql[self.flavor] % (','.join(self.cols), self.db_table))
        desc = self.curs.description
        diff_cols = set([x.lower() for x in self.cols]).symmetric_difference(set([x[0].lower() for x in desc]))
        if len(diff_cols) > 0:
            raise SQLWriterException('Columns supplied does not match table')  # TODO: add offending columns, table name, and possible options (fuzzy matching?)
            # BUG: wont work, will error at line 91
        return desc

    def _make_fields_pymssql(self):
        import pymssql
        string, datetime, date, numeric, other = [], [], [], [], []
        for i in range(len(self.description)):
            test = self.description[i][1]
            if test == pymssql.STRING.value:
                string.append(i)
            elif test == pymssql.DATETIME.value:
                datetime.append(i)
            elif test == pymssql.DECIMAL.value or test == pymssql.NUMBER.value:
                numeric.append(i)
            else:
                other.append(i)
        return string, datetime, date, numeric, other

    def _make_fields_psycopg2(self):
        import psycopg2
        string, datetime, date, numeric, other = [], [], [], [], []
        for i in range(len(self.description)):
            test = self.description[i][1]
            if test in psycopg2.STRING.values:
                string.append(i)
            elif test in psycopg2.DATETIME.values:
                datetime.append(i)
            elif test in psycopg2.NUMBER.values:
                numeric.append(i)
            elif test in (1082,):
                date.append(i)
            else:
                other.append(i)
        return string, datetime, date, numeric, other

    def _make_fields(self):
        """
        Iterates through description and determines each fields data types
        so they can be properly formatted during writing

        Returns
        -------
        fields: dictionary of lists
            field types and corresponding indexes
        """
        keys = ('string', 'datetime', 'date', 'numeric', 'other')
        if self.flavor == 'pymssql':
            values = self._make_fields_pymssql()
        elif self.flavor == 'psycopg2':
            values = self._make_fields_psycopg2()
        return dict(zip(keys, values))

    def _mogrify(self, row):
        """String formats data based on fields to be able to multi-insert into
        MySQL

        Parameters
        ---------
        row : array-like
            An array of data to be written to the columns in the target table

        Returns
        -------
        string:
            row formatted as string tuple for easy mysql writing
        """
        if isinstance(row, tuple):
            row = list(row)  # needs to be mutable
        for idx in self.fields['string']:
            try:
                row[idx] = "'{}'".format(str(row[idx]).replace("'", "")) if row[idx] else 'NULL'
            except UnicodeEncodeError:
                row[idx] = "'{}'".format(unidecode(row[idx])) if row[idx] else 'NULL'
        for idx in self.fields['datetime']:
            try:
                row[idx] = row[idx].strftime("'%Y-%m-%d %H:%M:%S'") if row[idx] else 'NULL'
            except AttributeError:
                row[idx] = parser.parse(row[idx])
                row[idx] = row[idx].strftime("'%Y-%m-%d %H:%M:%S'")
            except:
                row[idx] = 'NULL'
        for idx in self.fields['date']:
            row[idx] = "'{}'".format(row[idx]) if row[idx] else 'NULL'
            # row[idx] = row[idx].strftime("'%Y-%m-%d'") if row[idx] else 'NULL'
        for idx in self.fields['numeric']:
            if row[idx] == '':
                row[idx] = 'NULL'
            else:
                row[idx] = str(row[idx])
        for idx in self.fields['other']:
            row[idx] = str(row[idx]) if row[idx] else 'NULL'
        return '(%s)' % ','.join(row)

    def _truncate(self):
        # NOTE: I'm pretty sure this syntax is universal
        if self.truncate:
            self.curs.execute('TRUNCATE TABLE {}'.format(self.db_table))
            self.conn.commit()

    def write(self, rows):
        """Truncates table, formats strings in data and multi-inserts into MySQL

        Parameters
        ----------
        rows: array-like
            An array of arrays of data to be written to the target table
        """
        if isinstance(rows, pd.DataFrame):
            rows = rows.values

        self._truncate()
        if len(rows) == 0:
            return
        queries = chunks(rows, self.write_limit)
        for query in queries:
            query = [self._mogrify(x) for x in query]

            self.curs.execute(self.insert_part + ','.join(query))
            self.conn.commit()


    def close(self):
        self.curs.close()
        self.conn.close()
