from rich.console import Console, OverflowMethod
from rich.table import Table
import json
from rich import print
from typing import List
import os
from datetime import datetime, timedelta
import uuid
from enum import Enum


class User:
    def __init__(self, username):
        self.username = username

class Project:
    def __init__(self, project_id, title, owner):
        self.project_id = project_id
        self.title = title
        self.owner = owner
        self.members = []
        self.tasks = []

    def add_member(self, member):
        if member != self.owner and member not in self.members:
            self.members.append(member)


class ProjectManager:
    def __init__(self):
        self.projects = []

    def create_project(self, project_id, title, owner):
        for project in self.projects:
            if project.project_id == project_id:
                print("Error: Project ID already exists.")
                return
        new_project = Project(project_id, title, owner)
        new_project.add_member(owner)
        self.projects.append(new_project)
        self.save_projects()

    def delete_project(self, project_id, username):
        for project in self.projects:
            if project.project_id == project_id:
                if project.owner.username == username:
                    self.projects.remove(project)
                    self.save_projects()
                    print("Project deleted successfully.")
                    input("Press Enter to continue...")
                    clear_screen()
                    return
                else:
                    print("You are not the owner of this project. You cannot delete it.")
                    return
        print("Error: Project ID not found.")

    def add_member_to_project(self, project_id, member):
        for project in self.projects:
            if project.project_id == project_id:
                project.add_member(member)
                self.save_projects()
                return
        print("Error: Project ID not found.")

    def remove_member_from_project(self, project_id, member_to_remove, requesting_user):
        for project in self.projects:
            if project.project_id == project_id:
                if member_to_remove.username == project.owner.username:
                    print("Error: Owner cannot be removed from the project.")
                    return
                if requesting_user == project.owner.username:
                    if member_to_remove.username in [member.username for member in project.members]:
                        project.members = [member for member in project.members if
                        member.username != member_to_remove.username]
                        self.save_projects()
                        print(f"{member_to_remove.username} has been removed from the project.")
                        input("Press Enter to continue...")
                        clear_screen()
                        return
                    else:
                        print("Error: The specified user is not a member of this project.")
                        return
                else:
                    print("Error: Only project owner can remove members.")
                    return
        print("Error: Project ID not found.")

    def get_user_projects(self, username):
        user_projects = []
        for project in self.projects:
            if username == project.owner.username:
                user_projects.append((project.project_id, project.title, "Owner"))
            elif username in [member.username for member in project.members]:
                user_projects.append((project.project_id, project.title, "Member"))
        return user_projects

    def save_projects(self):
        projects_json = []
        for project in self.projects:
            project_json = {
                "project_id": project.project_id,
                "title": project.title,
                "owner": project.owner.username,
                "members": [member.username for member in project.members],
            }
            projects_json.append(project_json)
        with open(os.path.join("Account", "projects.json"), "w") as f: 
            json.dump(projects_json, f, default=str)

    def load_projects(self):
        if os.path.exists(os.path.join("Account", "projects.json")):
            with open(os.path.join("Account", "projects.json"), "r") as f:
                project_data = json.load(f)
                for data in project_data:
                    owner = User(data["owner"])
                    members = [User(member) for member in data["members"]]
                    project = Project(data["project_id"], data["title"], owner)
                    for member in members:
                        project.add_member(member)
                    self.projects.append(project)


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

def print_sign_up():
    console = Console(width=50)
    console.print("  ┏┓•          ", justify='left', style="blink bold red")
    console.print("  ┗┓┓┏┓┏┓  ┓┏┏┓", justify='left', style="blink bold red")
    console.print("  ┗┛┗┗┫┛┗  ┗┻┣┛", justify='left', style="blink bold red")
    console.print("      ┛      ┛ ", justify='left', style="blink bold red")

def print_your_account():
    console = Console(width=50)
    console.print("  ┬ ┬┌─┐┬ ┬┬─┐  ┌─┐┌─┐┌─┐┌─┐┬ ┬┌┐┌┌┬┐", justify='center', style="blink bold white")
    console.print("  └┬┘│ ││ │├┬┘  ├─┤│  │  │ ││ ││││ │ ", justify='center', style="blink bold white")
    console.print("   ┴ └─┘└─┘┴└─  ┴ ┴└─┘└─┘└─┘└─┘┘└┘ ┴ \n", justify='center', style="blink bold white")


def print_login():
    console = Console(width=50)
    console.print("  ┓     •  ", justify='left', style="blink bold green")
    console.print("  ┃ ┏┓┏┓┓┏┓", justify='left', style="blink bold green")
    console.print("  ┗┛┗┛┗┫┗┛┗", justify='left', style="blink bold green")
    console.print("       ┛   ", justify='left', style="blink bold green")


