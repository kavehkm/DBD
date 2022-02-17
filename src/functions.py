# internal
from . import settings
from . import db_backends


def load_databases():
    databases = list()
    for db in settings.DATABASES:
        backend = None
        dbms = db['dbms']
        if dbms == 'mssql':
            backend = db_backends.MSSQL
        elif dbms == 'mysql':
            pass
        elif dbms == 'sqlite':
            pass
        if backend and backend.check_conf(**db):
            databases.append(backend(**db))
    return databases
