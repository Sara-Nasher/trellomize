
import unittest
import json
from main import ProjectManager, UserManager  

class TestProjectManager(unittest.TestCase):
    def setUp(self):
        self.project_manager = ProjectManager()
        self.user_manager = UserManager()
        self.projects_file = "Account/projects.json"
        self.users_file = "Account/account.json"
        with open(self.projects_file, "r") as file:
            self.projects = json.load(file)
        with open(self.users_file, "r") as file:
            self.users = json.load(file)

    def test_add_member_to_project_success(self):
        project_id = "ID"
        member = "q"
        username = "Sara"
        self.projects[project_id]["members"] = []
        self.assertNotIn(member, self.projects[project_id].get("members", []))
        self.project_manager.add_member_to_project(project_id, member, username)

    def test_add_member_to_project_already_member(self):
        project_id = "ID"
        member = "q"
        username = "Sara"
        self.project_manager.add_member_to_project(project_id, member, username)
        self.assertFalse(self.project_manager.add_member_to_project(project_id, member, username))

    def test_add_member_to_project_user_not_found(self):
        project_id = "ID"
        member = "non_existent_user"
        username = "Sara"
        self.project_manager.add_member_to_project(project_id, member, username)
        self.assertEqual(self.project_manager.add_member_to_project(project_id, member, username), None)

    def test_add_member_to_project_not_owner(self):
        project_id = "ID"
        member = "q"
        username = "not_owner"
        self.project_manager.add_member_to_project(project_id, member, username)
        self.assertEqual(self.project_manager.add_member_to_project(project_id, member, username), None)

    def test_add_member_to_project_project_not_found(self):
        project_id = "non_existent_project"
        member = "new_member"
        username = "Sara"
        self.project_manager.add_member_to_project(project_id, member, username)
        self.assertEqual(self.project_manager.add_member_to_project(project_id, member, username), None)

if __name__ == "__main__":
    unittest.main()
