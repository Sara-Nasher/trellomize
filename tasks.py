from rich.console import Console, OverflowMethod
from rich.table import Table
from rich import print
import json
from rich import print
from typing import List
import os
import datetime
from enum import Enum
import uuid
import re
import hashlib
from rich.box import SIMPLE


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

    def create_task(self, username, project_id, label, title, description, deadline, assignees, priority=Priority.LOW,
                    status=Status.BACKLOG, comments=None):
        task_id = str(uuid.uuid4())
        task = {
            "task_id": task_id,
            "project_id": project_id,
            "label": label,
            "title": title,
            "description": description,
            "deadline": deadline.isoformat(),
            "assignees": assignees,
            "priority": priority.value,
            "status": status.value,
            "comments": [{"username": username, "comment": comments}] if comments else [],
            "created_at": datetime.datetime.now().isoformat()
        }
        self.tasks[task_id] = task
        self.save_tasks(self.tasks)
        self.save_history(project_id, "Task Created", label, title, username, datetime.datetime.now())
        return task

    def update_task(self, task_id, updated_task):
        if task_id in self.tasks:
            self.tasks[task_id].update(updated_task)
            self.save_tasks(self.tasks)
            print("Task updated successfully.")
        else:
            print("Error: Task not found.")

class User:
    def __init__(self, email, username, password, active=True):
        self.email = email
        self.username = username
        self.password = password
        self.active = active


class Project:
    def __init__(self, project_id, title, owner):
        self.project_id = project_id
        self.title = title
        self.owner = owner


class UserManager:
    def __init__(self, users_file="Account/account.json"):
        self.users_file = users_file

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
            print("No members found for this project.")


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
            print("[bold red]Project ID already exists! Please choose a different one.[/bold red]")
            input("Press Enter to continue...")
            clear_screen()
            return None

        # Check if the project with the same title already exists for the owner
        for proj in projects.values():
            if proj["title"] == title and proj["owner"] == owner:
                print(
                    "[bold red]You already have a project with the same title! Please choose a different title.[/bold red]")
                input("Press Enter to continue...")
                clear_screen()
                return None

        # If all checks pass, create the project
        print("Project created successfully!")
        input("Press Enter to continue...")
        clear_screen()
        projects[project_id] = {"title": title, "project_id": project_id, "owner": owner}
        self.save_projects(projects)
        return Project(project_id, title, owner)

    def delete_project(self, owner):
        projects = self.load_projects()
        owned_projects = [proj for proj in projects.values() if proj["owner"] == owner]
        if not owned_projects:
            print("[bold red]You don't own any projects to delete![/bold red]")
            return False
    
        while True:
            print("Your projects:")
            for index, proj in enumerate(owned_projects, 1):
                print(f"{index}. {proj['title']} (ID: {proj['project_id']})")
        
            choice = input("Enter the number of the project you want to delete: ")
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(owned_projects):
                print("[bold red]Invalid choice! Please enter a valid number.[/bold red]")
                input("Press Enter to continue...")
                clear_screen()
                continue

            project_to_delete = owned_projects[int(choice) - 1]
            confirm = input(f"Are you sure you want to delete '{project_to_delete['title']}' project? (y/n): ")
            if confirm.lower() == 'y':
                del projects[project_to_delete['project_id']]
                self.save_projects(projects)
                print("Project deleted successfully!")
                return True
            else:
                print("Deletion canceled.")
                return False


    def add_member_to_project(self, project_id, member, username):
        projects = self.load_projects()
        users = UserManager().load_users()

        if project_id in projects:
            project = projects[project_id]
            if project["owner"] == username:
                if member in users:
                    project["members"] = project.get("members", [])
                    if member not in project["members"]:
                        project["members"].append(member)
                        print(f"Member '{member}' added to project '{project['title']}' successfully.")
                        self.save_projects(projects)
                    else:
                        print(f"Member '{member}' is already a member of project '{project['title']}'.")
                        input("Press Enter to continue...")
                        clear_screen()
                else:
                    print("[bold red]User not found![/bold red]")
                    input("Press Enter to continue...")
                    clear_screen()
            else:
                print("[bold red]You are not the owner of this project![/bold red]")
                input("Press Enter to continue...")
                clear_screen()
        else:
            print(f"Project with ID '{project_id}' not found.")
            input("Press Enter to continue...")
            clear_screen()
        input("Press Enter to continue...")
        clear_screen()

    def remove_member_from_project(self, project_id, member, username):
        projects = self.load_projects()
        if project_id in projects:
            project = projects[project_id]
            if project["owner"] == username:
                if "members" in project and member in project["members"]:
                    project["members"].remove(member)
                    print(f"Member '{member}' removed from project '{project['title']}' successfully.")
                    self.save_projects(projects)
                    input("Press Enter to continue...")
                    clear_screen()
                else:
                    print(f"Member '{member}' is not a member of project '{project['title']}'")
                    input("Press Enter to continue...")
                    clear_screen()
            else:
                print("[bold red]You are not the owner of this project![/bold red]")
                input("Press Enter to continue...")
                clear_screen()
        else:
            print(f"Project with ID '{project_id}' not found.")
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



