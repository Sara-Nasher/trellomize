import unittest
from unittest.mock import patch
from io import StringIO
import json
from main import UserManager, ProjectManager

class TestUserManager(unittest.TestCase):
    def setUp(self):
        self.user_manager = UserManager()
        self.project_manager = ProjectManager()

    def test_display_project_members_with_members(self):
        with open("Account/projects.json", "r") as file:
            projects_data = self.project_manager.load_projects()
            project = projects_data["1"]
        expected_output = "Project Members:\n1. test_user\n2. q\n"
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.user_manager.display_project_members(project)
            self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_display_project_members_with_empty_members(self):
        with open("Account/projects.json", "r") as file:
            projects_data = self.project_manager.load_projects()
            project = projects_data["2"]
        expected_output = "Error: No members found for this project.\n"
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.user_manager.display_project_members(project)
            self.assertEqual(mock_stdout.getvalue(), expected_output)

if __name__ == "__main__":
    unittest.main()

