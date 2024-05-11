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

class Priority(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

# Enum for Task Status
class Status(Enum):
    BACKLOG = "BACKLOG"
    TODO = "TODO"
    DOING = "DOING"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"


class Task:
    def __init__(self, title, description, deadline, assignees, priority=Priority.LOW, status=Status.BACKLOG, comments=None):
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
    def __init__(self, tasks_file="Account/tasks.json"):
        self.tasks_file = tasks_file
        self.tasks = self.load_tasks()

    def save_tasks(self):
        with open(self.tasks_file, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def load_tasks(self):
        try:
            with open(self.tasks_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def create_task(self, project_id, title, description, deadline, assignees, priority=Priority.LOW, status=Status.BACKLOG, comments=None):
        task_id = str(uuid.uuid4())
        task = {
            "task_id": task_id,
            "project_id": project_id,
            "title": title,
            "description": description,
            "deadline": deadline.isoformat(),
            "assignees": assignees,
            "priority": priority.value,
            "status": status.value,
            "comments": comments if comments else [],
            "created_at": datetime.datetime.now().isoformat()
        }
        self.tasks.append(task)
        self.save_tasks()
        return task


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
        user_projects = [proj for proj in projects.values() if proj["owner"] == username or (proj.get("members") and username in proj["members"])]
        return user_projects

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
                print("[bold red]You already have a project with the same title! Please choose a different title.[/bold red]")
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
        
    
    def delete_project(self, project_id, owner):
        projects = self.load_projects()
        if project_id in projects:
            if projects[project_id]["owner"] == owner:
                del projects[project_id]
                self.save_projects(projects)
                return True
            else:
                print("[bold red]You are not the owner of this project![/bold red]")
                return False
        else:
            print("[bold red]Project not found![/bold red]")
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
                    else:
                        print(f"Member '{member}' is already a member of project '{project['title']}'.")
                    self.save_projects(projects)
                else:
                    print("[bold red]User not found![/bold red]")
            else:
                print("[bold red]You are not the owner of this project![/bold red]")
        else:
            print(f"Project with ID '{project_id}' not found.")

    def remove_member_from_project(self, project_id, member, username):
        projects = self.load_projects()
        if project_id in projects:
            project = projects[project_id]
            if project["owner"] == username:
                if "members" in project and member in project["members"]:
                    project["members"].remove(member)
                    print(f"Member '{member}' removed from project '{project['title']}' successfully.")
                    self.save_projects(projects)
                    return True
                else:
                    print(f"Member '{member}' is not a member of project '{project['title']}'")
                    return False
            else:
                print("[bold red]You are not the owner of this project![/bold red]")
                return False
        else:
            print(f"Project with ID '{project_id}' not found.")
            return False
        
    def view_projects(self, username):
        projects = self.load_projects()

        # Create a table with three columns: Project Title, Owner, and Role
        table = Table(title="Your Projects", show_header=True, header_style="bold magenta")
        table.add_column("Project Title", justify="center", style="cyan")
        table.add_column("Owner", justify="center", style="cyan")
        table.add_column("Role", justify="center", style="cyan")

        for proj_id, proj in projects.items():
            # Check if the user is the owner of the project
            if proj["owner"] == username:
                table.add_row(proj["title"], "You", "Owner")
            # Check if the user is a member of the project
            elif "members" in proj and username in proj["members"]:
                table.add_row(proj["title"], proj["owner"], "Member")

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
    print("[bold green]\nAccount created successfully![/bold green]")
    input("Press Enter to continue...")
    user_manager.create_user(email, username, password)
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

def select_project(username):
    projects = ProjectManager().load_projects()
    owner_projects = [proj for proj in projects.values() if proj["owner"] == username]
    
    print("Select a Project:")
    for index, project in enumerate(owner_projects, 1):
        print(f"{index}. {project['title']}")
    
    project_choice = int(input("Enter the project number: ")) - 1
    selected_project = owner_projects[project_choice] if 0 <= project_choice < len(owner_projects) else None
    
    if not selected_project:
        print("Invalid project choice")
        return None
    return selected_project

def create_task(username):
    project_manager = ProjectManager()
    task_manager = TaskManager()
    project = select_project(username)
    if not project:
        return

    project_id = project["project_id"]
    title = input("Enter the task title: ")
    description = input("Enter the task description: ")
    
    end_datetime_input = input("Enter the end date and time (format YYYY-MM-DD HH:MM), leave empty for default: ")
    end_datetime = datetime.datetime.now() + datetime.timedelta(days=1)  # Default 24 hours from now
    if end_datetime_input:
        end_datetime = datetime.datetime.strptime(end_datetime_input, "%Y-%m-%d %H:%M")

    members = project.get("members", [])
    print("Select Members:")
    for index, member in enumerate(members, 1):
        print(f"{index}. {member}")

    member_choices = input("Enter the member numbers (comma-separated): ")
    selected_members = [members[int(choice)-1] for choice in member_choices.split(',') if 0 < int(choice) <= len(members)]
    
    priority = input("Select Priority: (1. CRITICAL, 2. HIGH, 3. MEDIUM, 4. LOW): ")
    selected_priority = {
        '1': Priority.CRITICAL,
        '2': Priority.HIGH,
        '3': Priority.MEDIUM,
        '4': Priority.LOW
    }.get(priority, Priority.LOW)

    status = input("Select Status: (1. BACKLOG, 2. TODO, 3. DOING, 4. DONE, 5. ARCHIVED): ")
    selected_status = {
        '1': Status.BACKLOG,
        '2': Status.TODO,
        '3': Status.DOING,
        '4': Status.DONE,
        '5': Status.ARCHIVED
    }.get(status, Status.BACKLOG)

    comments = input("Enter comments for the task: ").strip()

    new_task = task_manager.create_task(project_id, title, description, end_datetime, selected_members, selected_priority, selected_status, comments)
    print("Task created successfully!")


def tasks_menu(username):
    project_manager = ProjectManager()
    while True:
        print("Tasks Menu:")
        print("1. Create Task")
        print("2. Edit Task")
        print("3. Delete Task")
        print("4. Exit")

        choice = input("Choose an option: ")
        clear_screen()

        if choice == '1':
            create_task(username)
        elif choice == '2':
            pass
        elif choice == '3':
            pass
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")
            

def account(username):
    project_manager = ProjectManager()

    while True:
        print("1. Create Project")
        print("2. Delete Project")
        print("3. Add Member to Project")
        print("4. Remove Member from Project")
        print("5. View Projects")
        print("6. Tasks")
        print("7. Logout")
        choice = input("Choose an option: ")
        clear_screen()
        if choice == '1':
            project_id = input("Enter project ID: ")
            title = input("Enter project title: ")
            project_manager.create_project(project_id, title, username)
            

        elif choice == '2':
            project_id = input("Enter project ID to delete: ")
            confirm = input("Are you sure you want to delete this project? (y/n): ")
            if confirm.lower() == 'y':
                if project_manager.delete_project(project_id, username):
                    print("Project deleted successfully!")
                    input("Press Enter to continue...")
                    clear_screen()
                else:
                    print("[bold red]Failed to delete project![/bold red]")
                    input("Press Enter to continue...")
                    clear_screen()
            else:
                print("Deletion canceled.")
                input("Press Enter to continue...")
                clear_screen()
        elif choice == '3':
            project_id = input("Enter project ID: ")
            member = input("Enter the username of the member you want to add: ")
            project_manager.add_member_to_project(project_id, member, username)
        
        elif choice == '4':
            project_id = input("Enter project ID: ")
            member = input("Enter the username or email of the member you want to remove: ")
            project_manager.remove_member_from_project(project_id, member, username)

        elif choice == '5':  
            project_manager.view_projects(username)
            input("Press Enter to continue...")
            clear_screen()

        elif choice == '6':
            tasks_menu(username)


        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")


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
        else:
            print("[blue]Good luck[/blue] ")
            exit()


if __name__ == "__main__":
    main()
