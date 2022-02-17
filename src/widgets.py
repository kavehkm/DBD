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
        print(self.NAME, 'do something...')


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


class Snaps(BaseWidget):
    """Snaps Widget"""
    CODE = 3
    NAME = 'Snaps'
    PARENT = Entry.CODE


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
