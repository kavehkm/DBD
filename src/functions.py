# internal
from src import console
from src import settings
from src import db_backends


def load_databases():
    databases = list()
    for db in settings.DATABASES:
        backend = None
        dbms = db['dbms']
        if dbms == 'mssql':
            backend = db_backends.MSSQL
        elif dbms == 'sqlite':
            backend = db_backends.SQLite
        elif dbms == 'mysql':
            pass
        if backend and backend.check_conf(**db):
            databases.append(backend(**db))
    return databases
