# rich
from rich.tree import Tree
from rich.panel import Panel
from rich.table import Table
from rich.style import Style
from rich.columns import Columns
from rich.console import Console
from rich.progress import track


console = Console()


print = console.print


def error(text):
    print('[red bold]{}'.format(text))


def success(text):
    print('[green bold]{}'.format(text))


def render_menu(items):
    tree = Tree('')
    for item in items:
        tree.add(item)
    print(tree)


def widget_title(widget):
    console.rule('[bold red]{}'.format(widget.NAME), style='[white]')


def render_databases(databases):
    columns = Columns()
    for i, db in enumerate(databases):
        panel = Panel(
            title=str(i),
            renderable='[bold red]{}[/bold red]\n[yellow]{}'.format(db.ENGINE, db.name)
        )
        columns.add_renderable(panel)
    print(columns)


def render_snaps(snaps):
    columns = Columns()
    for i, snap in enumerate(snaps):
        panel = Panel(
            title=str(i),
            renderable='[bold red]{}[/bold red]\n[yellow]{}'.format(snap.database_name, snap.created_at)
        )
        columns.add_renderable(panel)
    print(columns)


def render_tables(tables):
    columns = Columns()
    for i, table in enumerate(tables):
        panel = Panel(
            title=str(i),
            renderable='[yellow]{}'.format(table)
        )
        columns.add_renderable(panel)
    print(columns)


def render_columns(columns):
    render_tables(columns)


def render_records(columns, records):
    table = Table()
    for column in columns:
        table.add_column(column)
    for record in records:
        table.add_row(*[str(i) for i in record])
    print(table)


def progress(seq, description):
    return track(seq, description)


def render_compare(new, deleted, changed):
    # new
    new_style = Style(color='green')
    new_columns = Columns(title='New')
    # deleted
    deleted_style = Style(color='red')
    deleted_columns = Columns(title='Deleted')
    # changed
    changed_style = Style(color='cyan')
    changed_columns = Columns(title='Changed Tables')

    for n in new:
        new_columns.add_renderable(Panel(n, style=new_style))
    for d in deleted:
        deleted_columns.add_renderable(Panel(d, style=deleted_style))
    for c, col in enumerate(changed):
        panel = Panel(
            title=str(c),
            renderable='[yellow]{}'.format(col)
        )
        changed_columns.add_renderable(panel)
        
    print(new_columns, deleted_columns, changed_columns, sep='\n\n')

def render_changedColumns(col,sel):
    changed_columns = Columns(title='Changed Columns')

    #to check numeric choices coresspondence with changed columns
    #in changedField section
    tlist = []
    for k,v in col.items():
        if (k == sel):
            for i, values in enumerate(v):
                panel = Panel(
                    title = str (i),
                    renderable = '[yellow]{}'.format(values)
                )
                changed_columns.add_renderable(panel)
                tlist.append({i:values})
    print(changed_columns)
    return tlist