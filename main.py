from rich.console import Console, OverflowMethod
from rich.table import Table
import json
from rich import print
from typing import List
import os
import datetime



def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

users_file = "Account/account.json"


def save_users(users):
    with open(users_file, "w") as file:
        json.dump(users, file, indent=4)


def load_users():
    try:
        with open(users_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def is_valid_email(email):
    console = Console(width=50)
    while not email.endswith("@gmail.com"):
        print("[bold red]Invalid email format![/bold red]"
              "\n[cyan]Valid example: iust@gmail.com[/cyan]")

        input("Press Enter to continue...")
        clear_screen()
        console.print("  ┏┓•          ", justify='left', style="blink bold red")
        console.print("  ┗┓┓┏┓┏┓  ┓┏┏┓", justify='left', style="blink bold red")
        console.print("  ┗┛┗┗┫┛┗  ┗┻┣┛", justify='left', style="blink bold red")
        console.print("      ┛      ┛ ", justify='left', style="blink bold red")
        console.print("Enter your email address: ", justify='left', style="blink bold yellow")
        email = input()
    return email


def is_valid_password(email, username):
    console = Console(width=50)
    console.print("Enter your password: ", justify='left', style="blink bold blue")
    password = input()
    while not (any(char.isupper() for char in password) and any(char.islower() for char in password) \
               and any(char in "~@#$!%^&*?" for char in password) and any(char.isdigit() for char in password) \
               and len(password) == 8):
        print("[bold red]Invalid password! "
              "\nYour password must have 8 characters, "
              "\nat least one uppercase letter, "
              "\nat least one lowercase letter, "
              "\nat least one number, "
              "\nand at least one of the characters '~@#$!%^&*?'[/bold red]")

        print("[cyan]Valid example: Iust@ac1[/cyan]")
        input("Press Enter to continue...")
        clear_screen()
        console.print("  ┏┓•          ", justify='left', style="blink bold red")
        console.print("  ┗┓┓┏┓┏┓  ┓┏┏┓", justify='left', style="blink bold red")
        console.print("  ┗┛┗┗┫┛┗  ┗┻┣┛", justify='left', style="blink bold red")
        console.print("      ┛      ┛ ", justify='left', style="blink bold red")
        console.print("Enter your email address: ", justify='left', style="blink bold yellow")
        console.print(email, justify='right', style="blink bold cyan")
        console.print("Enter your username: ", justify='left', style="blink bold green")
        console.print(username, justify='right', style="blink bold cyan")
        console.print("Enter your password: ", justify='left', style="blink bold blue")

        password = input()

    return (password, email, username)


def print_account(email, username, password, console):
    overflow_methods: List[OverflowMethod] = ["Email"]
    for overflow in overflow_methods:
        console.rule(overflow)
        console.print(email, overflow=overflow, style="bold white")
        print("\n")

    overflow_methods_u: List_u[OverflowMethod] = ["Username"]
    for overflow_u in overflow_methods_u:
        console.rule(overflow_u)
        console.print(username, overflow=overflow_u, style="bold white")
        print("\n")

    overflow_methods_p: List_p[OverflowMethod] = ["Password"]
    for overflow_p in overflow_methods_p:
        console.rule(overflow_p)
        console.print(password, overflow=overflow_p, style="bold white")
        print("\n")


def create_account():
    console = Console(width=50)
    users = load_users()

    console.print("  ┏┓•          ", justify='left', style="blink bold red")
    console.print("  ┗┓┓┏┓┏┓  ┓┏┏┓", justify='left', style="blink bold red")
    console.print("  ┗┛┗┗┫┛┗  ┗┻┣┛", justify='left', style="blink bold red")
    console.print("      ┛      ┛ ", justify='left', style="blink bold red")
    console.print("Enter your email address: ", justify='left', style="blink bold yellow")
    email = is_valid_email(input())

    while any(user_data['email'] == email for user_data in users.values()):
        print("[bold red]Email already exists![/bold red]")
        input("Press Enter to continue...")
        clear_screen()
        console.print("  ┏┓•          ", justify='left', style="blink bold red")
        console.print("  ┗┓┓┏┓┏┓  ┓┏┏┓", justify='left', style="blink bold red")
        console.print("  ┗┛┗┗┫┛┗  ┗┻┣┛", justify='left', style="blink bold red")
        console.print("      ┛      ┛ ", justify='left', style="blink bold red")
        console.print("Enter your email address: ", justify='left', style="blink bold yellow")
        email = input()

    clear_screen()
    console.print("  ┏┓•          ", justify='left', style="blink bold red")
    console.print("  ┗┓┓┏┓┏┓  ┓┏┏┓", justify='left', style="blink bold red")
    console.print("  ┗┛┗┗┫┛┗  ┗┻┣┛", justify='left', style="blink bold red")
    console.print("      ┛      ┛ ", justify='left', style="blink bold red")
    console.print("Enter your email address: ", justify='left', style="blink bold yellow")
    console.print(email, justify='right', style="blink bold cyan")
    console.print("Enter your username: ", justify='left', style="blink bold green")
    username = input()

    while username in users:
        print("[bold red]Username already exists![/bold red]")
        input("Press Enter to continue...")
        clear_screen()
        console.print("  ┏┓•          ", justify='left', style="blink bold red")
        console.print("  ┗┓┓┏┓┏┓  ┓┏┏┓", justify='left', style="blink bold red")
        console.print("  ┗┛┗┗┫┛┗  ┗┻┣┛", justify='left', style="blink bold red")
        console.print("      ┛      ┛ ", justify='left', style="blink bold red")
        console.print("Enter your email address: ", justify='left', style="blink bold yellow")
        console.print(email, justify='right', style="blink bold cyan")
        console.print("Enter your username: ", justify='left', style="blink bold green")
        username = input()

    clear_screen()
    console.print("  ┏┓•          ", justify='left', style="blink bold red")
    console.print("  ┗┓┓┏┓┏┓  ┓┏┏┓", justify='left', style="blink bold red")
    console.print("  ┗┛┗┗┫┛┗  ┗┻┣┛", justify='left', style="blink bold red")
    console.print("      ┛      ┛ ", justify='left', style="blink bold red")
    console.print("Enter your email address: ", justify='left', style="blink bold yellow")
    console.print(email, justify='right', style="blink bold cyan")
    console.print("Enter your username: ", justify='left', style="blink bold green")
    console.print(username, justify='right', style="blink bold cyan")

    password, email, username = is_valid_password(email, username)
    clear_screen()
    print("injas")
    console.print("  ┏┓•          ", justify='left', style="blink bold red")
    console.print("  ┗┓┓┏┓┏┓  ┓┏┏┓", justify='left', style="blink bold red")
    console.print("  ┗┛┗┗┫┛┗  ┗┻┣┛", justify='left', style="blink bold red")
    console.print("      ┛      ┛ ", justify='left', style="blink bold red")
    console.print("Enter your email address: ", justify='left', style="blink bold yellow")
    console.print(email, justify='right', style="blink bold cyan")
    console.print("Enter your username: ", justify='left', style="blink bold green")
    console.print(username, justify='right', style="blink bold cyan")
    console.print("Enter your password: ", justify='left', style="blink bold blue")
    console.print(password, justify='right', style="blink bold cyan")
    console.print("Confirm your password: ", justify='left', style="blink bold magenta")
    confirm_password = input()

    while password != confirm_password:
        print("[bold red]Passwords do not match![/bold red]")
        input("Press Enter to continue...")
        clear_screen()
        console.print("  ┏┓•          ", justify='left', style="blink bold red")
        console.print("  ┗┓┓┏┓┏┓  ┓┏┏┓", justify='left', style="blink bold red")
        console.print("  ┗┛┗┗┫┛┗  ┗┻┣┛", justify='left', style="blink bold red")
        console.print("      ┛      ┛ ", justify='left', style="blink bold red")
        console.print("Enter your email address: ", justify='left', style="blink bold yellow")
        console.print(email, justify='right', style="blink bold cyan")
        console.print("Enter your username: ", justify='left', style="blink bold green")
        console.print(username, justify='right', style="blink bold cyan")
        console.print("Enter your password: ", justify='left', style="blink bold blue")
        password = input()
        clear_screen()
        console.print("  ┏┓•          ", justify='left', style="blink bold red")
        console.print("  ┗┓┓┏┓┏┓  ┓┏┏┓", justify='left', style="blink bold red")
        console.print("  ┗┛┗┗┫┛┗  ┗┻┣┛", justify='left', style="blink bold red")
        console.print("      ┛      ┛ ", justify='left', style="blink bold red")
        console.print("Enter your email address: ", justify='left', style="blink bold yellow")
        console.print(email, justify='right', style="blink bold cyan")
        console.print("Enter your username: ", justify='left', style="blink bold green")
        console.print(username, justify='right', style="blink bold cyan")
        console.print("Enter your password: ", justify='left', style="blink bold blue")
        console.print(password, justify='right', style="blink bold cyan")
        console.print("Confirm your password: ", justify='left', style="blink bold magenta")
        confirm_password = input()

    clear_screen()
    console.print("  ┏┓•          ", justify='left', style="blink bold red")
    console.print("  ┗┓┓┏┓┏┓  ┓┏┏┓", justify='left', style="blink bold red")
    console.print("  ┗┛┗┗┫┛┗  ┗┻┣┛", justify='left', style="blink bold red")
    console.print("      ┛      ┛ ", justify='left', style="blink bold red")
    console.print("Enter your email address: ", justify='left', style="blink bold yellow")
    console.print(email, justify='right', style="blink bold cyan")
    console.print("Enter your username: ", justify='left', style="blink bold green")
    console.print(username, justify='right', style="blink bold cyan")
    console.print("Enter your password: ", justify='left', style="blink bold blue")
    console.print(password, justify='right', style="blink bold cyan")
    console.print("Confirm your password: ", justify='left', style="blink bold magenta")
    console.print(confirm_password, justify='right', style="blink bold cyan")

    users[username] = {"email": email, "username": username, "password": password, "active": True}
    save_users(users)
    print("[bold green]Account created successfully![/bold green]")
    input("Press Enter to continue...")
    clear_screen()


def main():
    clear_screen()
    while True:
        table = Table( width=40, show_header=True, show_lines=True, style="bold magenta")

        table.add_column("Do you have an account?", justify="center", style="italic", no_wrap=True)
        table.add_row("1. sign up", style='bold red')
        table.add_row("2. login", style="bold green")
        table.add_row("3. exit", style='bold yellow')
        console = Console()
        console.print(table)
        choice = input("Choose an option: ")
        clear_screen()

        if choice == '1':
            create_account()


if __name__ == "__main__":
    main()