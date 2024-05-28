import unittest
import os
from main import UserManager, ProjectManager
import json 

class TestProjectSelection(unittest.TestCase):
    def setUp(self):
        self.user_manager = UserManager()
        self.project_manager = ProjectManager()
        self.projects_file = "Account/projects.json"
        with open(self.projects_file, "r") as file:
            self.projects = json.load(file)

    def test_select_project_success(self):

        expected_username = "q"
        selected_project = self.project_manager.select_project(expected_username)
        self.assertIsNotNone(selected_project)
        self.assertEqual(selected_project["owner"], expected_username)

    def test_select_project_fail(self):
        expected_username = 'sar'
        selected_project = self.project_manager.select_project(expected_username)
        self.assertIsNone(selected_project) 

    
if __name__ == '__main__':
    unittest.main()