def create_account():
    user_manager = UserManager()
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

    while password!= confirm_password:
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

    # Hash the password using SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

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

    users[username] = {"email": email, "username": username, "password": hashed_password, "active": True}
    save_users(users)
    print("[bold green]\nAccount created successfully![/bold green]")
    input("Press Enter to continue...")
    user_manager.create_user(email, username, hashed_password)
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
        console.print("********", overflow=overflow_p, justify='center', style="blink bold cyan") 
        print("\n")

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

    # Hash the input password using SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    if any(user["username"] == username and user["password"] == hashed_password for user in users.values()):
        print("[bold green]\nLogin successful![/bold green]")
        input("Press Enter to continue...")
        clear_screen()
        print_account(users[username]['email'], username, users[username]['password'], console)
        input("Press Enter to continue...")
        clear_screen()
        account(username)
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

def select_project(username):
    projects = ProjectManager().load_projects()
    owner_projects = [proj for proj in projects.values() if proj["owner"] == username]

    if not owner_projects:
        print("You are not associated with any projects.")
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
                print("Invalid project choice")
                input("Press Enter to continue...")
                clear_screen()
                for index, project in enumerate(owner_projects, 1):
                    print(f"{index}. {project['title']}")
        else:
            print("Please enter a valid project number.")
            input("Press Enter to continue...")
            clear_screen()
            for index, project in enumerate(owner_projects, 1):
                print(f"{index}. {project['title']}")

    selected_project = owner_projects[project_choice]
    return selected_project


def show_project(username):
    projects = ProjectManager().load_projects()
    person_projects = [proj for proj in projects.values() if
                       proj["owner"] == username or (proj.get("members") and username in proj["members"])]

    if not person_projects:
        print("You are not associated with any projects.")
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
                print("Invalid project choice")
                input("Press Enter to continue...")
                clear_screen()
                for index, project in enumerate(person_projects, 1):
                    print(f"{index}. {project['title']}")
        else:
            print("Please enter a valid project number.")
            input("Press Enter to continue...")
            clear_screen()
            for index, project in enumerate(person_projects, 1):
                print(f"{index}. {project['title']}")

    selected_project = person_projects[project_choice]
    return selected_project


def get_valid_datetime(prompt):
    while True:
        datetime_input = input(prompt)
        if not datetime_input:
            return None  # Return None if the input is empty
        try:
            datetime_obj = datetime.datetime.strptime(datetime_input, "%Y-%m-%d %H:%M")
            if datetime_obj < datetime.datetime.now():
                print("Invalid date and time. It should be in the future.")
                continue
            return datetime_obj
        except ValueError:
            print("Invalid date format. Please enter the date and time in the format YYYY-MM-DD HH:MM.")


