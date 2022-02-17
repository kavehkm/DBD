class BaseWidget(object):
    """BaseWidgets"""
    CODE = 0
    NAME = 'Base'
    PARENT = None

    def __init__(self):
        self._parent = None
        self._childs = list()

    def parent(self):
        return self._parent
    
    def set_parent(self, widget):
        pass

    def childs(self):
        return self._childs

    def add_child(self, widget):
        pass

    def remove_child(self, widget):
        pass

    def do(self):
        print('base widget do something')
