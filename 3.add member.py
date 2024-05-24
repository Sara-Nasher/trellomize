
import unittest
import json
from main import ProjectManager, UserManager  

class TestProjectManager(unittest.TestCase):
    def setUp(self):
        self.project_manager = ProjectManager()
        self.user_manager = UserManager()
        self.projects_file = "Account/projects.json"
        self.users_file = "Account/account.json"

        # Load the projects and users from the files
        with open(self.projects_file, "r") as file:
            self.projects = json.load(file)
        with open(self.users_file, "r") as file:
            self.users = json.load(file)

    def test_add_member_to_project_success(self):
        project_id = "ID"
        member = "q"
        username = "Sara"

    # Clear the project's member list before adding the member
        self.projects[project_id]["members"] = []

    # Check that the member is not already in the project
        self.assertNotIn(member, self.projects[project_id].get("members", []))

    # Add the member to the project
        self.project_manager.add_member_to_project(project_id, member, username)

    

    def test_add_member_to_project_already_member(self):
        project_id = "ID"
        member = "q"
        username = "Sara"

    # Add the member to the project first
        self.project_manager.add_member_to_project(project_id, member, username)

    # Try to add the member again
        self.assertFalse(self.project_manager.add_member_to_project(project_id, member, username))

    def test_add_member_to_project_user_not_found(self):
        project_id = "ID"
        member = "non_existent_user"
        username = "Sara"

        # Try to add the member to the project
        self.project_manager.add_member_to_project(project_id, member, username)

        # Check that an error message is printed
        self.assertEqual(self.project_manager.add_member_to_project(project_id, member, username), None)

    def test_add_member_to_project_not_owner(self):
        project_id = "ID"
        member = "q"
        username = "not_owner"

        # Try to add the member to the project
        self.project_manager.add_member_to_project(project_id, member, username)

        # Check that an error message is printed
        self.assertEqual(self.project_manager.add_member_to_project(project_id, member, username), None)

    def test_add_member_to_project_project_not_found(self):
        project_id = "non_existent_project"
        member = "new_member"
        username = "Sara"

        # Try to add the member to the project
        self.project_manager.add_member_to_project(project_id, member, username)

        # Check that an error message is printed
        self.assertEqual(self.project_manager.add_member_to_project(project_id, member, username), None)

if __name__ == "__main__":
    unittest.main()
