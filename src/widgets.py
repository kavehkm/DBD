# internal
from src import console
from src import functions as fn


class BaseWidget(object):
    """BaseWidgets"""
    CODE = 0
    NAME = 'Base'
    PARENT = 0

    def __init__(self):
        self._parent = None
        self._childs = list()

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, widget):
        self._parent = widget

    @property
    def childs(self):
        return self._childs

    def add_child(self, widget):
        self._childs.append(widget)

    def remove_child(self, widget):
        self._childs.remove(widget)

    def do(self):
        pass


class Entry(BaseWidget):
    """Entry Widget"""
    CODE = 1
    NAME = 'Entry'
    PARENT = 0


class Databases(BaseWidget):
    """Databases Widget"""
    CODE = 2
    NAME = 'Databases'
    PARENT = Entry.CODE

    def __init__(self):
        super().__init__()
        self._databases = None

    @property
    def databases(self):
        if self._databases is None:
            self._databases = fn.load_databases()
        return self._databases

    def do(self):
        console.databases(self.databases)


class Snaps(BaseWidget):
    """Snaps Widget"""
    CODE = 3
    NAME = 'Snaps'
    PARENT = Entry.CODE


class Tables(BaseWidget):
    """Database Tables Widget"""
    CODE = 4
    NAME = 'Tables'
    PARENT = Databases.CODE

    def do(self):
        database = self.parent.databases[int(input('Database: '))]
        console.tables(database.tables())


class CreateSnap(BaseWidget):
    """Create Snap Widget"""
    CODE = 5
    NAME = 'CreateSnap'
    PARENT = Databases.CODE

    def do(self):
        database = self.parent.databases[int(input('Database: '))]
        fn.create_snap(database)
        console.success('Snap created successfully')


class Compare(BaseWidget):
    """Database Compare Widget"""
    CODE = 6
    NAME = 'Compare'
    PARENT = Databases.CODE


# initialize widgets and set relations
WIDGETS = {
    cls.CODE: cls()
    for cls in BaseWidget.__subclasses__()
}

for widget in WIDGETS.values():
    parent = WIDGETS.get(widget.PARENT)
    if parent:
        widget.parent = parent
        parent.add_child(widget)


# set root
ROOT = WIDGETS.get(1)