def is_valid_email(email):
    console = Console(width=50)
    while not email.endswith("@gmail.com"):
        print("[bold red]Invalid email format![/bold red]"
              "\n[cyan]Valid example: iust@gmail.com[/cyan]")

        input("Press Enter to continue...")
        clear_screen()
        print_sign_up()
        console.print("\nEnter your email address: ", justify='left', style="blink bold yellow")
        email = input()
    return email


def is_valid_password(email, username):
    console = Console(width=50)
    console.print("\nEnter your password: ", justify='left', style="blink bold blue")
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
        print_sign_up()
        console.print("\nEnter your email address: ", justify='left', style="blink bold yellow")
        console.print(email, justify='left', style="blink bold cyan")
        console.print("\nEnter your username: ", justify='left', style="blink bold green")
        console.print(username, justify='left', style="blink bold cyan")
        console.print("\nEnter your password: ", justify='left', style="blink bold blue")

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

    print_sign_up()
    console.print("\nEnter your email address: ", justify='left', style="blink bold yellow")
    email = is_valid_email(input())

    while any(user_data['email'] == email for user_data in users.values()):
        print("[bold red]Email already exists![/bold red]")
        input("Press Enter to continue...")
        clear_screen()
        print_sign_up()
        console.print("\nEnter your email address: ", justify='left', style="blink bold yellow")
        email = input()

    clear_screen()
    print_sign_up()
    console.print("\nEnter your email address: ", justify='left', style="blink bold yellow")
    console.print(email, justify='left', style="blink bold cyan")
    console.print("\nEnter your username: ", justify='left', style="blink bold green")
    username = input()

    while username in users:
        print("[bold red]Username already exists![/bold red]")
        input("Press Enter to continue...")
        clear_screen()
        print_sign_up()
        console.print("\nEnter your email address: ", justify='left', style="blink bold yellow")
        console.print(email, justify='left', style="blink bold cyan")
        console.print("\nEnter your username: ", justify='left', style="blink bold green")
        username = input()

    clear_screen()
    print_sign_up()
    console.print("\nEnter your email address: ", justify='left', style="blink bold yellow")
    console.print(email, justify='left', style="blink bold cyan")
    console.print("\nEnter your username: ", justify='left', style="blink bold green")
    console.print(username, justify='left', style="blink bold cyan")

    password, email, username = is_valid_password(email, username)
    clear_screen()
    print_sign_up()
    console.print("\nEnter your email address: ", justify='left', style="blink bold yellow")
    console.print(email, justify='left', style="blink bold cyan")
    console.print("\nEnter your username: ", justify='left', style="blink bold green")
    console.print(username, justify='left', style="blink bold cyan")
    console.print("\nEnter your password: ", justify='left', style="blink bold blue")
    console.print(password, justify='left', style="blink bold cyan")
    console.print("\nConfirm your password: ", justify='left', style="blink bold magenta")
    confirm_password = input()

    while password != confirm_password:
        print("[bold red]Passwords do not match![/bold red]")
        input("Press Enter to continue...")
        clear_screen()
        print_sign_up()
        console.print("\nEnter your email address: ", justify='left', style="blink bold yellow")
        console.print(email, justify='left', style="blink bold cyan")
        console.print("\nEnter your username: ", justify='left', style="blink bold green")
        console.print(username, justify='left', style="blink bold cyan")
        console.print("\nEnter your password: ", justify='left', style="blink bold blue")
        password = input()
        clear_screen()
        print_sign_up()
        console.print("\nEnter your email address: ", justify='left', style="blink bold yellow")
        console.print(email, justify='left', style="blink bold cyan")
        console.print("\nEnter your username: ", justify='left', style="blink bold green")
        console.print(username, justify='left', style="blink bold cyan")
        console.print("\nEnter your password: ", justify='left', style="blink bold blue")
        console.print(password, justify='left', style="blink bold cyan")
        console.print("\nConfirm your password: ", justify='left', style="blink bold magenta")
        confirm_password = input()

    clear_screen()
    print_sign_up()
    console.print("Enter your email address: ", justify='left', style="blink bold yellow")
    console.print(email, justify='left', style="blink bold cyan")
    console.print("\nEnter your username: ", justify='left', style="blink bold green")
    console.print(username, justify='left', style="blink bold cyan")
    console.print("\nEnter your password: ", justify='left', style="blink bold blue")
    console.print(password, justify='left', style="blink bold cyan")
    console.print("\nConfirm your password: ", justify='left', style="blink bold magenta")
    console.print(confirm_password, justify='left', style="blink bold cyan")

    users[username] = {"email": email, "username": username, "password": password, "active": True}
    save_users(users)

    user_filename = f"{username}.json"
    user_path = os.path.join("users", user_filename)
    with open(user_path, 'w') as file:
        json.dump(users[username], file)

    print("[bold green]\nAccount created successfully![/bold green]")
    input("Press Enter to continue...")
    clear_screen()