def create_task(username, selected_project):
    if selected_project['owner']!= username:
        print("You do not have permission to create tasks for this project.")
        input("Press Enter to continue...")
        clear_screen()
        return

    task_manager = TaskManager()
    project_id = selected_project["project_id"]
    while True:
        label = input("Enter the task label: ")
        if label.strip():
            break  # Exit loop if label is provided
        else:
            print("Task label cannot be empty. Please enter a label.")
            input("Press Enter to continue...")
            clear_screen()

    title = input("Enter the task title: ")
    description = input("Enter the task description: ")
    

    start_datetime = datetime.datetime.now()
    end_datetime = get_valid_datetime("Enter the task deadline (YYYY-MM-DD HH:MM): ")
    if not end_datetime:
        end_datetime = start_datetime + datetime.timedelta(days=1)
    elif end_datetime < start_datetime:
        print("Invalid deadline. It should be after the start time.")
        return
    UserManager().display_project_members(selected_project)
    member_choices = input("Enter the member numbers (comma-separated): ")
    selected_members = []
    if member_choices:
        for choice in member_choices.split(','):
            if choice.isdigit() and 0 < int(choice) <= len(members):
                selected_members.append(members[int(choice) - 1])
            else:
                print("Invalid member choice. Task cannot be assigned without any members.")
                continue
    else:
        print("No members selected for the task. You can add members later.")
        proceed = input("Do you want to proceed without assigning any members? (y/n): ")
        if proceed.lower()!= 'y':
            print("Task creation cancelled.")
            return

    print("Select Priority:")
    print("1. CRITICAL")
    print("2. HIGH")
    print("3. MEDIUM")
    print("4. LOW")

    selected_priority = None
    while not selected_priority:
        priority = input("Choose priority (1-4): ")
        if priority.isdigit() and 1 <= int(priority) <= 4:
            selected_priority = {
                '1': Priority.CRITICAL,
                '2': Priority.HIGH,
                '3': Priority.MEDIUM,
                '4': Priority.LOW
            }.get(priority, Priority.LOW)
        elif not priority:
            selected_priority = Priority.CRITICAL
        else:
            print("Invalid input. Please choose a priority between 1 and 4.")
    if selected_priority is None:
        selected_priority = Priority.CRITICAL

    print(f"Selected priority: {selected_priority}")


    print("Select Status:")
    print("1. BACKLOG")
    print("2. TODO")
    print("3. DOING")
    print("4. DONE")
    print("5. ARCHIVED")

    selected_status = None
    while not selected_status:
        status = input("Choose Status (1-5): ")
        if status.isdigit() and 1 <= int(status) <= 5:
            selected_status = {
                '1': Status.BACKLOG,
                '2': Status.TODO,
                '3': Status.DOING,
                '4': Status.DONE, 
                '5': Status.ARCHIVED
            }.get(status, Status.BACKLOG)
        elif not status:
            selected_status = Status.BACKLOG
        else:
            print("Invalid input. Please choose a status between 1 and 5.")
    if selected_status is None:
        selected_status = Status.BACKLOG

    print(f"Selected status: {selected_status}")

    comments = input("Enter comments for the task: ").strip()

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
        "created_at": datetime.datetime.now().isoformat()
    }

    tasks = task_manager.load_tasks()
    tasks[new_task["task_id"]] = new_task
    task_manager.save_tasks(tasks)
    task_manager.save_history(project_id, "Task Created", label, title, username, datetime.datetime.now())

    print("Task created successfully!")
    input("Press Enter to continue...")
    clear_screen()


