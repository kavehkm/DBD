# internal
import pandas
from src import mem
from src import console
from src import settings
from src.snap import Snap
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
    def parent(self, w):
        self._parent = w

    @property
    def childs(self):
        return self._childs

    def add_child(self, w):
        self._childs.append(w)

    def remove_child(self, w):
        self._childs.remove(w)

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
        console.render_databases(self.databases)


class Snaps(BaseWidget):
    """Snaps Widget"""
    CODE = 3
    NAME = 'Snaps'
    PARENT = Entry.CODE

    def do(self):
        snaps = mem.get('snaps')
        if snaps is None:
            snaps = fn.load_snaps()
            mem.set('snaps', snaps)
        console.render_snaps(snaps)


class Tables(BaseWidget):
    """Database Tables Widget"""
    CODE = 4
    NAME = 'Tables'
    PARENT = Databases.CODE

    def __init__(self):
        super().__init__()
        self.current_database = None

    def do(self):
        database = self.parent.databases[int(input('Database: '))]
        self.current_database = database
        console.render_tables(database.tables())


class CreateSnap(BaseWidget):
    """Create Snap Widget"""
    CODE = 5
    NAME = 'CreateSnap'
    PARENT = Databases.CODE

    def do(self):
        # find database
        database = self.parent.databases[int(input('Database: '))]
        # create snap
        snap = Snap.from_database(database)
        console.success('Snap created successfully')
        # save created snap into snaps directory as pickle
        snap.to_pickle(settings.SNAP_DIR)
        console.success('Snap saved successfully')
        # clear cached snaps
        mem.delete('snaps')


class Compare(BaseWidget):
    """Database Compare Widget"""
    CODE = 6
    NAME = 'Compare'
    PARENT = Snaps.CODE

    def do(self):
        # get snaps
        snaps = mem.get('snaps', [])
        snap1 = snaps[int(input('Snap1: '))]
        snap2 = snaps[int(input('Snap2: '))]
        # compare

        deleted = snap1.difference(snap2)
        new = snap1.r_difference(snap2)
        changed = snap1.changed(snap2)

        mem.set("columnChanged", changed[0])
        mem.set("rowChanged", changed[1])

        # generate report
        if not any([deleted, new, changed[0]]):
            console.print('No changes detected')
        else:
            console.render_compare(new, deleted, changed[0])


class Columns(BaseWidget):
    """Table Columns Widget"""
    CODE = 7
    NAME = 'Columns'
    PARENT = Tables.CODE

    def do(self):
        table = self.parent.current_database.tables()[int(input('Table: '))]
        columns = self.parent.current_database.columns(table)
        console.render_columns(columns)


class Records(BaseWidget):
    """Table Records Widget"""
    CODE = 8
    NAME = 'Records'
    PARENT = Tables.CODE

    def do(self):
        table = self.parent.current_database.tables()[int(input('Table: '))]
        columns = self.parent.current_database.columns(table)
        records = self.parent.current_database.records(table)
        console.render_records(columns, records)

class ChangedColumns(BaseWidget):
    """Changed Columns in a Table"""
    CODE = 9
    NAME = 'View Changed Columns'
    PARENT = Compare.CODE

    def do(self):
        
        changed_columns = mem.get('columnChanged',[])
        selected_tbl = list(changed_columns.keys())[int(input('Table: '))]
        a = console.render_changedColumns(changed_columns,selected_tbl)

        mem.set('selected_tbl', selected_tbl)
        mem.set('selected_clmn', a)
        
        

class ChangedFields(BaseWidget):
    """Detailed changes in Columns"""
    CODE = 10
    NAME = "View Change in a Column"
    PARENT = ChangedColumns.CODE

    def do (self):
        df = pandas.DataFrame()
        changed_columns = mem.get('rowChanged')
        selected_column = mem.get('selected_tbl')
        selected_detail = mem.get('selected_clmn')
        for i in changed_columns:
            if(selected_column in list(i.keys())):
                df = i.get(selected_column)
        selection = int(input('Column: '))
        for i in selected_detail:
            if selection in i.keys():
                value = i.get(selection)
        user_selection = df.loc[:,value ].fillna(-1)
        
        for index, row in user_selection.iterrows():
            if not(row.get('self') == -1 and row.get('other') == -1):
                console.print(f"Change in line {index} from {row.get('self')} to {row.get('other')}")
        df.iloc[0:0]

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
