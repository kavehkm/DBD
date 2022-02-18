# rich
from rich.tree import Tree
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.console import Console
from rich.progress import track


console = Console()


print = console.print


def error(text):
    print('[red bold]{}'.format(text))


def success(text):
    print('[green bold]{}'.format(text))


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
            renderable='[bold red]{}[/bold red]\n[yellow]{}'.format(db.ENGINE, db.name)
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


def columns(columns):
    tables(columns)


def records(columns, records):
    table = Table()
    for column in columns:
        table.add_column(column)
    for record in records:
        table.add_row(*[str(i) for i in record])
    print(table)


def progress(seq, description):
    return track(seq, description)