def print_account(email, username, password, console):
    console = Console(width=50)
    print_your_account()
    overflow_methods: List[OverflowMethod] = ["Email"]
    for overflow in overflow_methods:
        console.rule(overflow)
        print("\n")
        console.print(email, overflow=overflow, style="blink bold cyan", justify='center')
        print("\n")

    overflow_methods_u: List_u[OverflowMethod] = ["Username"]
    for overflow_u in overflow_methods_u:
        console.rule(overflow_u)
        print("\n")
        console.print(username, overflow=overflow_u, style="blink bold yellow", justify='center')
        print("\n")

    overflow_methods_p: List_p[OverflowMethod] = ["Password"]
    for overflow_p in overflow_methods_p:
        console.rule(overflow_p)
        print("\n")
        console.print(password, overflow=overflow_p, style="blink bold cyan", justify='center')
        print("\n")

def account():
    project_manager = ProjectManager()
    project_manager.load_projects()

    while True:
        print("1. Create Project")
        print("2. Delete Project")
        print("3. Add Member to Project")
        print("4. Remove Member from Project")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            project_id = input("Enter Project ID: ")
            title = input("Enter Project Title: ")
            owner_username = input("Enter Owner Username: ")
            owner = User(owner_username)
            project_manager.create_project(project_id, title, owner)

        elif choice == "2":
            project_id = input("Enter Project ID: ")
            username = input("Enter Your Username: ")
            project_manager.delete_project(project_id, username)
            

        elif choice == "3":
            project_id = input("Enter Project ID: ")
            member_username = input("Enter Member Username: ")
            member = User(member_username)
            project_manager.add_member_to_project(project_id, member)

        elif choice == "4":
            project_id = input("Enter Project ID: ")
            member_to_remove_username = input("Enter Member Username to Remove: ")
            member_to_remove = User(member_to_remove_username)
            requesting_user = input("Enter Your Username: ")
            project_manager.remove_member_from_project(project_id, member_to_remove, requesting_user)

        
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid Choice!")


def login():
    console = Console(width=50)
    users = load_users()
    print_login()

    console.print("Enter your username: ", justify='left', style="blink bold magenta")
    username = input()
    clear_screen()
    print_login()
    console.print("Enter your username: ", justify='left', style="blink bold magenta")
    console.print(username, justify='left', style="blink bold cyan")
    console.print("\nEnter your password: ", justify='left', style="blink bold blue")
    password = input()
    clear_screen()
    print_login()
    console.print("Enter your username: ", justify='left', style="blink bold magenta")
    console.print(username, justify='left', style="blink bold cyan")
    console.print("\nEnter your password: ", justify='left', style="blink bold blue")
    console.print(password, justify='left', style="blink bold cyan")

    if any(user["username"] == username and user["password"] == password for user in users.values()):
        print("[bold green]\nLogin successful![/bold green]")
        input("Press Enter to continue...")
        clear_screen()
        print_account(users[username]['email'], username, users[username]['password'], console)
        input("Press Enter to continue...")
        clear_screen()
        '''
        remember_choice = input("[cyan]Do you want to remember your username and password for a week? (y/n)[/cyan]")
        if remember_choice.lower() == 'y':
            expiry_date = datetime.datetime.now() + datetime.timedelta(days=7)
            users[username]["remembered_until"] = expiry_date.strftime("%Y-%m-%d")
            save_users(users)
        input("Press Enter to continue...")
        clear_screen()
        '''
        account()
    else:
        print("[bold red]Invalid username or password![/bold red]")
        print(f"[cyan]Do you have an account?(y/n)[/cyan]")
        answer = input()
        if answer.lower() == 'y':
            clear_screen()
            login()
        elif answer.lower() == 'n':
            clear_screen()
            create_account()
        else:
            clear_screen()
            print("[bold red]Invalid input! [/bold red]")
            input("Press Enter to continue...")
            clear_screen()



def main():
    clear_screen()
    while True:
        table = Table(width=40, show_header=True, show_lines=True, style="bold magenta")

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
        elif choice == '2':
            login()
        else:
            print("[blue]Good luck[/blue] ")
            exit()


if __name__ == "__main__":
    main()