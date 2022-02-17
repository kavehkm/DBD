# rich
from rich.tree import Tree
from rich.console import Console


console = Console()


def menu(items):
    tree = Tree('')
    for item in items:
        tree.add(item)
    console.print(tree)


def widget_title(widget):
    console.rule('[bold red]{}'.format(widget.NAME))
