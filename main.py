import asyncio
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from random import randint
from rich.console import Console, OverflowMethod
from rich.table import Table
from rich import print
import json
from rich import print
from typing import List
import os
from enum import Enum
import uuid
import re
import hashlib
import logging
from rich.box import SIMPLE
from datetime import datetime, timedelta
import time

logging.basicConfig(filename='Account/logfile.log', level=logging.INFO)
logger = logging.getLogger()

fileHandler = logging.FileHandler('logfile.log')
logger.addHandler(fileHandler)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


class User:
    def __init__(self, email, username, password, active=True):
        self.email = email
        self.username = username
        self.password = password
        self.active = active


class UserManager:
    def __init__(self, users_file="Account/account.json"):
        self.users_file = users_file
        self.project_manager = ProjectManager()

    def save_users(self, users):
        with open(self.users_file, "w") as file:
            json.dump(users, file, indent=4)

    def load_users(self):
        try:
            with open(self.users_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def create_user(self, email, username, password):
        users = self.load_users()
        users[username] = {"email": email, "username": username, "password": password, "active": True}
        self.save_users(users)
        logger.info(f"user {username} sigend up successfully.")
        return User(email, username, password)

    def get_user_projects(self, username):
        projects = ProjectManager().load_projects()
        user_projects = [proj for proj in projects.values() if
                         proj.get("owner") == username or (proj.get("members") and username in proj.get("members"))]
        return user_projects

    def display_project_members(self, project):
        members = project.get("members", [])
        console = Console()  # Initialize the Console object
        if members:
            console.print("Project Members:", style="bold")  # Display the header
            for index, member in enumerate(members, 1):
                console.print(f"{index}. {member}")  # Display the members
        else:
            console.print("Error: No members found for this project.",
                          style='bold red')  # Display error message if no members found
            logger.info(f"Error: No members found for project {project}.")

    def print_sign_up(self):
        console = Console(width=50)
        console.print("  ┏┓•          ", justify='left', style="blink bold red")
        console.print("  ┗┓┓┏┓┏┓  ┓┏┏┓", justify='left', style="blink bold red")
        console.print("  ┗┛┗┗┫┛┗  ┗┻┣┛", justify='left', style="blink bold red")
        console.print("      ┛      ┛ ", justify='left', style="blink bold red")

    def print_your_account(self):
        console = Console(width=50)
        console.print("  ┬ ┬┌─┐┬ ┬┬─┐  ┌─┐┌─┐┌─┐┌─┐┬ ┬┌┐┌┌┬┐", justify='center', style="blink bold white")
        console.print("  └┬┘│ ││ │├┬┘  ├─┤│  │  │ ││ ││││ │ ", justify='center', style="blink bold white")
        console.print("   ┴ └─┘└─┘┴└─  ┴ ┴└─┘└─┘└─┘└─┘┘└┘ ┴ \n", justify='center', style="blink bold white")

    def print_login(self):
        console = Console(width=50)
        console.print("  ┓     •  ", justify='left', style="blink bold green")
        console.print("  ┃ ┏┓┏┓┓┏┓", justify='left', style="blink bold green")
        console.print("  ┗┛┗┛┗┫┗┛┗", justify='left', style="blink bold green")
        console.print("       ┛   ", justify='left', style="blink bold green")

    def is_valid_email(self, email):
        console = Console(width=50)
        while not email.endswith("@gmail.com"):
            print("[bold red]Error: Invalid email format![/bold red]"
                  "\n[cyan]Valid example: iust@gmail.com[/cyan]")
            logging.info("Error: Invalid email format!")

            input("Press Enter to continue...")
            clear_screen()
            self.print_sign_up()
            console.print("\nEnter your email address: ", justify='left', style="blink bold yellow")
            email = input()
        return email

    def is_valid_password(self, email, username):
        console = Console(width=50)
        console.print("\nEnter your password: ", justify='left', style="blink bold blue")
        password = input()
        while not (any(char.isupper() for char in password) and any(char.islower() for char in password) \
                   and any(char in "~@#$!%^&*?" for char in password) and any(char.isdigit() for char in password) \
                   and len(password) == 8):
            print("[bold red]Error: Invalid password! "
                  "\nYour password must have 8 characters, "
                  "\nat least one uppercase letter, "
                  "\nat least one lowercase letter, "
                  "\nat least one number, "
                  "\nand at least one of the characters '~@#$!%^&*?'[/bold red]")
            logging.info("Invalid password!")

            print("[cyan]Valid example: Iust@ac1[/cyan]")
            input("Press Enter to continue...")
            clear_screen()
            self.print_sign_up()
            console.print("\nEnter your email address: ", justify='left', style="blink bold yellow")
            console.print(email, justify='left', style="blink bold cyan")
            console.print("\nEnter your username: ", justify='left', style="blink bold green")
            console.print(username, justify='left', style="blink bold cyan")
            console.print("\nEnter your password: ", justify='left', style="blink bold blue")

            password = input()

        return (password, email, username)

    def sign_up(self):
        console = Console(width=50)
        users = self.load_users()

        self.print_sign_up()
        console.print("\nEnter your email address: ", justify='left', style="blink bold yellow")
        email = self.is_valid_email(input())

        while any(user_data['email'] == email for user_data in users.values()):
            print("[bold red]Error: Email already exists![/bold red]")
            logging.info("Error: Email already exists!")
            input("Press Enter to continue...")
            clear_screen()
            self.print_sign_up()
            console.print("\nEnter your email address: ", justify='left', style="blink bold yellow")
            email = input()

        clear_screen()
        self.print_sign_up()
        console.print("\nEnter your email address: ", justify='left', style="blink bold yellow")
        console.print(email, justify='left', style="blink bold cyan")
        console.print("\nEnter your username: ", justify='left', style="blink bold green")
        username = input()

        while username in users:
            print("[bold red]Error: Username already exists![/bold red]")
            logging.info("Error: Username already exists!")
            input("Press Enter to continue...")
            clear_screen()
            self.print_sign_up()
            console.print("\nEnter your email address: ", justify='left', style="blink bold yellow")
            console.print(email, justify='left', style="blink bold cyan")
            console.print("\nEnter your username: ", justify='left', style="blink bold green")
            username = input()

        clear_screen()
        self.print_sign_up()
        console.print("\nEnter your email address: ", justify='left', style="blink bold yellow")
        console.print(email, justify='left', style="blink bold cyan")
        console.print("\nEnter your username: ", justify='left', style="blink bold green")
        console.print(username, justify='left', style="blink bold cyan")

        password, email, username = self.is_valid_password(email, username)
        clear_screen()
        self.print_sign_up()
        console.print("\nEnter your email address: ", justify='left', style="blink bold yellow")
        console.print(email, justify='left', style="blink bold cyan")
        console.print("\nEnter your username: ", justify='left', style="blink bold green")
        console.print(username, justify='left', style="blink bold cyan")
        console.print("\nEnter your password: ", justify='left', style="blink bold blue")
        console.print(password, justify='left', style="blink bold cyan")
        console.print("\nConfirm your password: ", justify='left', style="blink bold magenta")
        confirm_password = input()

        while password != confirm_password:
            print("[bold red]Error: Passwords do not match![/bold red]")
            logging.info("Error: Passwords do not match!")
            input("Press Enter to continue...")
            clear_screen()
            self.print_sign_up()
            console.print("\nEnter your email address: ", justify='left', style="blink bold yellow")
            console.print(email, justify='left', style="blink bold cyan")
            console.print("\nEnter your username: ", justify='left', style="blink bold green")
            console.print(username, justify='left', style="blink bold cyan")
            console.print("\nEnter your password: ", justify='left', style="blink bold blue")
            password = input()
            clear_screen()
            self.print_sign_up()
            console.print("\nEnter your email address: ", justify='left', style="blink bold yellow")
            console.print(email, justify='left', style="blink bold cyan")
            console.print("\nEnter your username: ", justify='left', style="blink bold green")
            console.print(username, justify='left', style="blink bold cyan")
            console.print("\nEnter your password: ", justify='left', style="blink bold blue")
            console.print(password, justify='left', style="blink bold cyan")
            console.print("\nConfirm your password: ", justify='left', style="blink bold magenta")
            confirm_password = input()

        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        clear_screen()
        self.print_sign_up()
        console.print("Enter your email address: ", justify='left', style="blink bold yellow")
        console.print(email, justify='left', style="blink bold cyan")
        console.print("\nEnter your username: ", justify='left', style="blink bold green")
        console.print(username, justify='left', style="blink bold cyan")
        console.print("\nEnter your password: ", justify='left', style="blink bold blue")
        console.print(password, justify='left', style="blink bold cyan")
        console.print("\nConfirm your password: ", justify='left', style="blink bold magenta")
        console.print(confirm_password, justify='left', style="blink bold cyan")

        users[username] = {"email": email, "username": username, "password": hashed_password, "active": True}
        self.save_users(users)
        print("[bold green]\nAccount created successfully![/bold green]")
        logging.info("Account created successfully")
        input("Press Enter to continue...")
        self.create_user(email, username, hashed_password)
        clear_screen()

    def print_account(self, email, username, password, console):
        self.print_your_account()

        overflow_methods: List[OverflowMethod] = ["Email"]
        for overflow in overflow_methods:
            console.rule(overflow)
            print("\n")
            console.print(email, overflow=overflow, style="blink bold cyan", justify='center')
            print("\n")

        overflow_methods_u: List[OverflowMethod] = ["Username"]
        for overflow_u in overflow_methods_u:
            console.rule(overflow_u)
            print("\n")
            console.print(username, overflow=overflow_u, style="blink bold yellow", justify='center')
            print("\n")

        overflow_methods_p: List[OverflowMethod] = ["Password"]
        for overflow_p in overflow_methods_p:
            console.rule(overflow_p)
            print("\n")
            console.print("********", overflow=overflow_p, justify='center', style="blink bold cyan")
            print("\n")

    def login(self):
        console = Console(width=50)
        users = self.load_users()
        project_manager = ProjectManager()
        self.print_login()
        console.print("Enter your username: ", justify='left', style="blink bold magenta")
        username = input()
        clear_screen()
        self.print_login()
        console.print("Enter your username: ", justify='left', style="blink bold magenta")
        console.print(username, justify='left', style="blink bold cyan")
        console.print("\nEnter your password: ", justify='left', style="blink bold blue")
        password = input()
        clear_screen()
        self.print_login()
        console.print("Enter your username: ", justify='left', style="blink bold magenta")
        console.print(username, justify='left', style="blink bold cyan")
        console.print("\nEnter your password: ", justify='left', style="blink bold blue")
        console.print(password, justify='left', style="blink bold cyan")

        # Hash the input password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if any(user["username"] == username and user["password"] == hashed_password for user in users.values()):
            print("[bold green]\nLogin successful![/bold green]")
            logging.info("Login successful!")
            input("Press Enter to continue...")
            clear_screen()
            self.print_account(users[username]['email'], username, users[username]['password'], console)
            input("Press Enter to continue...")
            clear_screen()
            project_manager.account(username)
        else:
            print("[bold red]Error: Invalid username or password![/bold red]")
            logging.info("Error: Invalid username or password!")
            print(f"[cyan]Do you have an account?(y/n)[/cyan]")
            answer = input()
            if answer.lower() == 'y':
                clear_screen()
                self.login()
            elif answer.lower() == 'n':
                clear_screen()
                self.sign_up()
            else:
                clear_screen()
                print("[bold red]Error: Invalid input! [/bold red]")
                logging.info("Error: Invalid input!")
                clear_screen()

    def menu(self):
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
                self.sign_up()
            elif choice == '2':
                self.login()
            elif choice == '3':
                async def demo(screen):
                    start_time = asyncio.get_event_loop().time()

                    while True:
                        current_time = asyncio.get_event_loop().time()
                        elapsed_time = current_time - start_time
                        if elapsed_time >= 10:
                            screen.clear()
                            screen.refresh()
                            screen.close()  # Close the screen
                            loop.stop()  # Stop the event loop
                            return

                        screen.print_at('EXIT!',
                                        randint(0, screen.width), randint(0, screen.height),
                                        colour=randint(0, screen.colours - 1),
                                        bg=randint(0, screen.colours - 1))
                        ev = screen.get_key()
                        if ev in (ord('Q'), ord('q')):
                            return
                        screen.refresh()
                        await asyncio.sleep(0.05)

                screen = Screen.open()
                loop = asyncio.new_event_loop()
                task = loop.create_task(demo(screen))
                loop.run_forever()
                loop.close()
                exit()
            else:
                print("[bold red]Error: Invalid choice. Please enter 1, 2, or 3.[/bold red]")
                logging.info("Error: Invalid choice.")
                input("Press Enter to continue...")
                clear_screen()


class Project:
    def __init__(self, project_id, title, owner):
        self.project_id = project_id
        self.title = title
        self.owner = owner


class ProjectManager:
    def __init__(self, projects_file="Account/projects.json"):
        self.projects_file = projects_file

    def save_projects(self, projects):
        with open(self.projects_file, "w") as file:
            json.dump(projects, file, indent=4)

    def load_projects(self):
        try:
            with open(self.projects_file, "r") as file:
                data = file.read()
                if not data:
                    return {}  # Return an empty dictionary if the file is empty
                return json.loads(data)
        except FileNotFoundError:
            return {}

    def print_your_projects(self):
        console = Console(width=50)
        console.print("  ╦ ╦┌─┐┬ ┬┬─┐  ┌─┐┬─┐┌─┐ ┬┌─┐┌─┐┌┬┐┌─┐", justify='center', style='blink bold red')
        console.print("  ╚╦╝│ ││ │├┬┘  ├─┘├┬┘│ │ │├┤ │   │ └─┐", justify='center', style='blink bold white')
        console.print("   ╩ └─┘└─┘┴└─  ┴  ┴└─└─┘└┘└─┘└─┘ ┴ └─┘", justify='center', style='blink bold red')

    def check_project_existence(self, project_id):
        projects = self.load_projects()
        return project_id in projects

    def create_project(self, project_id, title, owner):
        projects = self.load_projects()

        # Check if project_id or title is empty
        if not project_id or not title:
            print("[bold red]Error: Project ID and title cannot be empty![/bold red]")
            input("Press Enter to continue...")
            clear_screen()
            return None

        # Check if the project_id already exists
        if project_id in projects:
            print("[bold red]Erorr: Project ID already exists! Please choose a different one.[/bold red]")
            logging.info(f"Erorr: Project ID {project_id} already exists!")
            input("Press Enter to continue...")
            clear_screen()
            return None

        # Check if the project with the same title already exists for the owner
        for proj in projects.values():
            if proj["title"] == title and proj.get("owner") == owner:
                print(
                    "[bold red]Erorr: You already have a project with the same title! Please choose a different title.[/bold red]")
                logging.error(f"You already have a project with the same title: {title} owned by {owner}!")
                input("Press Enter to continue...")
                clear_screen()
                return None

        # If all checks pass, create the project
        print("[bold green]Project created successfully![/bold green]")
        logger.info(f"{owner} created project {title} successfully.")
        input("Press Enter to continue...")
        clear_screen()
        projects[project_id] = {"title": title, "project_id": project_id, "owner": owner}
        self.save_projects(projects)
        return Project(project_id, title, owner)

    def delete_project(self, owner):
        selected_project = self.select_project(owner)
        if selected_project is None:
            return False

        confirm = input(f"Are you sure you want to delete '{selected_project['title']}' project? (y/n): ")
        if confirm.lower() == 'y':
            projects = self.load_projects()
            del projects[selected_project['project_id']]
            self.save_projects(projects)
            logger.info(f"{owner} deleted project {selected_project['title']} successfully.")
            print("[bold green]Project deleted successfully![/bold green]")
            input("Press Enter to continue...")
            clear_screen()
            return True
        else:
            print("Deletion canceled.")
            logger.info(f"[bold red]Error: project {selected_project['title']} Deletion canceled.[/bold red]")
            input("Press Enter to continue...")
            clear_screen()
            return False

    def print_add_member(self):
        console = Console(width=50)
        console.print("  ┌─┐┌┬┐┌┬┐  ┌┬┐┌─┐┌┬┐┌┐ ┌─┐┬─┐", justify='center', style="blink bold magenta")
        console.print("  ├─┤ ││ ││  │││├┤ │││├┴┐├┤ ├┬┘", justify='center', style="blink bold cyan")
        console.print("  ┴ ┴─┴┘─┴┘  ┴ ┴└─┘┴ ┴└─┘└─┘┴└─", justify='center', style="blink bold magenta")

    def add_member_to_project(self, project_id, member, username):
        user_manager = UserManager()
        projects = self.load_projects()
        users = user_manager.load_users()

        if project_id in projects:
            project = projects[project_id]
            if project["owner"] == username:
                if member in users:
                    project["members"] = project.get("members", [])
                    if member not in project["members"]:
                        project["members"].append(member)
                        print(
                            f"[bold green]Member '{member}' added to project '{project['title']}' successfully.[/bold green]")
                        logger.info(f"Member '{member}' added to project '{project['title']}' successfully.")
                        self.save_projects(projects)
                        print("Press Enter to continue...")
                        input()
                        clear_screen()
                    else:
                        print(
                            f"[bold red]Erorr: Member '{member}' is already a member of project '{project['title']}'.[/bold red]")
                        logging.info(f"Erorr: Member '{member}' is already a member of project '{project['title']}'.")
                        print("Press Enter to continue...")
                        input()
                        clear_screen()
                else:
                    print("[bold red]Erorr: User not found![/bold red]")
                    logging.error(f"Erorr: User '{member}' not found!")
                    print("Press Enter to continue...")
                    input()
                    clear_screen()
            else:
                print("[bold red]Erorr: You are not the owner of this project![/bold red]")
                logging.info("Erorr: You are not the owner of this project!")
                print("Press Enter to continue...")
                input()
                clear_screen()
        else:
            print(f"[bold red]Erorr: Project with ID '{project_id}' not found.[/bold red]")
            logging.info(f"Erorr: Project with ID '{project_id}' not found.")
            print("Press Enter to continue...")
            input()
            clear_screen()

    def print_members_of_project(self):
        console = Console(width=70)
        console.print("  ╔╦╗┌─┐┌┬┐┌┐ ┌─┐┬─┐┌─┐  ┌─┐┌─┐  ┌─┐┬─┐┌─┐ ┬┌─┐┌─┐┌┬┐", justify='left',
                      style="blink bold magenta")
        console.print("  ║║║├┤ │││├┴┐├┤ ├┬┘└─┐  │ │├┤   ├─┘├┬┘│ │ │├┤ │   │ ", justify='left',
                      style="blink bold yellow")
        console.print("  ╩ ╩└─┘┴ ┴└─┘└─┘┴└─└─┘  └─┘└    ┴  ┴└─└─┘└┘└─┘└─┘ ┴ ", justify='left',
                      style="blink bold magenta")

    def remove_member_from_project(self, project_id, username):
        console = Console(width=50)
        projects = self.load_projects()
        if project_id in projects:
            project = projects[project_id]
            if project["owner"] == username:
                if "members" in project:
                    self.print_members_of_project()

                    table = Table(padding=(0, 10, 0, 10))
                    table.add_column("No.", justify="center", style="bold yellow")
                    table.add_column("Member", justify="center", style="bold magenta")

                    for index, member in enumerate(project["members"], 1):
                        table.add_row(str(index), member)

                    console.print(table)

                    while True:
                        console.print("Enter the number of the member you want to remove: ", justify='center')
                        choice = input()
                        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(project["members"]):
                            print("[bold red]Error: Invalid choice! Please enter a valid number.[/bold red]")
                            logging.info("Error: Invalid choice! Please enter a valid number.")
                            input("Press Enter to continue...")
                            clear_screen()
                            self.print_members_of_project()
                            console.print(table)
                            continue

                        member_to_remove = project["members"][int(choice) - 1]
                        confirm = input(
                            f"Are you sure you want to remove '{member_to_remove}' from project '{project['title']}'? (y/n): ")
                        if confirm.lower() == 'y':
                            project["members"].remove(member_to_remove)
                            self.save_projects(projects)
                            logger.info(
                                f"Member '{member_to_remove}' removed from project '{project['title']}' successfully.")
                            print("[bold green]Member removed successfully![/bold green]")
                            input("Press Enter to continue...")
                            clear_screen()
                            return True

                        else:
                            print("[bold red]Error: Remove canceled.[/bold red]")
                            logging.info("Error: Remove canceled.")
                            clear_screen()
                            return False

                else:
                    print("[bold red]Error: This project has no members.[/bold red]")
                    logging.info("Error: This project has no members.")
                    clear_screen()
            else:
                print("[bold red]Error: You are not the owner of this project![/bold red]")
                logging.info(f"Error: You are not the owner of project '{project['title']}'!")
                input("Press Enter to continue...")
                clear_screen()
        else:
            print(f"[bold red]Error: Project with ID '{project_id}' not found.[/bold red]")
            logging.info(f"Error: Project with ID '{project_id}' not found.")
            input("Press Enter to continue...")
            clear_screen()

    def view_projects(self, username):
        projects = self.load_projects()

        # Create a table with four columns: Project Title, Owner, Role, and Members
        self.print_your_projects()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Project Title", justify="center", style="cyan")
        table.add_column("Owner", justify="center", style="cyan")
        table.add_column("Role", justify="center", style="cyan")
        table.add_column("Members", justify="center", style="cyan")  # New column for members

        for proj_id, proj in projects.items():
            members = ', '.join(proj.get("members", []))  # Joining members with comma separator
            # Check if the user is the owner of the project
            if proj["owner"] == username:
                table.add_row(proj["title"], "You", "Owner", members)
            # Check if the user is a member of the project
            elif "members" in proj and username in proj["members"]:
                table.add_row(proj["title"], proj["owner"], "Member", members)

        console = Console()
        console.print(table)

    def select_project(self, username):
        console = Console(width=50)
        projects = self.load_projects()
        owner_projects = [proj for proj in projects.values() if proj["owner"] == username]

        if not owner_projects:
            console.print("[bold red]Error: You are not associated with any projects.[/bold red]")
            logging.info("Error: You are not associated with any projects.")
            input("Press Enter to continue...")
            clear_screen()
            return None

        self.print_your_projects()
        time.sleep(0.5)

        table = Table(padding=(0, 8, 0, 8))

        table.add_column("No.", justify="center", style="bold cyan")
        table.add_column("Project Title", justify="center", style="bold magenta")

        for index, project in enumerate(owner_projects, 1):
            table.add_row(str(index), project['title'])

        console.print(table)

        while True:
            console.print("\nEnter the project number: ", justify='center', style='bold white')
            project_choice = input()
            if re.match("^\d+$", project_choice):
                project_choice = int(project_choice) - 1
                if 0 <= project_choice < len(owner_projects):
                    break
                else:
                    console.print("[bold red]Error: Invalid project choice.[/bold red]")
                    logging.info("Error: Invalid project choice")
                    input("Press Enter to continue...")
                    clear_screen()
                    self.print_your_projects()
                    console.print(table)
            else:
                console.print("[bold red]Error: Please enter a valid project number.[/bold red]")
                logging.info("Error: Invalid project number")
                input("Press Enter to continue...")
                clear_screen()
                self.print_your_projects()
                console.print(table)

        selected_project = owner_projects[project_choice]
        return selected_project

    def show_project(self, username):
        console = Console(width=50)
        projects = self.load_projects()
        person_projects = [proj for proj in projects.values() if
                           proj["owner"] == username or (proj.get("members") and username in proj["members"])]

        if not person_projects:
            console.print("[bold red]Error: You are not associated with any projects.[/bold red]")
            logging.info("Error: You are not associated with any projects.")
            input("Press Enter to continue...")
            clear_screen()
            return None

        self.print_your_projects()

        table = Table(padding=(0, 8, 0, 8))

        table.add_column("No.", justify="center", style="bold yellow")
        table.add_column("Project Title", justify="center", style="bold cyan")

        for index, project in enumerate(person_projects, 1):
            table.add_row(str(index), project['title'])

        console.print(table)

        while True:
            console.print("\nEnter the project number: ", justify='center', style='bold white')
            project_choice = input()
            if re.match("^\d+$", project_choice):
                project_choice = int(project_choice) - 1
                if 0 <= project_choice < len(person_projects):
                    break
                else:
                    console.print("[bold red]Error: Invalid project choice[/bold red]")
                    logging.info("Error: Invalid project choice")
                    input("Press Enter to continue...")
                    clear_screen()
                    self.print_your_projects()
                    console.print(table)
            else:
                console.print("[bold red]Please enter a valid project number.[/bold red]")
                logging.info("Please enter a valid project number.")
                input("Press Enter to continue...")
                clear_screen()
                self.print_your_projects()
                console.print(table)

        selected_project = person_projects[project_choice]
        return selected_project

    def print_project_manager_menu(self):
        console = Console(width=80)
        console.print("  ╔═╗┬─┐┌─┐ ┬┌─┐┌─┐┌┬┐  ╔╦╗┌─┐┌┐┌┌─┐┌─┐┌─┐┌┬┐┌─┐┌┐┌┌┬┐  ╔╦╗┌─┐┌┐┌┬ ┬", justify='left',
                      style='blink bold cyan')
        console.print("  ╠═╝├┬┘│ │ │├┤ │   │   ║║║├─┤│││├─┤│ ┬├┤ │││├┤ │││ │   ║║║├┤ ││││ │", justify='left',
                      style='blink bold cyan')
        console.print("  ╩  ┴└─└─┘└┘└─┘└─┘ ┴   ╩ ╩┴ ┴┘└┘┴ ┴└─┘└─┘┴ ┴└─┘┘└┘ ┴   ╩ ╩└─┘┘└┘└─┘\n", justify='left',
                      style='blink bold cyan')

    def edit_project_menu(self, username, selected_project):
        task_manager = TaskManager()
        console = Console(width=60)
        while True:
            clear_screen()
            self.print_project_manager_menu()
            time.sleep(0.7)
            console.print("1. Add Member to Project", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("2. Remove Member from Project", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("3. Manage Tasks", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("4. Exit", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("Choose an option: ", justify='center', style="blink bold yellow")
            choice = input()
            clear_screen()
            if choice == '1':
                clear_screen()
                self.print_add_member()
                member = input("Enter the username of the member you want to add: ")
                self.add_member_to_project(selected_project['project_id'], member, username)
            elif choice == '2':
                clear_screen()
                self.remove_member_from_project(selected_project['project_id'], username)
            elif choice == '3':
                clear_screen()
                task_manager.tasks_menu(username, selected_project)
            elif choice == '4':
                clear_screen()
                break

            else:
                print("[bold red]Invalid choice. Please try again.[/bold red]")
                input("Press Enter to continue...")

    def print_project_menu(self):
        console = Console(width=50)
        console.print("  ╔═╗┬─┐┌─┐ ┬┌─┐┌─┐┌┬┐┌─┐  ┌┬┐┌─┐┌┐┌┬ ┬", justify='center', style="blink bold magenta")
        console.print("  ╠═╝├┬┘│ │ │├┤ │   │ └─┐  │││├┤ ││││ │", justify='center', style="blink bold magenta")
        console.print("  ╩  ┴└─└─┘└┘└─┘└─┘ ┴ └─┘  ┴ ┴└─┘┘└┘└─┘\n", justify='center', style="blink bold magenta")

    def print_create_project(self):
        console = Console(width=50)
        console.print("  ┌─┐┬─┐┌─┐┌─┐┌┬┐┌─┐  ┌─┐┬─┐┌─┐ ┬┌─┐┌─┐┌┬┐", justify='center', style="blink bold yellow")
        console.print("  │  ├┬┘├┤ ├─┤ │ ├┤   ├─┘├┬┘│ │ │├┤ │   │ ", justify='center', style="blink bold yellow")
        console.print("  └─┘┴└─└─┘┴ ┴ ┴ └─┘  ┴  ┴└─└─┘└┘└─┘└─┘ ┴ \n", justify='center', style="blink bold yellow")

    def create_project_design(self):

        console = Console(width=50)
        self.print_create_project()
        overflow_methods: List[OverflowMethod] = ["Enter project ID: "]
        for overflow in overflow_methods:
            console.rule(overflow, style="bold yellow")
            print("\n")
            project_id = input()
            clear_screen()
            self.print_create_project()
            console.rule(overflow)
            print("\n")
            console.print(project_id, overflow=overflow, style="blink bold cyan", justify='center')
            print("\n")

        overflow_methods_u: List[OverflowMethod] = ["Enter project title: "]
        for overflow_u in overflow_methods_u:
            console.rule(overflow_u, style="bold yellow")
            print("\n")
            title = input()
            clear_screen()
            self.print_create_project()
            console.rule(overflow, style="bold magenta")
            print("\n")
            console.print(project_id, overflow=overflow, style="blink bold cyan", justify='center')
            print("\n")
            console.rule(overflow, style="bold magenta")
            print("\n")
            console.print(title, overflow=overflow_u, style="blink bold yellow", justify='center')
            print("\n")
        return project_id, title

    def account(self, username):
        console = Console(width=50)
        while True:
            self.print_project_menu()
            time.sleep(0.7)
            console.print("1. Create Project", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("2. Edit Project", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("3. Delete Project", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("4. View Projects", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("5. Logout", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("Choose an option: ", justify='center', style="blink bold yellow")
            choice = input()
            clear_screen()
            if choice == '1':
                project_id, title = self.create_project_design()
                self.create_project(project_id, title, username)

            elif choice == '2':
                selected_project = self.show_project(username)
                if selected_project:
                    self.edit_project_menu(username, selected_project)

            elif choice == '3':
                self.delete_project(username)


            elif choice == '4':
                self.view_projects(username)
                print()
                console.print("Press Enter to continue...", justify='center')
                input()
                clear_screen()

            elif choice == '5':
                break
            else:
                print("[bold red]Error: Invalid choice. Please try again.[/bold red]")
                logging.info("Error: Invalid choice.")
                input("Press Enter to continue...")
                clear_screen()
                continue


class Priority(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Status(Enum):
    BACKLOG = "BACKLOG"
    TODO = "TODO"
    DOING = "DOING"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"


class Task:
    def __init__(self, label, title, description, deadline, assignees, priority=Priority.LOW, status=Status.BACKLOG,
                 comments=None):
        self.label = label
        self.title = title
        self.description = description
        self.deadline = deadline
        self.assignees = assignees
        self.priority = priority
        self.status = status
        self.comments = comments if comments else []

    def add_comment(self, comment):
        self.comments.append(comment)


class TaskManager:
    def __init__(self, tasks_file="Account/tasks.json", history_file="Account/history.json"):
        self.tasks_file = tasks_file
        self.history_file = history_file
        self.tasks = self.load_tasks()

    def save_tasks(self, tasks):
        with open(self.tasks_file, "w") as file:
            json.dump(tasks, file, indent=4)

    def load_tasks(self):
        try:
            with open(self.tasks_file, "r") as file:
                tasks = json.load(file)
                if not isinstance(tasks, dict):
                    print("Error: Loaded tasks are not in the expected format.")
                    logging.info("Error: Loaded tasks are not in the expected format.")
                    return {}
                return tasks
        except FileNotFoundError:
            return {}

    def save_history(self, project_id, action, field_name, new_value, changer, timestamp):
        # Convert timestamp to datetime object if it's a string
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        try:
            with open(self.history_file, "r") as file:
                history = json.load(file)
        except FileNotFoundError:
            history = []
            with open(self.history_file, "w") as file:
                json.dump(history, file)

        change = {
            "project_id": project_id,
            "action": action,
            "field_name": field_name,
            "new_value": new_value,
            "changer": changer,
            "timestamp": timestamp.isoformat()
        }
        history.append(change)

        with open(self.history_file, "w") as file:
            json.dump(history, file, indent=4)

    def update_task(self, task_id, updated_task):
        if task_id in self.tasks:
            self.tasks[task_id].update(updated_task)
            self.save_tasks(self.tasks)
            print("[bold green]Task updated successfully.[/bold green]")
            logger.info(f"Task {task_id} updated successfully.")
        else:
            print("Error: Task not found.")
            logger.info(f"Error: Task {task_id} not found.")

    def get_valid_datetime(self):
        console = Console(width=60)
        while True:
            console.print("Enter the task deadline (2024-09-04 04:09): ", justify='center', style='white underline')
            datetime_input = input()
            if not datetime_input:
                return None  # Return None if the input is empty
            try:
                datetime_obj = datetime.strptime(datetime_input, "%Y-%m-%d %H:%M")
                if datetime_obj < datetime.now():
                    console.print("\nError: Invalid date and time. It should be in the future.", justify='center',
                                  style='red')
                    logging.info("Error: Invalid date and time. It should be in the future.")
                    continue
                return datetime_obj
            except ValueError:
                console.print(
                    "\nError: Invalid date format. Please enter the date and time in the format YYYY-MM-DD HH:MM.",
                    justify='center', style='red')
                logging.info(
                    "Error: Invalid date format. Please enter the date and time in the format YYYY-MM-DD HH:MM.")

    def print_create_task(self):
        console = Console(width=100)
        console.print("     ___ ____   ____  ___  ______  ____    ______  ___   __  __ __", justify='left',
                      style='blink bold yellow')
        console.print("[yellow]    //   || \\\ ||    // \\\ | || | ||       | || | // \\\ (( \ || // [/yellow]",
                      justify='left', style='blink bold yellow')
        console.print("[yellow]   ((    ||_// ||==  ||=||   ||   ||==       ||   ||=||  \\\  ||<<  [/yellow]",
                      justify='left', style='blink bold yellow')
        console.print("[yellow]    \\__  || \\\ ||___ || ||   ||   ||___      ||   || || \_)) || \\\ [/yellow]",
                      justify='left', style='blink bold yellow')

    def create_task(self, username, selected_project):
        console = Console(width=80)
        project_manager = ProjectManager()
        projects = project_manager.load_projects()

        if selected_project['owner'] != username:
            console.print("Error: You do not have permission to create tasks for this project.", justify='center',
                          style='red')
            logging.info("Error: You do not have permission to create tasks for this project.")
            input("Press Enter to continue...")
            clear_screen()
            return

        project_id = selected_project["project_id"]

        while True:
            self.print_create_task()
            print()
            console.print("Enter the task label: ", justify='center', style='white underline')
            label = input()
            if label.strip():
                break
            else:
                console.print("Error: Task label cannot be empty. Please enter a label.", justify='center',
                              style='bold red')
                logging.info("Error: Task label cannot be empty.")
                console.print("Press Enter to continue...", justify='center', style='white')
                input()
                clear_screen()

        console.print("Enter the task title: ", justify='center', style='white underline')
        title = input()
        console.print("Enter the task description: ", justify='center', style='white underline')
        description = input()
        start_datetime = datetime.now()
        end_datetime = self.get_valid_datetime()
        if not end_datetime:
            end_datetime = start_datetime + timedelta(days=1)
        elif end_datetime < start_datetime:
            console.print("Error: Invalid deadline. It should be after the start time.", justify='center', style='red')
            logging.info("Error: Invalid deadline. It should be after the start time.")
            return

        selected_members = []
        while True:
            console.print("Enter the member numbers (comma-separated): ", justify='center', style='white underline')
            console.print("\nMembers in the project:", justify='left', style='blink bold magenta')
            print()
            members = projects[project_id].get('members', [])
            for idx, member in enumerate(members, 1):
                print(f"{idx}. {member}")
                time.sleep(0.5)

            member_choices = input()
            if not member_choices:
                console.print("No members selected for the task. You can add members later.", justify='center',
                              style='bold red')
                logging.info("Error: No members selected for the task. You can add members later.")
                console.print("Do you want to proceed without assigning any members? (y/n): ", justify='center',
                              style='red underline')
                proceed = input()
                if proceed.lower() != 'y':
                    console.print("Task creation cancelled.", justify='center', style='bold red')
                    return
                else:
                    break
            invalid_choice = False
            for choice in member_choices.split(','):
                if choice.isdigit() and 0 < int(choice) <= len(members):
                    selected_members.append(members[int(choice) - 1])
                else:
                    console.print("Error: Invalid member choice.", justify='center', style='bold red')

                    logging.info("Error: Invalid member choice.")
                    invalid_choice = True
                    break
            if not invalid_choice:
                break

        while True:
            console.print("Choose priority (1-4): ", justify='center', style='white underline')
            console.print("\nSelect Priority:", justify='left', style='blink bold magenta')
            time.sleep(0.5)
            print("1. CRITICAL")
            time.sleep(0.5)
            print("2. HIGH")
            time.sleep(0.5)
            print("3. MEDIUM")
            time.sleep(0.5)
            print("4. LOW")
            time.sleep(0.5)
            priority = input()
            if priority.isdigit() and 1 <= int(priority) <= 4:
                selected_priority = {
                    '1': Priority.CRITICAL,
                    '2': Priority.HIGH,
                    '3': Priority.MEDIUM,
                    '4': Priority.LOW
                }.get(priority, Priority.LOW)
                break
            elif not priority:
                selected_priority = Priority.CRITICAL
                break
            else:
                console.print("Error: Invalid input. Please choose a priority between 1 and 4.", justify='center',
                              style='bold red')
                logging.info("Error: Invalid input.")

        console.print(f"Selected priority: {selected_priority}\n", justify='center', style='blink bold cyan')

        while True:
            console.print("Choose Status (1-5): ", justify='center', style='white underline')
            console.print("\nSelect Status: ", justify='left', style='blink bold magenta')
            print("1. BACKLOG")
            time.sleep(0.5)
            print("2. TODO")
            time.sleep(0.5)
            print("3. DOING")
            time.sleep(0.5)
            print("4. DONE")
            time.sleep(0.5)
            print("5. ARCHIVED")
            status = input()
            if status.isdigit() and 1 <= int(status) <= 5:
                selected_status = {
                    '1': Status.BACKLOG,
                    '2': Status.TODO,
                    '3': Status.DOING,
                    '4': Status.DONE,
                    '5': Status.ARCHIVED
                }.get(status, Status.BACKLOG)
                break
            elif not status:
                selected_status = Status.BACKLOG
                break
            else:
                console.print("Error: Invalid input. Please choose a status between 1 and 5.", justify='center',
                              style='bold red')
                logging.info("Error: Invalid input.")

        console.print(f"Selected status: {selected_status}\n", justify='center', style='blink bold cyan')
        console.print("Enter comments for the task: ", justify='center', style='white underline')
        comments = input().strip()

        new_task = {
            "task_id": str(uuid.uuid4()),
            "project_id": project_id,
            "label": label,
            "title": title,
            "description": description,
            "deadline": end_datetime.isoformat(),
            "assignees": selected_members,
            "priority": selected_priority.value,
            "status": selected_status.value,
            "comments": [{"username": username, "comment": comments}] if comments else [],
            "created_at": datetime.now().isoformat()
        }

        tasks = self.load_tasks()
        tasks[new_task["task_id"]] = new_task
        self.save_tasks(tasks)
        self.save_history(project_id, "Task Created", label, title, username, datetime.now())

        console.print("Task created successfully!", justify='center', style='bold green')
        logging.info("Task created successfully!")
        console.print("Press Enter to continue...", justify='center', style='bold white')
        input()
        clear_screen()

    def print_edit_task_menu(self):
        console = Console(width=50)
        console.print("  ╔═╗┌┬┐┬┌┬┐  ╔╦╗┌─┐┌─┐┬┌─  ╔╦╗┌─┐┌┐┌┬ ┬", justify='center', style='blink bold cyan')
        console.print("  ║╣  │││ │    ║ ├─┤└─┐├┴┐  ║║║├┤ ││││ │", justify='center', style='blink bold magenta')
        console.print("  ╚═╝─┴┘┴ ┴    ╩ ┴ ┴└─┘┴ ┴  ╩ ╩└─┘┘└┘└─┘", justify='center', style='blink bold cyan')

    def edit_task(self, username, selected_project, selected_task):

        self.load_tasks()
        console = Console(width=50)
        while True:
            clear_screen()
            self.print_edit_task_menu()
            time.sleep(0.7)
            console.print("\n1. Change label", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("2. Change Title", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("3. Change Description", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("4. Change Assignees", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("5. Change Deadline", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("6. Change Priority", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("7. Change Status", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("8. Comments", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("9. Exit", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("Choose an option: ", justify='center')
            choice = input()
            if choice == '1':
                clear_screen()
                if username == selected_project["owner"] or username in selected_task["assignees"]:
                    console.print("Change label:", justify='center', style='blink bold magenta')
                    console.print("Enter new label (or leave blank): ", justify='center', style='white')
                    new_label = input()
                    if new_label:
                        selected_task["label"] = new_label
                        self.save_history(selected_project["project_id"], "Task label Changed", selected_task["title"],
                                          new_label, username, datetime.now())

                        console.print("label changed successfully.", justify='center', style='bold green')
                        logger.info(f"label of task {selected_task} changed to {new_label}")
                        console.print("Press Enter to continue...", justify='center', style='bold white')
                        input()
                        clear_screen()
                    else:
                        console.print("label remains unchanged.", justify='center', style='bold red')
                        logger.info("label remains unchanged.")
                        console.print("Press Enter to continue...", justify='center', style='bold white')
                        input()
                        clear_screen()
                else:
                    console.print("You are not allowed to change this section.", justify='center', style='bold red')
                    logger.info("You are not allowed to change this section.")
                    console.print("Press Enter to continue...", justify='center', style='bold white')
                    input()
                    clear_screen()
                    return

            elif choice == '2':
                clear_screen()
                if username == selected_project["owner"] or username in selected_task["assignees"]:
                    console.print("Change Title: ", justify='center', style='blink bold blue')
                    console.print("Enter new title (leave blank to remove current title): ", justify='center',
                                  style='white')
                    new_title = input()
                    if new_title:
                        selected_task["title"] = new_title
                        self.save_history(selected_project["project_id"], "Task Title Changed", selected_task["title"],
                                          new_title, username, datetime.now())

                        console.print("Title changed successfully.", justify='center', style='bold green')
                        logger.info(f"title of task {selected_task} changed to {new_title}")
                        console.print("Press Enter to continue...", justify='center', style='bold white')
                        input()
                        clear_screen()
                    else:
                        selected_task["title"] = ""
                        self.save_history(selected_project["project_id"], "Task Title Removed", selected_task["title"],
                                          selected_task["title"], username, datetime.now())
                        console.print("Title removed successfully.", justify='center', style='bold green')
                        logger.info(f"Title of task {selected_task} removed successfully.")
                        console.print("Press Enter to continue...", justify='center', style='bold white')
                        input()
                else:
                    console.print("Error: You are not allowed to change this section.", justify='center',
                                  style='bold red')
                    logger.info("Error: You are not allowed to change this section.")
                    console.print("Press Enter to continue...", justify='center', style='bold white')
                    input()
                    return

            elif choice == '3':
                clear_screen()
                if username == selected_project["owner"] or username in selected_task["assignees"]:
                    console.print("Change Description: ", justify='center', style='blink bold magenta')
                    console.print("Enter new description (leave blank to remove current description): ",
                                  justify='center', style='white')
                    new_description = input()
                    if new_description:
                        selected_task["description"] = new_description
                        self.save_history(selected_project["project_id"], "Task Description Changed",
                                          selected_task["title"],
                                          new_description, username, datetime.now())
                        console.print("Description changed successfully.", justify='center', style='bold green')
                        logger.info(f"Description of task {selected_task} changed to {new_description}")
                        console.print("Press Enter to continue...", justify='center', style='bold white')
                        input()
                        clear_screen()
                    else:
                        selected_task["description"] = ""
                        self.save_history(selected_project["project_id"], "Task Description Removed",
                                          selected_task["title"],
                                          selected_task["description"], username, datetime.now())
                        console.print("Description removed successfully.", justify='center', style='bold green')
                        logger.info(f"Description of task {selected_task} removed successfully.")
                        console.print("Press Enter to continue...", justify='center', style='bold white')
                        input()
                        clear_screen()
                else:
                    console.print("Error: You are not allowed to change this section.", justify='center',
                                  style='bold red')
                    logger.info("You are not allowed to change this section.")
                    console.print("Press Enter to continue...", justify='center', style='bold white')
                    input()
                    return

            elif choice == '4':
                clear_screen()
                if username == selected_project["owner"]:
                    while True:  # Loop until valid choice is made
                        console.print("Assignees menu: ", justify='center', style="blink bold blue")
                        console.print("\n1. Add Assignees", justify='center', style='white')
                        console.print("  ", justify='center')
                        console.print("2. Remove Assignees", justify='center', style='white')
                        console.print("  ", justify='center')
                        console.print("3. Exit", justify='center', style='white')
                        console.print("  ", justify='center')
                        console.print("Choose an option: ", justify='center', style='white')
                        assignee_choice = input()

                        if assignee_choice == '1':
                            clear_screen()
                            # Add Assignees
                            available_assignees = [member for member in selected_project["members"] if
                                                   member not in selected_task["assignees"]]
                            if not available_assignees:
                                console.print("Error: There are no available assignees to add.", justify='center',
                                              style='bold red')
                                logging.info("There are no available assignees to add.")
                                console.print("Press Enter to continue...", justify='center', style='bold white')
                                input()
                                clear_screen()
                                break

                            console.print("Available Assignees: ", justify='center', style='bold magenta')
                            for index, assignee in enumerate(available_assignees, 1):
                                console.print(f"{index}. {assignee}", justify='center', style='cyan')
                                console.print("  ", justify='center')
                                time.sleep(0.5)

                            console.print("\nEnter the numbers of the assignees to add (comma-separated): ",
                                          justify='center', style='white')
                            selected_assignees = input().split(',')
                            selected_assignees = [int(x.strip()) - 1 for x in selected_assignees if
                                                  re.match("^\d+$", x.strip())]

                            for index in selected_assignees:
                                if 0 <= index < len(available_assignees):
                                    selected_task["assignees"].append(available_assignees[index])
                                else:
                                    console.print("Error: Invalid assignee choice.", justify='center', style='bold red')
                                    logging.info("Error: Invalid assignee choice.")
                                    console.print("Press Enter to continue...", justify='center', style='bold white')
                                    input()
                                    clear_screen()  # Restart the loop to get input again
                                    break
                            else:
                                self.save_history(selected_project["project_id"], "Assignees Added",
                                                  selected_task["title"],
                                                  ', '.join(selected_task["assignees"]), username, datetime.now())
                                console.print("Assignees added successfully.", justify='center', style='bold green')
                                logger.info(f"Assignees {selected_assignees} added to {selected_task} successfully.")
                                console.print("Press Enter to continue...", justify='center', style='bold white')
                                input()
                                clear_screen()
                                continue  # Exit the loop after successful input

                        elif assignee_choice == '2':
                            clear_screen()
                            # Remove Assignees
                            console.print("Current Assignees:", justify='center', style='blink bold magenta')
                            if not selected_task["assignees"]:
                                console.print("Error: There are no assignees to remove.", justify='center',
                                              style='bold red')
                                logging.info("Error: There are no assignees to remove.")
                                console.print("Press Enter to continue...", justify='center', style='bold white')
                                input()
                                clear_screen()
                                break

                            for index, assignee in enumerate(selected_task["assignees"], 1):
                                console.print(f"{index}. {assignee}", justify='center')
                                time.sleep(0.5)

                            console.print("Enter the numbers of the assignees to remove (comma-separated): ",
                                          justify='center', style='white')
                            selected_assignees = input().split(',')
                            selected_assignees = [int(x.strip()) - 1 for x in selected_assignees if
                                                  re.match("^\d+$", x.strip())]

                            removed_assignees = []
                            for index in selected_assignees:
                                if 0 <= index < len(selected_task["assignees"]):
                                    removed_assignees.append(selected_task["assignees"].pop(index))
                                else:
                                    console.print("Error: Invalid assignee choice.", justify='center', style='bold red')
                                    logging.info("Error: Invalid assignee choice.")
                                    console.print("Press Enter to continue...", justify='center', style='bold white')
                                    input()
                                    clear_screen()
                                    break  # Restart the loop to get input again
                            else:
                                self.save_history(selected_project["project_id"], "Assignees Removed",
                                                  selected_task["title"],
                                                  ', '.join(removed_assignees), username, datetime.now())
                                console.print("Assignees removed successfully.", justify='center', style='bold green')
                                logger.info(
                                    f"Assignees {selected_assignees} removed from {selected_task} successfully.")
                                console.print("Press Enter to continue...", justify='center', style='bold white')
                                input()
                                clear_screen()
                                continue  # Exit the loop after successful input

                        elif assignee_choice == '3':
                            break  # Exit the loop and return to the main menu
                        else:
                            console.print("Error: Invalid choice.", justify='center', style='bold red')
                            logging.info("Error: Invalid choice.")
                            console.print("Press Enter to continue...", justify='center', style='bold white')
                            input()
                            clear_screen()
                            continue  # Restart the loop to get valid input
                else:
                    console.print("Error: You are not allowed to change this section.", justify='center',
                                  style='bold red')
                    logging.info("Error: You are not allowed to change this section.")
                    console.print("Press Enter to continue...", justify='center', style='bold white')
                    input()
                    return

            elif choice == '5':
                clear_screen()
                console.print("Change Deadline: ", justify='center', style='blink bold magenta')
                if username == selected_project["owner"] or username in selected_task["assignees"]:
                    new_deadline = self.get_valid_datetime()
                    if new_deadline is not None:
                        selected_task["deadline"] = new_deadline.strftime("%Y-%m-%d %H:%M")
                        self.save_history(selected_project["project_id"], "Deadline Changed", selected_task["title"],
                                          selected_task["deadline"], username, datetime.now())
                        console.print("Deadline changed successfully.", justify='center', style='bold green')
                        logger.info(f"Deadline of {selected_task} changed to {new_deadline}.")
                        console.print("Press Enter to continue...", justify='center', style='bold white')
                        input()
                        clear_screen()
                    else:
                        console.print("Error: Deadline remains unchanged.", justify='center', style='bold red')
                        logging.info("Error: Deadline remains unchanged.")
                        console.print("Press Enter to continue...", justify='center', style='bold white')
                        input()
                        clear_screen()
                else:
                    console.print("Error: You are not allowed to change this section.", justify='center',
                                  style='bold red')
                    logging.info("Error: You are not allowed to change this section.")
                    console.print("Press Enter to continue...", justify='center', style='bold white')
                    input()
                    clear_screen()
                    return

            elif choice == '6':
                clear_screen()
                console.print("Change Priority: ", justify='center', style='blink bold blue')
                if username == selected_project["owner"] or username in selected_task["assignees"]:
                    console.print("\nSelect Priority:", justify='center', style='bold cyan')
                    console.print("  ", justify='center')
                    console.print("1. CRITICAL", justify='center', style='bold yellow')
                    console.print("  ", justify='center')
                    console.print("2. HIGH", justify='center', style='bold yellow')
                    console.print("  ", justify='center')
                    console.print("3. MEDIUM", justify='center', style='bold yellow')
                    console.print("  ", justify='center')
                    console.print("4. LOW", justify='center', style='bold yellow')
                    console.print("  ", justify='center')
                    console.print("Choose priority (1-4) or press Enter to keep current priority: ", justify='center',
                                  style='white')
                    new_priority_choice = input()

                    if new_priority_choice.isdigit() and 1 <= int(new_priority_choice) <= 4:
                        new_priority = {
                            '1': Priority.CRITICAL,
                            '2': Priority.HIGH,
                            '3': Priority.MEDIUM,
                            '4': Priority.LOW
                        }[new_priority_choice]
                        selected_task["priority"] = new_priority.value
                        self.save_history(selected_project["project_id"], "Priority Changed", selected_task["title"],
                                          new_priority.name, username, datetime.now())
                        console.print("Priority changed successfully.", justify='center', style='bold green')
                        logger.info(f"Priority of task {selected_task} changed to {new_priority}")
                    elif new_priority_choice == "":
                        console.print("Keeping current priority.", justify='center', style='bold red')
                        logging.info("Keeping current priority.")
                    else:
                        console.print("Error: Invalid priority choice. Please choose a number between 1 and 4.",
                                      justify='center', style='bold red')
                        logging.info("Error: Invalid priority choice.")
                        console.print("Press Enter to continue...", justify='center', style='bold white')
                        input()
                        clear_screen()
                        continue



                else:
                    console.print("Error: You are not allowed to change this section.", justify='center',
                                  style='bold red')
                    logging.info("Error: You are not allowed to change this section.")

                console.print("Press Enter to continue...", justify='center', style='bold white')
                input()
                clear_screen()


            elif choice == '7':
                clear_screen()
                console.print("Change Priority: ", justify='center', style='blink bold magenta')
                if username == selected_project["owner"] or username in selected_task["assignees"]:
                    console.print("\nSelect Status:", justify='center', style='bold cyan')
                    console.print("  ", justify='center')
                    console.print("1. BACKLOG", justify='center', style='bold yellow')
                    console.print("  ", justify='center')
                    console.print("2. TODO", justify='center', style='bold yellow')
                    console.print("  ", justify='center')
                    console.print("3. DOING", justify='center', style='bold yellow')
                    console.print("  ", justify='center')
                    console.print("4. DONE", justify='center', style='bold yellow')
                    console.print("  ", justify='center')
                    console.print("5. ARCHIVED", justify='center', style='bold yellow')

                    console.print("\nChoose status (1-5) or press Enter to keep current status: ", justify='center',
                                  style='white')
                    new_status_choice = input()

                    if new_status_choice.isdigit() and 1 <= int(new_status_choice) <= 5:
                        new_status = {
                            '1': Status.BACKLOG,
                            '2': Status.TODO,
                            '3': Status.DOING,
                            '4': Status.DONE,
                            '5': Status.ARCHIVED
                        }[new_status_choice]
                        selected_task["status"] = new_status.value
                        self.save_history(selected_project["project_id"], "Status Changed", selected_task["title"],
                                          new_status.name, username, datetime.now())
                        console.print("Status changed successfully.", justify='center', style='bold green')
                        logger.info(f"Status of task {selected_task} changed to {new_status}")
                    elif new_status_choice == "":
                        console.print("Keeping current status.", justify='center', style='bold red')
                        logging.info("Keeping current status.")
                    else:
                        console.print("Error: Invalid status choice. Please choose a number between 1 and 5.",
                                      justify='center', style='bold red')
                        logging.info("Error: Invalid status choice.")
                        console.print("Press Enter to continue...", justify='center', style='bold white')
                        input()
                        break
                        clear_screen()


                else:
                    console.print("Error: You are not allowed to change this section.", justify='center',
                                  style='bold red')
                    logging.info("Error: You are not allowed to change this section.")

                console.print("Press Enter to continue...", justify='center', style='bold white')
                input()
                clear_screen()

            elif choice == '8':
                clear_screen()
                while True:
                    console.print("Comment Menu:", justify='center', style='blink bold blue')
                    console.print("\n1. Add Comment", justify='center', style='white')
                    console.print("  ", justify='center')
                    console.print("2. Remove Comment", justify='center', style='white')
                    console.print("  ", justify='center')
                    console.print("3. Exit", justify='center', style='white')
                    console.print("  ", justify='center')
                    console.print("Choose an option: ", justify='center', style='white')
                    comment_choice = input()

                    if comment_choice not in ['1', '2', '3']:
                        console.print("Error: Invalid option. Please choose a valid option.", justify='center',
                                      style='bold red')
                        logging.info("Error: Invalid option. Please choose a valid option.")
                        console.print("Press Enter to continue...", justify='center', style='bold white')
                        input()
                        continue

                    if comment_choice == '1':
                        clear_screen()
                        try:
                            console.print("Add Comment: ", justify='center', style='blink bold magenta')
                            console.print("\nEnter your comment: ", justify='center', style='white')
                            comment_text = input()
                            if not comment_text:
                                console.print("Error: Comment cannot be empty.", justify='center', style='bold red')
                                logging.info("Error: Comment cannot be empty.")
                                console.print("Press Enter to continue...", justify='center', style='bold white')
                                input()
                                continue
                            selected_task["comments"].append({"username": username, "comment": comment_text})
                            self.save_history(selected_project["project_id"], "Comment Added", selected_task["title"],
                                              comment_text, username, datetime.now())
                            console.print("Comment added successfully.", justify='center', style='bold green')
                            logger.info(f"{username} added a comment to {selected_task}")
                            console.print("Press Enter to continue...", justify='center', style='bold white')
                            input()
                            clear_screen()
                        except Exception as e:
                            console.print(f"Error adding comment: {e}", justify='center', style='bold red')
                            logging.info(f"Error adding comment: {e}")
                            console.print("Press Enter to continue...", justify='center', style='bold white')
                            input()
                            clear_screen()

                    elif comment_choice == '2':
                        clear_screen()
                        console.print("Remove Comment: ", justify='center', style='blink bold magenta')
                        if not selected_task["comments"]:
                            console.print("Error: No comments to remove.", justify='center', style='bold red')
                            logger.info("Error: No comments to remove.")
                            console.print("Press Enter to continue...", justify='center', style='bold white')
                            input()
                            continue

                        console.print("\nSelect a comment to remove:", justify='center', style='bold cyan')
                        for index, comment in enumerate(selected_task["comments"], 1):
                            console.print(f"{index}. {comment['username']}: {comment['comment']}", justify='center',
                                          style='cyan')
                            console.print("  ", justify='center')
                            time.sleep(0.5)

                        while True:
                            console.print("\nEnter the comment number to remove (or press Enter to cancel): ",
                                          justify='center', style='white')
                            remove_choice = input()
                            if remove_choice == "":
                                break
                            elif re.match("^\d+$", remove_choice):
                                remove_choice = int(remove_choice) - 1
                                if 0 <= remove_choice < len(selected_task["comments"]):
                                    comment_to_remove = selected_task["comments"][remove_choice]
                                    if comment_to_remove["username"] == username or username == selected_project[
                                        "owner"]:
                                        try:
                                            # Remove the comment and save the changes
                                            selected_task["comments"].remove(comment_to_remove)
                                            self.save_history(
                                                selected_project["project_id"],
                                                "Comment Removed",
                                                selected_task["title"],
                                                comment_to_remove["comment"],
                                                username,
                                                datetime.now()
                                            )
                                            console.print("Comment removed successfully.", justify='center',
                                                          style='bold green')
                                            logger.info(f"{comment_to_remove} removed successfully.")
                                            console.print("Press Enter to continue...", justify='center',
                                                          style='bold white')
                                            input()
                                            clear_screen()
                                            break  # Return to the main comment menu
                                        except Exception as e:
                                            console.print(f"Error removing comment: {e}", justify='center',
                                                          style='bold red')
                                            logging.info(f"Error removing comment: {e}")
                                            console.print("Press Enter to continue...", justify='center',
                                                          style='bold white')
                                            input()
                                            clear_screen()
                                            break
                                    else:
                                        console.print("Error: You do not have permission to remove this comment.",
                                                      justify='center', style='bold red')
                                        logging.info("Error: You do not have permission to remove this comment.")
                                        console.print("Press Enter to continue...", justify='center',
                                                      style='bold white')
                                        input()
                                        clear_screen()
                                        break
                                else:
                                    console.print("Error: Invalid comment number.", justify='center', style='bold red')
                                    logging.info("Error: Invalid comment number.")
                                    console.print("Press Enter to continue...", justify='center', style='bold white')
                                    input()
                                    clear_screen()
                                    break
                            else:
                                console.print("Error: Invalid input. Please enter a valid comment number.",
                                              justify='center', style='bold red')
                                logging.info("Error: Invalid input.")
                                console.print("Press Enter to continue...", justify='center', style='bold white')
                                input()
                                clear_screen()

                    elif comment_choice == '3':
                        break

            elif choice == '9':
                clear_screen()
                self.update_task(selected_task['task_id'], selected_task)
                console.print("Task saved and exited.", justify='center', style='bold green')
                logger.info(f"Task {selected_task} saved and exited.")
                return selected_task
            else:
                console.print("Error: Invalid choice. Please try again.", justify='center', style='bold red')
                logging.info("Error: Invalid choice.")
                console.print("Press Enter to continue...", justify='center', style='bold white')
                input()
                clear_screen()

    def print_delete_task(self):
        console = Console(width=50)
        console.print("  ┌┬┐┌─┐┬  ┌─┐┌┬┐┌─┐  ┌┬┐┌─┐┌─┐┬┌─", justify='center', style='blink bold green')
        console.print("   ││├┤ │  ├┤  │ ├┤    │ ├─┤└─┐├┴┐", justify='center', style='blink bold blue')
        console.print("  ─┴┘└─┘┴─┘└─┘ ┴ └─┘   ┴ ┴ ┴└─┘┴ ┴\n", justify='center', style='blink bold green')

    def delete_task(self, username, selected_project):
        console = Console(width=50)
        self.print_delete_task()
        if selected_project['owner'] != username:
            console.print("Error: You do not have permission to delete tasks for this project.", justify='center',
                          style='bold red')
            logging.info("Error: You do not have permission to delete tasks for this project.")
            console.print("Press Enter to continue...", justify='center', style='bold white')
            input()
            clear_screen()
            return

        project_id = selected_project["project_id"]

        # Extract tasks related to the selected project
        project_tasks = [task for task in self.tasks.values() if
                         isinstance(task, dict) and task.get('project_id') == project_id]

        # Filter tasks owned by the user
        user_tasks = [task for task in project_tasks if selected_project.get('owner') == username]

        # Check if the user has any tasks in the project
        if not user_tasks:
            console.print("Error: You don't have any tasks in your project.", justify='center', style='bold red')
            logging.info("Error: You don't have any tasks in your project.")
            console.print("Press Enter to continue...", justify='center', style='bold white')
            input()
            return

        for index, task in enumerate(user_tasks, 1):
            deadline = datetime.fromisoformat(task['deadline']).strftime("%Y-%m-%d %H:%M:%S")
            console.print(f"{index}. {task['title']} - Deadline: {deadline}", justify='center')
            console.print("  ", justify='center')

        # Prompt user to select a task
        console.print("\nEnter the number of the task to delete: ", justify='center', style='yellow')
        selected_task_index = input()
        if not selected_task_index.isdigit() or int(selected_task_index) < 1 or int(selected_task_index) > len(
                user_tasks):
            console.print("Error: Invalid task selection. Please enter a valid task number.", justify='center',
                          style='bold red')
            logging.info("Error: Invalid task selection.")
            console.print("Press Enter to continue...", justify='center', style='bold white')
            input()
            return

        selected_task = user_tasks[int(selected_task_index) - 1]

        confirm = input(f"Are you sure you want to delete task '{selected_task['title']}'? (y/n): ")
        if confirm.lower() != 'y':
            console.print("Error: Task deletion canceled.", justify='center', style='bold red')
            logging.info("Error: Task deletion canceled.")
            console.print("Press Enter to continue...", justify='center', style='bold white')
            input()
            return

        # Remove the task
        del self.tasks[selected_task['task_id']]
        self.save_tasks(self.tasks)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_history(project_id, "Task Deleted", selected_task["title"], selected_task['title'], username,
                          current_time)
        console.print("Task deleted successfully.", justify='center', style='bold green')
        logger.info(f"Task '{selected_task['title']}' deleted successfully.")
        console.print("Press Enter to continue...", justify='center', style='bold white')
        input()

    def print_tasks_menu(self):
        console = Console(width=50)
        console.print("  ╔╦╗┌─┐┌─┐┬┌─┌─┐  ╔╦╗┌─┐┌┐┌┬ ┬", justify='center', style='blink bold black on white underline ')
        console.print("   ║ ├─┤└─┐├┴┐└─┐  ║║║├┤ ││││ │", justify='center', style='blink bold black on white underline ')
        console.print("   ╩ ┴ ┴└─┘┴ ┴└─┘  ╩ ╩└─┘┘└┘└─┘", justify='center', style='blink bold black on white underline ')

    def print_task_details(self):
        console = Console(width=50)
        console.print("  ┌┬┐┌─┐┌─┐┬┌─  ┌┬┐┌─┐┌┬┐┌─┐┬┬  ┌─┐", justify='center', style='blink bold blue')
        console.print("   │ ├─┤└─┐├┴┐   ││├┤  │ ├─┤││  └─┐", justify='center', style='blink bold white')
        console.print("   ┴ ┴ ┴└─┘┴ ┴  ─┴┘└─┘ ┴ ┴ ┴┴┴─┘└─┘", justify='center', style='blink bold blue')

    def print_task_menu(self):
        console = Console(width=50)
        console.print("  ╔╦╗┌─┐┌─┐┬┌─  ┌┬┐┌─┐┌┐┌┬ ┬", justify='center', style='blink bold green')
        console.print("   ║ ├─┤└─┐├┴┐  │││├┤ ││││ │", justify='center', style='blink bold magenta')
        console.print("   ╩ ┴ ┴└─┘┴ ┴  ┴ ┴└─┘┘└┘└─┘", justify='center', style='blink bold green')

    def print_tasks_status(self):
        console = Console(width=50)
        console.print("  ╔╦╗┌─┐┌─┐┬┌─┌─┐  ╔═╗┌┬┐┌─┐┌┬┐┬ ┬┌─┐", justify='center', style='blink bold cyan')
        console.print("   ║ ├─┤└─┐├┴┐└─┐  ╚═╗ │ ├─┤ │ │ │└─┐", justify='center', style='blink bold yellow')
        console.print("   ╩ ┴ ┴└─┘┴ ┴└─┘  ╚═╝ ┴ ┴ ┴ ┴ └─┘└─┘", justify='center', style='blink bold cyan')

    def print_task_history(self):
        console = Console(width=50)
        console.print("  ┌┬┐┌─┐┌─┐┬┌─  ┬ ┬┬┌─┐┌┬┐┌─┐┬─┐┬ ┬", justify='center', style='blink bold magenta')
        console.print("   │ ├─┤└─┐├┴┐  ├─┤│└─┐ │ │ │├┬┘└┬┘", justify='center', style='blink bold yellow')
        console.print("   ┴ ┴ ┴└─┘┴ ┴  ┴ ┴┴└─┘ ┴ └─┘┴└─ ┴ ", justify='center', style='blink bold magenta')

    def view_task_history(self, selected_task):
        console = Console(width=80)
        self.print_task_history()
        try:
            with open(self.history_file, "r") as file:
                history = json.load(file)
                selected_task_history = [change for change in history if
                                         change["project_id"] == selected_task["project_id"]]
                for change in selected_task_history:
                    console.print(f"\nAction: {change['action']}")
                    console.print(f"Field Name: {change['field_name']}", style='blue')
                    console.print(f"New Value: {change['new_value']}", style='magenta')
                    console.print(f"Changer: {change['changer']}", style='yellow')

                    timestamp = change.get('timestamp')
                    if timestamp:
                        formatted_time = datetime.fromisoformat(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        formatted_time = 'N/A'

                    console.print(f"Timestamp: {formatted_time}", style='red')
                    print()
                    print('-' * 40)
                    print()
        except FileNotFoundError:
            console.print("Erorr: No history available for this task.", style='bold red')
            logging.info(f"Erorr: No history available task {selected_task}.")

    def view_tasks(self, selected_project, username):
        console = Console(width=50)
        # Load tasks from tasks.json
        tasks = self.load_tasks()

        if not isinstance(tasks, dict):
            print("Error: Loaded tasks are not in the expected format.")
            logging.info("Error: Loaded tasks are not in the expected format.")
            return

        # Filter tasks based on project_id
        project_tasks = [task for task in tasks.values() if
                         isinstance(task, dict) and task.get("project_id") == selected_project.get("project_id")]

        if not project_tasks:
            console.print("Error: No tasks in this project.", justify='center', style='bold red')
            logging.info("Error: No tasks in this project.")
            console.print("Press Enter to continue...", justify='center', style='bold white')
            input()
            return

        # Create a table to display the tasks
        table_data = {"BACKLOG": [], "TODO": [], "DOING": [], "DONE": [], "ARCHIVED": []}
        for task in project_tasks:
            status = task["status"]
            table_data[status].append(task["label"])

        # Find the maximum number of tasks in any status to ensure alignment
        max_length = max(len(labels) for labels in table_data.values())

        # Normalize the lengths of all status lists by adding empty strings
        for status in table_data:
            table_data[status].extend([""] * (max_length - len(table_data[status])))

        self.print_tasks_status()
        table = Table(box=SIMPLE)

        # Adding columns for each status
        for status in table_data.keys():
            table.add_column(status, justify='center')

        # Adding rows for each label and their corresponding task status with unique numbers
        unique_number = 1
        label_to_number = {}
        for row_idx in range(max_length):
            row = []
            for status in table_data.keys():
                label = table_data[status][row_idx]
                if label:
                    if label not in label_to_number:
                        label_to_number[label] = unique_number
                        unique_number += 1
                    row.append(f"{label_to_number[label]}. {label}")
                else:
                    row.append("")
            table.add_row(*row)

        console.print(table)

        while True:
            try:
                console.print("Enter the number of the task you want to view or edit: ", justify='center',
                              style='bold white')
                task_choice = int(input())
                if task_choice in label_to_number.values():
                    break
                else:
                    console.print("Error: Invalid number. Please enter a valid task number.", justify='center',
                                  style='bold red')
                    logging.info("Error: Invalid number.")
            except ValueError:
                console.print("Error: Invalid input. Please enter a number.", justify='center', style='bold red')
                logging.info("Error: Invalid input.")

        # Get the selected task based on the user's choice
        selected_label = next(label for label, number in label_to_number.items() if number == task_choice)
        selected_task = next(task for task in project_tasks if task["label"] == selected_label)

        # Display menu for task options
        while True:
            clear_screen()
            console = Console(width=50)
            self.print_task_menu()
            time.sleep(0.7)
            console.print("\n1. View Task Details", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("2. Edit Task", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("3. View Task History", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("4. Exit", justify='center')
            console.print("  ", justify='center')
            time.sleep(0.7)
            console.print("Choose an option: ", justify='center')
            menu_choice = input()

            if menu_choice == '1':
                clear_screen()

                try:
                    # Display task details
                    self.print_task_details()
                    table = Table(show_header=True, header_style="bold white")
                    table.add_column("Field", justify="center", style="cyan")
                    table.add_column("Value", justify="center")

                    table.add_row("task_id", selected_task['task_id'], style='cyan')
                    table.add_row()
                    table.add_row("Label", selected_task['label'], style='white')
                    table.add_row()
                    table.add_row("Title", selected_task.get('title', 'N/A'), style='cyan')
                    table.add_row()
                    table.add_row("Description", selected_task.get('description', 'N/A'), style='white')
                    table.add_row()
                    table.add_row("Assignees", ', '.join(selected_task['assignees']), style='cyan')
                    table.add_row()
                    deadline_formatted = datetime.fromisoformat(selected_task.get('deadline')).strftime(
                        "%Y-%m-%d %H:%M") if selected_task.get('deadline') else 'N/A'
                    table.add_row("Deadline", deadline_formatted, style='white')
                    table.add_row()
                    table.add_row("Priority", selected_task.get('priority', 'N/A'), style='cyan')
                    table.add_row()
                    table.add_row("Status", selected_task.get('status', 'N/A'), style='white')
                    table.add_row()
                    table.add_row("Comments", "[italic]See below[/italic]", style='cyan')
                    table.add_row()
                    for comment in selected_task.get('comments', []):
                        table.add_row("", f"{comment['username']}: {comment['comment']}")

                    console.print(table)
                    console.print("Press Enter to continue...", justify='center', style='bold white')
                    input()
                except KeyError as e:
                    console.print(f"Error: Missing key {e}", justify='center', style='bold red')
                    logging.info(f"Error: Missing key {e}")
                    input("Press Enter to continue...")

            elif menu_choice == '2':
                selected_task = self.edit_task(username, selected_project,
                                               selected_task)  # Update selected_task with the returned value
            elif menu_choice == '3':
                clear_screen()
                self.view_task_history(selected_task)
                console.print("Press Enter to continue...", justify='center', style='bold white')
                input()
            elif menu_choice == '4':
                break
            else:
                console.print("Error: Invalid choice. Please try again.", justify='center', style='bold red')
                console.print("Press Enter to continue...", justify='center', style='bold white')
                input()
                logging.info("Error: Invalid choice.")

    def tasks_menu(self, username, selected_project):
        console = Console(width=50)
        project_manager = ProjectManager()
        while True:
            clear_screen()
            self.print_tasks_menu()
            print()
            console.print("[black]1. [/black]Create Task", justify='center', style='bold magenta on white')
            console.print("  ", justify='center')
            time.sleep(1)
            console.print("[black]2. [/black]View Task", justify='center', style='bold magenta on white')
            console.print("  ", justify='center')
            time.sleep(1)
            console.print("[black]3. [/black]Delete Task", justify='center', style='bold magenta on white')
            console.print("  ", justify='center')
            time.sleep(1)
            console.print("[black]4. [/black]Exit", justify='center', style='bold magenta on white')
            console.print("  ", justify='center')
            time.sleep(1)
            console.print("Choose an option: ", justify='center', style='bold white on black')
            choice = input()
            clear_screen()

            if choice == '1':
                self.create_task(username, selected_project)
            elif choice == '2':
                self.view_tasks(selected_project, username)
            elif choice == '3':
                self.delete_task(username, selected_project)
            elif choice == '4':
                break
            else:
                console.print("Error: Invalid choice. Please try again.", justify='center', style='bold red')
                logging.info("Error: Invalid choice.")
                console.print("Press Enter to continue...", justify='center', style='bold white')
                input()
                clear_screen()
                continue


def main():
    user_manager = UserManager()

    def update_screen(end_time, loop, screen):
        screen.draw_next_frame()
        if loop.time() < end_time:
            loop.call_later(0.05, update_screen, end_time, loop, screen)
        else:
            loop.stop()

    # Define the scene that you'd like to play.
    screen = Screen.open()
    effects = [
        Cycle(
            screen,
            FigletText("Trellomize", font='big'),
            screen.height // 2 - 8),
        Stars(screen, (screen.width + screen.height) // 2)
    ]
    screen.set_scenes([Scene(effects, 500)])

    # Schedule the first call to display_date()
    loop = asyncio.new_event_loop()
    end_time = loop.time() + 5.0
    loop.call_soon(update_screen, end_time, loop, screen)

    # Blocking call interrupted by loop.stop()
    loop.run_forever()
    loop.close()
    screen.close()
    user_manager.menu()


if __name__ == "__main__":
    main()
