# standard
import os
# pyodbc: mssql connector
import pyodbc
# sqlite3: sqlite connector
import sqlite3


class BaseBackend(object):
    """Base Backend"""
    ENGINE = 'Base'

    @property
    def name(self):
        return

    @classmethod
    def check_conf(cls, **kwargs):
        pass

    @staticmethod
    def execute(conn, sql, *params, method='fetchall'):
        cursor = conn.cursor()
        cursor.execute(sql, params)
        result = None
        if method == 'fetchval':
            result = cursor.fetchval()
        elif method == 'fetchone':
            result = cursor.fetchone()
        elif method == 'fetchall':
            result = cursor.fetchall()
        # close cursor
        cursor.close()
        return result

    def tables(self):
        pass

    def columns(self, table):
        pass

    def records(self, table):
        pass


class MSSQL(BaseBackend):
    """Microsoft SQL Server"""
    ENGINE = 'MSSQL'

    def __init__(self, **kwargs):
        self.server = kwargs.get('server')
        self.database = kwargs.get('database')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.conn = self.connection(self.server, self.database, self.username, self.password)

    @property
    def name(self):
        return '{}@{}'.format(self.database, self.server)

    @staticmethod
    def connection(server, database, username, password):
        driver = [d for d in pyodbc.drivers() if d.find('SQL') != -1][0]
        dsn = 'driver={};server={};database={};uid={};pwd={}'
        dsn = dsn.format(driver, server, database, username, password)
        return pyodbc.connect(dsn)

    @classmethod
    def check_conf(cls, **kwargs):
        server = kwargs.get('server')
        database = kwargs.get('database')
        username = kwargs.get('username')
        password = kwargs.get('password')
        if not all([server, database, username, password]):
            return False
        try:
            conn = cls.connection(server, database, username, password)
            cls.execute(conn, 'SELECT @@VERSION')
        except Exception:
            return False
        else:
            return True

    def tables(self):
        sql = f"""
            SELECT TABLE_NAME
            FROM {self.database}.INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE'
        """
        return [table[0] for table in self.execute(self.conn, sql)]

    def columns(self, table):
        sql = f"""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{table}'
        """
        columns = [column[0] for column in self.execute(self.conn, sql)]
        return columns

    def records(self, table):
        sql = "SELECT * FROM {}".format(table)
        return self.execute(self.conn, sql)


class SQLite(BaseBackend):
    """SQLite"""
    ENGINE = 'SQLite'

    def __init__(self, **kwargs):
        self.path = kwargs.get('path')
        self.conn = self.connection(self.path)

    @property
    def name(self):
        return self.path

    @staticmethod
    def connection(path):
        return sqlite3.connect(path)

    @classmethod
    def check_conf(cls, **kwargs):
        path = kwargs.get('path')
        if not path or not os.path.exists(path):
            return False
        return True

    def tables(self):
        sql = """
            SELECT name
            FROM sqlite_master
            WHERE type='table';
        """
        return [table[0] for table in self.execute(self.conn, sql)]

    def columns(self, table):
        sql = "SELECT * FROM {}".format(table)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        cursor.close()
        return columns

    def records(self, table):
        sql = "SELECT * FROM {}".format(table)
        return self.execute(self.conn, sql)
