# standard
import sys
from collections import OrderedDict
# internal
from src import widgets
from src import console


class Runner(object):
    """Runner"""
    def __init__(self):
        self._current_widget = widgets.ROOT
        self._menu = OrderedDict()

    def do(self):
        console.widget_title(self._current_widget)
        try:
            self._current_widget.do()
        except Exception as e:
            console.error(str(e))

    def print_menu(self):
        # clear menu
        self._menu.clear()
        # add current widget childs as menu items
        for i, widget in enumerate(self._current_widget.childs):
            self._menu[str(i)] = widget.NAME
        # if current widget has parent add back option
        if self._current_widget.parent:
            self._menu['b'] = 'Back'
        # finally add exit into menu
        self._menu['x'] = 'Exit'
        items = ['({}) {}'.format(key, value) for key, value in self._menu.items()]
        console.menu(items)

    def dispatch(self):
        # get answer
        while True:
            answer = input(': ')
            if answer in self._menu:
                break
            console.error('EEK')
        # dispatch
        if answer == 'x':
            console.print('Goodbye')
            sys.exit(0)
        elif answer == 'b':
            self._current_widget = self._current_widget.parent
        else:
            self._current_widget = self._current_widget.childs[int(answer)]

    def run(self):
        while True:
            self.do()
            self.print_menu()
            self.dispatch()


def main():
    runner = Runner()
    runner.run()


if __name__ == '__main__':
    main()
