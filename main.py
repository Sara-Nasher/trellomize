from rich.console import Console
from rich.table import Table

table = Table( width=40, show_header=True, show_lines=True, style="bold magenta", title_justify='center', caption_justify='center')

table.add_column("Do you have an account?", justify="center", style="italic", no_wrap=True)
table.add_row("1. sign up", style='bold red')
table.add_row("2. login", style="bold green")
table.add_row("3. exit", style='bold yellow')
console = Console()
console.print(table)
