import json
import os
from main import print_your_account
from rich.console import Console, OverflowMethod
from rich.table import Table
from rich import print
from typing import List



class User:
    def __init__(self, username):
        self.username = username

class Project:
    def __init__(self, project_id, title, owner):
        self.project_id = project_id
        self.title = title
        self.owner = owner
        self.members = []

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

    def delete_project(self, project_id):
        for project in self.projects:
            if project.project_id == project_id:
                self.projects.remove(project)
                self.save_projects()
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
        with open("projects.json", "w") as f:
            project_data = []
            for project in self.projects:
                project_data.append({
                    "project_id": project.project_id,
                    "title": project.title,
                    "owner": project.owner.username,
                    "members": [member.username for member in project.members]
                })
            json.dump(project_data, f, indent=4)

    def load_projects(self):
        if os.path.exists("projects.json"):
            with open("projects.json", "r") as f:
                project_data = json.load(f)
                for data in project_data:
                    owner = User(data["owner"])
                    members = [User(member) for member in data["members"]]
                    project = Project(data["project_id"], data["title"], owner)
                    for member in members:
                        project.add_member(member)
                    self.projects.append(project)

    def save_projects(self):
        account_folder = "Account"
        if not os.path.exists(account_folder):
            os.makedirs(account_folder)
        with open(f"{account_folder}/projects.json", "w") as f:
            project_data = []
            for project in self.projects:
                project_data.append({
                    "project_id": project.project_id,
                    "title": project.title,
                    "owner": project.owner.username,
                    "members": [member.username for member in project.members]
                })
            json.dump(project_data, f, indent=4)


def main():
    project_manager = ProjectManager()
    project_manager.load_projects()

    while True:
        console = Console(width=50)
        print("\n1. Create Project")
        print("2. Delete Project")
        print("3. Add Member to Project")
        print("4. Remove Member from Project")
        print("5. View User Projects")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            project_id = input("Enter project ID: ")
            title = input("Enter project title: ")
            username = input("Enter your username: ")
            owner = User(username)
            project_manager.create_project(project_id, title, owner)

        elif choice == "2":
            project_id = input("Enter project ID to delete: ")
            project_manager.delete_project(project_id)

        elif choice == "3":
            project_id = input("Enter project ID: ")
            member = input("Enter member username to add: ")
            project_manager.add_member_to_project(project_id, User(member))



        elif choice == "4":
            project_id = input("Enter project ID: ")
            member = input("Enter member username to remove: ")
            username = input("Enter your username: ")
            project_manager.remove_member_from_project(project_id, User(member), username)

        elif choice == "5":
            username = input("Enter your username: ")
            user_projects = project_manager.get_user_projects(username)
            print("Your projects:")
            for project_id, title, role in user_projects:
                print(f"Project ID: {project_id}, Title: {title}, Role: {role}")

        elif choice == "6":
            project_manager.save_projects()
            break

if __name__ == "__main__":
    main()