def edit_task(username, selected_project, selected_task, task_manager):
    task_manager = TaskManager()
    task_manager.load_tasks()
    while True:
        clear_screen()
        print("Edit Task Menu:")
        print("1. Change label")
        print("2. Change Title")
        print("3. Change Description")
        print("4. Change Assignees")
        print("5. Change Deadline")
        print("6. Change Priority")
        print("7. Change Status")
        print("8. Comments")
        print("9. Exit")

        choice = input("Choose an option: ")
        if choice == '1':
            if username == selected_project["owner"] or username in selected_task["assignees"]:
                new_label = input("Enter new label (or leave blank): ")
                if new_label:
                    selected_task["label"] = new_label
                    task_manager.save_history(selected_project["project_id"], "Task label Changed", selected_task["title"],
                                              new_label, username, datetime.datetime.now())

                    print("label changed successfully.")
                    input("Press Enter to continue...")
                    clear_screen()
                else:
                    print("label remains unchanged.")
                    input("Press Enter to continue...")
                    clear_screen()
            else:
                print("You are not allowed to change this section.")
                input("Press Enter to continue...")
                clear_screen()
                return
            
        elif choice == '2':
            if username == selected_project["owner"] or username in selected_task["assignees"]:
                new_title = input("Enter new title (leave blank to remove current title): ")
                if new_title:
                    selected_task["title"] = new_title
                    task_manager.save_history(selected_project["project_id"], "Task Title Changed", selected_task["title"],
                                              new_title, username, datetime.datetime.now())
                    print("Title changed successfully.")
                    input("Press Enter to continue...")
                    clear_screen()
                else:
                    selected_task["title"] = ""
                    task_manager.save_history(selected_project["project_id"], "Task Title Removed", selected_task["title"],
                                              selected_task["title"], username, datetime.datetime.now())
                    print("Title removed successfully.")
                    input("Press Enter to continue...")
            else:
                print("You are not allowed to change this section.")
                input("Press Enter to continue...")
                return

        elif choice == '3':
            if username == selected_project["owner"] or username in selected_task["assignees"]:
                new_description = input("Enter new description (leave blank to remove current description): ")
                if new_description:
                    selected_task["description"] = new_description
                    task_manager.save_history(selected_project["project_id"], "Task Description Changed", selected_task["title"],
                                              new_description, username, datetime.datetime.now())
                    print("Description changed successfully.")
                    input("Press Enter to continue...")
                    clear_screen()
                else:
                    selected_task["description"] = ""
                    task_manager.save_history(selected_project["project_id"], "Task Description Removed", selected_task["title"],
                                              selected_task["description"], username, datetime.datetime.now())
                    print("Description removed successfully.")
                    input("Press Enter to continue...")
                    clear_screen()
            else:
                print("You are not allowed to change this section.")
                input("Press Enter to continue...")
                return

        elif choice == '4':
            if username == selected_project["owner"]:
                while True:  # Loop until valid choice is made
                    print("1. Add Assignees")
                    print("2. Remove Assignees")
                    print("3. Exit")

                    assignee_choice = input("Choose an option: ")

                    if assignee_choice == '1':
                        # Add Assignees
                        available_assignees = [member for member in selected_project["members"] if member not in selected_task["assignees"]]
                        if not available_assignees:
                            print("There are no available assignees to add.")
                            input("Press Enter to continue...")
                            continue
            
                        print("Available Assignees:")
                        for index, assignee in enumerate(available_assignees, 1):
                            print(f"{index}. {assignee}")
            
                        selected_assignees = input("Enter the numbers of the assignees to add (comma-separated): ").split(',')
                        selected_assignees = [int(x.strip()) - 1 for x in selected_assignees if re.match("^\d+$", x.strip())]
            
                        for index in selected_assignees:
                            if 0 <= index < len(available_assignees):
                                selected_task["assignees"].append(available_assignees[index])
                            else:
                                print("Invalid assignee choice.")
                                continue  # Restart the loop to get input again
                        else:
                            task_manager.save_history(selected_project["project_id"], "Assignees Added", selected_task["title"],
                                                        ', '.join(selected_task["assignees"]), username, datetime.datetime.now())
                            print("Assignees added successfully.")
                            input("Press Enter to continue...")
                            clear_screen()
                            break  # Exit the loop after successful input
                
                    elif assignee_choice == '2':
                        # Remove Assignees
                        if not selected_task["assignees"]:
                            print("There are no assignees to remove.")
                            input("Press Enter to continue...")
                            continue
            
                        print("Current Assignees:")
                        for index, assignee in enumerate(selected_task["assignees"], 1):
                            print(f"{index}. {assignee}")
            
                        selected_assignees = input("Enter the numbers of the assignees to remove (comma-separated): ").split(',')
                        selected_assignees = [int(x.strip()) - 1 for x in selected_assignees if re.match("^\d+$", x.strip())]
            
                        removed_assignees = []
                        for index in selected_assignees:
                            if 0 <= index < len(selected_task["assignees"]):
                                removed_assignees.append(selected_task["assignees"].pop(index))
                            else:
                                print("Invalid assignee choice.")
                                continue  # Restart the loop to get input again
                        else:
                            task_manager.save_history(selected_project["project_id"], "Assignees Removed", selected_task["title"], 
                                                     ', '.join(removed_assignees), username, datetime.datetime.now())
                            print("Assignees removed successfully.")
                            input("Press Enter to continue...")
                            break  # Exit the loop after successful input
                
                    elif assignee_choice == '3':
                        break  # Exit the loop and return to the main menu
                    else:
                        print("Invalid choice.")
                        continue  # Restart the loop to get valid input
            else:
                print("You are not allowed to change this section.")
                input("Press Enter to continue...")
                return

        elif choice == '5':
            if username == selected_project["owner"] or username in selected_task["assignees"]:
                new_deadline = get_valid_datetime("Enter new deadline (YYYY-MM-DD HH:MM) or leave blank: ")
                if new_deadline is not None:
                    selected_task["deadline"] = new_deadline.strftime("%Y-%m-%d %H:%M")
                    task_manager.save_history(selected_project["project_id"], "Deadline Changed", selected_task["title"], 
                                      selected_task["deadline"], username, datetime.datetime.now())
                    print("Deadline changed successfully.")
                    input("Press Enter to continue...")
                    clear_screen()
                else:
                    print("Deadline remains unchanged.")
                    input("Press Enter to continue...")
                    clear_screen()
            else:
                print("You are not allowed to change this section.")
                input("Press Enter to continue...")
                clear_screen()
                return
            
        elif choice == '6':
            if username == selected_project["owner"] or username in selected_task["assignees"]:
                print("Select Priority:")
                print("1. CRITICAL")
                print("2. HIGH")
                print("3. MEDIUM")
                print("4. LOW")

                new_priority_choice = input("Choose priority (1-4) or press Enter to keep current priority: ")
        
                if new_priority_choice.isdigit() and 1 <= int(new_priority_choice) <= 4:
                    new_priority = {
                        '1': Priority.CRITICAL,
                        '2': Priority.HIGH,
                        '3': Priority.MEDIUM,
                        '4': Priority.LOW
                    }[new_priority_choice]
                    selected_task["priority"] = new_priority.value
                    task_manager.save_history(selected_project["project_id"], "Priority Changed", selected_task["title"], 
                              new_priority.name, username, datetime.datetime.now())
                    print("Priority changed successfully.")
                elif new_priority_choice == "":
                    print("Keeping current priority.")
                else:
                    print("Invalid priority choice. Please choose a number between 1 and 4.")

            else:
                print("You are not allowed to change this section.")
        
            input("Press Enter to continue...")
            clear_screen()


        elif choice == '7':
            if username == selected_project["owner"] or username in selected_task["assignees"]:
                print("Select Status:")
                print("1. BACKLOG")
                print("2. TODO")
                print("3. DOING")
                print("4. DONE")
                print("5. ARCHIVED")

                new_status_choice = input("Choose status (1-5) or press Enter to keep current status: ")
        
                if new_status_choice.isdigit() and 1 <= int(new_status_choice) <= 5:
                    new_status = {
                        '1': Status.BACKLOG,
                        '2': Status.TODO,
                        '3': Status.DOING,
                        '4': Status.DONE,
                        '5': Status.ARCHIVED
                    }[new_status_choice]
                    selected_task["status"] = new_status.value
                    task_manager.save_history(selected_project["project_id"], "Status Changed", selected_task["title"], 
                              new_status.name, username, datetime.datetime.now())
                    print("Status changed successfully.")
                elif new_status_choice == "":
                    print("Keeping current status.")
                else:
                    print("Invalid status choice. Please choose a number between 1 and 5.")

            else:
                print("You are not allowed to change this section.")
        
            input("Press Enter to continue...")
            clear_screen()

        elif choice == '8':
            while True:
                print("Comment Menu:")
                print("1. Add Comment")
                print("2. Remove Comment")
                print("3. Exit")

                comment_choice = input("Choose an option: ")

                if comment_choice not in ['1', '2', '3']:
                    print("Invalid option. Please choose a valid option.")
                    continue

                if comment_choice == '1':
                    try:
                        comment_text = input("Enter your comment: ")
                        if not comment_text:
                            print("Comment cannot be empty.")
                            continue
                        selected_task["comments"].append({"username": username, "comment": comment_text})
                        task_manager.save_history(selected_project["project_id"], "Comment Added", selected_task["title"], 
                                                  comment_text, username, datetime.datetime.now())
                        print("Comment added successfully.")
                        input("Press Enter to continue...")
                        clear_screen()
                    except Exception as e:
                        print(f"Error adding comment: {e}")

                elif comment_choice == '2':
                    if not selected_task["comments"]:
                        print("No comments to remove.")
                        input("Press Enter to continue...")
                        continue

                    print("Select a comment to remove:")
                    for index, comment in enumerate(selected_task["comments"], 1):
                        print(f"{index}. {comment['username']}: {comment['comment']}")

                    while True:
                        remove_choice = input("Enter the comment number to remove (or press Enter to cancel): ")
                        if remove_choice == "":
                            break
                        elif re.match("^\d+$", remove_choice):
                            remove_choice = int(remove_choice) - 1
                            if 0 <= remove_choice < len(selected_task["comments"]):
                                comment_to_remove = selected_task["comments"][remove_choice]
                                if comment_to_remove["username"] == username or username == selected_project["owner"]:
                                    try:
                                        # Remove the comment and save the changes
                                        selected_task["comments"].remove(comment_to_remove)
                                        task_manager.save_history(
                                            selected_project["project_id"], 
                                            "Comment Removed", 
                                            selected_task["title"],
                                            comment_to_remove["comment"], 
                                            username, 
                                            datetime.datetime.now()
                                        )
                                        print("Comment removed successfully.")
                                        input("Press Enter to continue...")
                                        clear_screen()
                                        break  # Return to the main comment menu
                                    except Exception as e:
                                        print(f"Error removing comment: {e}")
                                else:
                                    print("You do not have permission to remove this comment.")
                            else:
                                print("Invalid comment number.")
                        else:
                            print("Invalid input. Please enter a valid comment number.")
                elif comment_choice == '3':
                    break

        elif choice == '9':
            task_manager.update_task(selected_task['task_id'], selected_task)
            print("Task saved and exited.")
            return selected_task
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")
            clear_screen()
    

