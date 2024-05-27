import unittest
import json
from unittest import mock  # اضافه کردن import به این شکل

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

    def test_remove_member_from_project_success(self):
        project_id = "1"
        username = "Sara_Nasher"
        member_to_remove = "q"
        self.assertIn(member_to_remove, self.projects[project_id].get("members", []))
        self.project_manager.remove_member_from_project(project_id, username, member_to_remove)

    def test_remove_member_from_project_cancel(self):
        project_id = "1"
        username = "Sara_Nasher"
        member_to_remove = "test_user"
        self.assertIn(member_to_remove, self.projects[project_id].get("members", []))
        with mock.patch('builtins.input', side_effect=['1', 'n']): 
            self.project_manager.remove_member_from_project(project_id, username, member_to_remove)
        self.assertIn(member_to_remove, self.projects[project_id].get("members", []))

    def test_remove_member_from_project_not_member(self):
        project_id = "1"
        username = "Sara_Nasher"
        member_to_remove = "r"
        self.assertNotIn(member_to_remove, self.projects[project_id].get("members", []))
        result = self.project_manager.remove_member_from_project(project_id, username, member_to_remove)
    def test_remove_member_from_project_not_owner(self):
        project_id = "1"
        username = "not_owner"
        member_to_remove = "q"
        self.project_manager.remove_member_from_project(project_id, username, member_to_remove)
        self.assertEqual(self.project_manager.remove_member_from_project(project_id, username, member_to_remove), None)

    def test_remove_member_from_project_project_not_found(self):
        project_id = "non_existent_project"
        username = "Sara_Nasher"
        member_to_remove = "new_member"
        self.project_manager.remove_member_from_project(project_id, username, member_to_remove)
        self.assertEqual(self.project_manager.remove_member_from_project(project_id, username, member_to_remove), None)

if __name__ == "__main__":
    unittest.main()
