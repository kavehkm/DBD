# pyodbc: mssql connector
import pyodbc


class BaseBackend(object):
    """Base Backend"""
    def __init__(self, **kwargs):
        pass

    @property
    def name(self):
        return

    @classmethod
    def check_conf(cls, **kwargs):
        pass

    def tables(self):
        pass

    def columns(self, table):
        pass

    def records(self, table):
        pass


class MSSQL(BaseBackend):
    """Microsoft SQL Server"""
    def __init__(self, **kwargs):
            self.server = kwargs.get('server')
            self.database = kwargs.get('database')
            self.username = kwargs.get('username')
            self.password = kwargs.get('password')
            self.conn = self.connection(self.server, self.database, self.username, self.password)

    @property
    def name(self):
        return 'MSSQL->{}->{}'.format(self.server, self.database)

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
            cursor = conn.cursor()
            cursor.execute('SELECT @@VERSION')
            cursor.close()
            conn.close()
        except Exception:
            return False
        else:
            return True

    def _execute(self, sql, *params, method='fetchall'):
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        result = None
        if method == 'fetchval':
            result = cursor.fetchval()
        elif method == 'fetchone':
            record = cursor.fetchone()
            result = record[0] if record else None
        elif method == 'fetchall':
            result = [record for record in cursor.fetchall()]
        # close cursor
        cursor.close()
        return result

    def tables(self):
        sql = """
            SELECT TABLE_NAME
            FROM [?].INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE'
        """
        return self._execute(sql, self.database)