def delete_task(username, selected_project):
    if selected_project['owner'] != username:
        print("You do not have permission to delete tasks for this project.")
        input("Press Enter to continue...")
        clear_screen()
        return

    task_manager = TaskManager()
    project_id = selected_project["project_id"]
    
    # Extract tasks related to the selected project
    project_tasks = [task for task in task_manager.tasks.values() if task.get('project_id') == project_id]
    
    # Filter tasks owned by the user
    user_tasks = [task for task in project_tasks if selected_project.get('owner') == username]
    
    # Check if the user has any tasks in the project
    if not user_tasks:
        print("You don't have any tasks in your project.")
        input("Press Enter to continue...")
        return

    print("Select Task to Delete:")
    for index, task in enumerate(user_tasks, 1):
        print(f"{index}. {task['title']} - Deadline: {task['deadline']}")

    # Prompt user to select a task
    selected_task_index = input("Enter the number of the task to delete: ")
    if not selected_task_index.isdigit() or int(selected_task_index) < 1 or int(selected_task_index) > len(user_tasks):
        print("Invalid task selection. Please enter a valid task number.")
        input("Press Enter to continue...")
        return

    selected_task = user_tasks[int(selected_task_index) - 1]

    confirm = input(f"Are you sure you want to delete task '{selected_task['title']}'? (y/n): ")
    if confirm.lower() != 'y':
        print("Task deletion canceled.")
        input("Press Enter to continue...")
        return

    # Remove the task
    del task_manager.tasks[selected_task['task_id']]
    task_manager.save_tasks(task_manager.tasks)
    task_manager.save_history(project_id, "Task Deleted", selected_task["title"], selected_task['title'], username, datetime.datetime.now())
    print("Task deleted successfully.")
    input("Press Enter to continue...")

