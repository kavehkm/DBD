# rich
from rich.tree import Tree
from rich.panel import Panel
from rich.columns import Columns
from rich.console import Console


console = Console()


print = console.print


def error(text):
    print('[red bold]{}'.format(text))


def menu(items):
    tree = Tree('')
    for item in items:
        tree.add(item)
    print(tree)


def widget_title(widget):
    console.rule('[bold red]{}'.format(widget.NAME), style='[white]')


def databases(databases):
    columns = Columns()
    for i, db in enumerate(databases):
        panel = Panel(
            title=str(i),
            renderable='[bold red]{}[/bold red]\n[yellow]{}'.format(db.DBMS, db.name)
        )
        columns.add_renderable(panel)
    print(columns)


def tables(tables):
    columns = Columns()
    for i, table in enumerate(tables):
        panel = Panel(
            title=str(i),
            renderable='[yellow]{}'.format(table)
        )
        columns.add_renderable(panel)
    print(columns)
