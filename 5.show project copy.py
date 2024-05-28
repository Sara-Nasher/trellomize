import unittest
import os
import json
from main import UserManager, ProjectManager

class TestProjectShow(unittest.TestCase):
    def setUp(self):
        self.user_manager = UserManager()
        self.project_manager = ProjectManager()
        self.projects_file = "Account/projects.json"
        with open(self.projects_file, "r") as file:
            self.projects_data = json.load(file)

    def test_show_project_success(self):
        username = "q"
        selected_project = self.project_manager.show_project(username)
        self.assertIsNotNone(selected_project)
        self.assertIn(username, selected_project["owner"])


    def test_show_project_fail(self):
        username = "user_without_projects"
        selected_project = self.project_manager.show_project(username)
        self.assertIsNone(selected_project)

if __name__ == '__main__':
    unittest.main()
