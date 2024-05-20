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


logging.basicConfig(filename='Account/logfile.log',level=logging.INFO)
logger = logging.getLogger()

fileHandler=logging.FileHandler('logfile.log')
logger.addHandler(fileHandler)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


users_file = "Account/account.json"

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
                         proj["owner"] == username or (proj.get("members") and username in proj["members"])]
        return user_projects
    
    def display_project_members(self, project):
        members = project.get("members", [])
        if members:
            print("Project Members:")
            for index, member in enumerate(members, 1):
                print(f"{index}. {member}")
        else:
            print("Erorr: No members found for this project.")
            logger.info(f"Erorr: No members found project {project}.")
    
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

    def create_account(self):
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

        while password!= confirm_password:
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
                self.create_account()
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
                self.create_account()
            elif choice == '2':
                self.login()
            elif choice == '3':
                print("[blue]Good luck[/blue] ")
                exit()
            else:
                print("Error: Invalid choice. Please enter 1, 2, or 3.")
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
                return json.load(file)
        except FileNotFoundError:
            return {}

    def check_project_existence(self, project_id):
        projects = self.load_projects()
        return project_id in projects

    def create_project(self, project_id, title, owner):
        projects = self.load_projects()

        # Check if the project_id already exists
        if project_id in projects:
            print("[bold red]Erorr: Project ID already exists! Please choose a different one.[/bold red]")
            logging.info(f"Erorr: Project ID {project_id} already exists!")
            input("Press Enter to continue...")
            clear_screen()
            return None

        # Check if the project with the same title already exists for the owner
        for proj in projects.values():
            if proj["title"] == title and proj["owner"] == owner:
                print("Erorr: [bold red]You already have a project with the same title! Please choose a different title.[/bold red]")
                logging.error(f"You already have a project with the same title: {title} owned by {owner}!")
                input("Press Enter to continue...")
                clear_screen()
                return None

        # If all checks pass, create the project
        print("Project created successfully!")
        logger.info(f"{owner} created project {title} successfully.")
        input("Press Enter to continue...")
        clear_screen()
        projects[project_id] = {"title": title, "project_id": project_id, "owner": owner}
        self.save_projects(projects)
        return Project(project_id, title, owner)

    def delete_project(self, owner):
        projects = self.load_projects()
        owned_projects = [proj for proj in projects.values() if proj["owner"] == owner]
        if not owned_projects:
            print("[bold red]Erorr: You don't own any projects to delete![/bold red]")
            logging.info("Erorr: You don't own any projects to delete!You don't own any projects to delete!")
            return False
    
        while True:
            print("Your projects:")
            for index, proj in enumerate(owned_projects, 1):
                print(f"{index}. {proj['title']} (ID: {proj['project_id']})")
        
            choice = input("Enter the number of the project you want to delete: ")
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(owned_projects):
                print("[bold red]Erorr: Invalid choice! Please enter a valid number.[/bold red]")
                logging.info("Erorr: Invalid choice! Please enter a valid number.")
                input("Press Enter to continue...")
                clear_screen()
                continue

            project_to_delete = owned_projects[int(choice) - 1]
            confirm = input(f"Are you sure you want to delete '{project_to_delete['title']}' project? (y/n): ")
            if confirm.lower() == 'y':
                del projects[project_to_delete['project_id']]
                self.save_projects(projects)
                logger.info(f"{owner} deleted project {project_to_delete['title']} successfully.")
                print("Project deleted successfully!")
                input("Press Enter to continue...")
                clear_screen()
                return True
            else:
                print("Deletion canceled.")
                logging.info(f"Erorr: project {project_to_delete['title']} Deletion canceled.")
                input("Press Enter to continue...")
                clear_screen()
                return False


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
                        print(f"Member '{member}' added to project '{project['title']}' successfully.")
                        logger.info(f"Member '{member}' added to project '{project['title']}' successfully.")
                        self.save_projects(projects)
                        input("Press Enter to continue...")
                        clear_screen()
                    else:
                        print(f"Erorr: Member '{member}' is already a member of project '{project['title']}'.")
                        logging.info(f"Erorr: Member '{member}' is already a member of project '{project['title']}'.")
                        input("Press Enter to continue...")
                        clear_screen()
                else:
                    print("[bold red]Erorr: User not found![/bold red]")
                    logging(f"Erorr: User '{member}' not found!")
                    input("Press Enter to continue...")
                    clear_screen()
            else:
                print("[bold red]Erorr: You are not the owner of this project![/bold red]")
                logging.info("Erorr: You are not the owner of this project!")
                input("Press Enter to continue...")
                clear_screen()
        else:
            print(f"Erorr: Project with ID '{project_id}' not found.")
            logging.info(f"Erorr: Project with ID '{project_id}' not found.")
            input("Press Enter to continue...")
            clear_screen()

    def remove_member_from_project(self, project_id, username):
        projects = self.load_projects()
        if project_id in projects:
            project = projects[project_id]
            if project["owner"] == username:
                if "members" in project:
                    print("Members of project:")
                    for index, member in enumerate(project["members"], 1):
                        print(f"{index}. {member}")
                    while True:
                        choice = input("Enter the number of the member you want to remove: ")
                        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(project["members"]):
                            print("[bold red]Erorr: Invalid choice! Please enter a valid number.[/bold red]")
                            logging.info("Erorr: Invalid choice! Please enter a valid number.")
                            input("Press Enter to continue...")
                            clear_screen()
                            print("Members of project:")
                            for index, member in enumerate(project["members"], 1):
                                print(f"{index}. {member}")
                            continue
                        member_to_remove = project["members"][int(choice) - 1]
                        confirm = input(f"Are you sure you want to remove '{member_to_remove}' from project '{project['title']}'? (y/n): ")
                        if confirm.lower() == 'y':
                            project["members"].remove(member_to_remove)
                            self.save_projects(projects)
                            logger.info(f"Member '{member_to_remove}' removed from project '{project['title']}' successfully.")
                            print("Member removed successfully!")
                            input("Press Enter to continue...")
                            clear_screen()
                            return True
                        else:
                            print("Erorr: Remove canceled.")
                            logging.info("Erorr: Remove canceled.")
                            clear_screen()
                            return False
                else:
                    print("Erorr: This project has no members.")
                    logging.info("Erorr: This project has no members.")
                    clear_screen()
            else:
                print("[bold red]Erorr: You are not the owner of this project![/bold red]")
                logging.info(f"Erorr: You are not the owner of project '{project['title']}'!")
                input("Press Enter to continue...")
                clear_screen()
        else:
            print(f"Erorr: Project with ID '{project_id}' not found.")
            logging.info(f"Erorr: Project with ID '{project_id}' not found.")
            input("Press Enter to continue...")
            clear_screen()

    def view_projects(self, username):
        projects = self.load_projects()

        # Create a table with four columns: Project Title, Owner, Role, and Members
        table = Table(title="Your Projects", show_header=True, header_style="bold magenta")
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
        projects = self.load_projects()
        owner_projects = [proj for proj in projects.values() if proj["owner"] == username]

        if not owner_projects:
            print("Error: You are not associated with any projects.")
            logging.info("Error: You are not associated with any projects.")
            input("Press Enter to continue...")
            clear_screen()
            return None

        print("Select a Project:")
        for index, project in enumerate(owner_projects, 1):
            print(f"{index}. {project['title']}")

        while True:
            project_choice = input("Enter the project number: ")
            if re.match("^\d+$", project_choice):
                project_choice = int(project_choice) - 1
                if 0 <= project_choice < len(owner_projects):
                    break
                else:
                    print("Error: Invalid project choice")
                    logging.info("Error: Invalid project choice")
                    input("Press Enter to continue...")
                    clear_screen()
                    for index, project in enumerate(owner_projects, 1):
                        print(f"{index}. {project['title']}")
            else:
                print("Error: Please enter a valid project number.")
                logging.info("Error: Invalid project number")
                input("Press Enter to continue...")
                clear_screen()
                for index, project in enumerate(owner_projects, 1):
                    print(f"{index}. {project['title']}")

        selected_project = owner_projects[project_choice]
        return selected_project


    def show_project(self, username):
        projects = self.load_projects()
        person_projects = [proj for proj in projects.values() if
                       proj["owner"] == username or (proj.get("members") and username in proj["members"])]

        if not person_projects:
            print("Error: You are not associated with any projects.")
            logging.info("Error: You are not associated with any projects.")
            input("Press Enter to continue...")
            clear_screen()
            return None

        print("Select a Project:")
        for index, project in enumerate(person_projects, 1):
            print(f"{index}. {project['title']}")

        while True:
            project_choice = input("Enter the project number: ")
            if re.match("^\d+$", project_choice):
                project_choice = int(project_choice) - 1
                if 0 <= project_choice < len(person_projects):
                    break
                else:
                    print("Error: Invalid project choice")
                    logging.info("Error: Invalid project choice")
                    input("Press Enter to continue...")
                    clear_screen()
                    print("Select a Project:")
                    for index, project in enumerate(person_projects, 1):
                        print(f"{index}. {project['title']}")
            else:
                print("Please enter a valid project number.")
                logging.info("Please enter a valid project number.")
                input("Press Enter to continue...")
                clear_screen()
                for index, project in enumerate(person_projects, 1):
                    print(f"{index}. {project['title']}")

        selected_project = person_projects[project_choice]
        return selected_project

    def edit_project_menu(self, username, selected_project):
        while True:
            clear_screen()
            print("1. Add Member to Project")
            print("2. Remove Member from Project")
            print("3. Manage Tasks")
            print("4. Exit")
            choice = input("Choose an option: ")
            if choice == '1':
                member = input("Enter the username of the member you want to add: ")
                self.add_member_to_project(selected_project['project_id'], member, username)
            elif choice == '2':
                self.remove_member_from_project(selected_project['project_id'], username)
            elif choice == '3':
                self.tasks_menu(username, selected_project)
            elif choice == '4':
                break
                clear_screen()
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def account(self, username):

        while True:
            print("1. Create Project")
            print("2. Edit Project")
            print("3. Delete Project")
            print("4. View Projects")
            print("5. Logout")
            choice = input("Choose an option: ")
            clear_screen()
            if choice == '1':
                project_id = input("Enter project ID: ")
                title = input("Enter project title: ")
                self.create_project(project_id, title, username)

            elif choice == '2':
                selected_project = self.show_project(username)
                if selected_project:
                    self.edit_project_menu(username, selected_project)

            elif choice == '3':
                self.delete_project(username)


            elif choice == '4':
                self.view_projects(username)
                input("Press Enter to continue...")
                clear_screen()

            elif choice == '5':
                break
            else:
                print("Error: Invalid choice. Please try again.")
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
            print("Task updated successfully.")
            logger.info(f"Task {task_id} updated successfully.")
        else:
            print("Error: Task not found.")
            logger.info(f"Error: Task {task_id} not found.")

    def view_task_history(self, selected_task):
        try:
            with open(self.history_file, "r") as file:
                history = json.load(file)
                selected_task_history = [change for change in history if change["project_id"] == selected_task["project_id"]]
                for change in selected_task_history:
                    print(f"Action: {change['action']}")
                    print(f"Field Name: {change['field_name']}")
                    print(f"New Value: {change['new_value']}")
                    print(f"Changer: {change['changer']}")
                
                
                    timestamp = change.get('timestamp')
                    if timestamp:
                        formatted_time = datetime.fromisoformat(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        formatted_time = 'N/A'
                
                    print(f"Timestamp: {formatted_time}")
                    print()
        except FileNotFoundError:
            print("Erorr: No history available for this task.")
            logging.info(f"Erorr: No history available task {selected_task}.")


def main():
    user_manager = UserManager()
    user_manager.menu()

if __name__ == "__main__":
    main()