def view_tasks(selected_project, task_manager, username):
    console = Console()
    # Load tasks from tasks.json
    tasks = task_manager.load_tasks()

    if not isinstance(tasks, dict):
        print("Error: Loaded tasks are not in the expected format.")
        return

    # Filter tasks based on project_id
    project_tasks = [task for task in tasks.values() if isinstance(task, dict) and task.get("project_id") == selected_project.get("project_id")]

    if not project_tasks:
        print("Error: No tasks in this project.")
        input("Press Enter to continue...")
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

    table = Table(title="Tasks Status", box=SIMPLE)

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
            task_choice = int(input("Enter the number of the task you want to view or edit: "))
            if task_choice in label_to_number.values():
                break
            else:
                print("Invalid number. Please enter a valid task number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Get the selected task based on the user's choice
    selected_label = next(label for label, number in label_to_number.items() if number == task_choice)
    selected_task = next(task for task in project_tasks if task["label"] == selected_label)

    # Display menu for task options
    while True:
        clear_screen()
        print("Task Menu:")
        print("1. View Task Details")
        print("2. Edit Task")
        print("3. Exit")

        menu_choice = input("Choose an option: ")

        if menu_choice == '1':
            
            try:
                # Display task details
                print(f"task_id: {selected_task['task_id']}")
                print(f"Label: {selected_task['label']}")
                print(f"Title: {selected_task.get('title', 'N/A')}")
                print(f"Description: {selected_task.get('description', 'N/A')}")
                print(f"Assignees: {', '.join(selected_task['assignees'])}")
                deadline = selected_task.get('deadline')
                if deadline:
                    deadline_formatted = datetime.datetime.fromisoformat(deadline).strftime("%Y-%m-%d %H:%M")
                else:
                    deadline_formatted = 'N/A'
                print(f"Deadline: {deadline_formatted}")
                print(f"Priority: {selected_task.get('priority', 'N/A')}")
                print(f"Status: {selected_task.get('status', 'N/A')}")
                print("Comments:")
                for comment in selected_task.get('comments', []):
                    print(f"  {comment['username']}: {comment['comment']}")
                input("Press Enter to continue...")
            except KeyError as e:
                print(f"Error: Missing key {e}")
                input("Press Enter to continue...")
        elif menu_choice == '2':
            selected_task = edit_task(username, selected_project, selected_task, task_manager)  # Update selected_task with the returned value
        elif menu_choice == '3':
            break

        else:
            print("Invalid choice. Please try again.")




def tasks_menu(username, selected_project):
    project_manager = ProjectManager()
    task_manager = TaskManager()
    while True:
        clear_screen()
        print("Tasks Menu:")
        print("1. Create Task")
        print("2. View Task")
        print("3. Delete Task")
        print("4. Exit")

        choice = input("Choose an option: ")
        clear_screen()

        if choice == '1':
            create_task(username, selected_project)
        elif choice == '2':
            view_tasks(selected_project, task_manager, username)
        elif choice == '3':
            delete_task(username, selected_project)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

def edit_project_menu(username, selected_project):
    project_manager = ProjectManager()
    while True:
        clear_screen()
        print("1. Add Member to Project")
        print("2. Remove Member from Project")
        print("3. Manage Tasks")
        print("4. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            member = input("Enter the username of the member you want to add: ")
            project_manager.add_member_to_project(selected_project['project_id'], member, username)
        elif choice == '2':
            member = input("Enter the username of the member you want to remove: ")
            project_manager.remove_member_from_project(selected_project['project_id'], member, username)
        elif choice == '3':
            tasks_menu(username, selected_project)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def account(username):
    project_manager = ProjectManager()

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
            project_manager.create_project(project_id, title, username)

        elif choice == '2':
            selected_project = show_project(username)
            if selected_project:
                edit_project_menu(username, selected_project)

        elif choice == '3':
            project_manager.delete_project(username)

        elif choice == '4':
            project_manager.view_projects(username)
            input("Press Enter to continue...")
            clear_screen()

        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

            
def main():
    clear_screen()
    user_manager = UserManager()
    project_manager = ProjectManager()
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
        elif choice == '3':
            print("[blue]Good luck[/blue] ")
            exit()
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            input("Press Enter to continue...")
            clear_screen()

if __name__ == "__main__":
    main()