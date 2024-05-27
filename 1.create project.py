import unittest
from unittest.mock import patch
from main import ProjectManager

class TestProjectManager(unittest.TestCase):
    @patch("main.input", side_effect=["", "Title", "Owner"])
    def test_create_project_empty_fields(self, mock_input):
        manager = ProjectManager()
        project = manager.create_project("", "Title", "Owner")
        self.assertIsNone(project)

        project = manager.create_project("ID", "", "Owner")
        self.assertIsNone(project)

        project = manager.create_project("", "", "Owner")
        self.assertIsNone(project)

    @patch("main.input", side_effect=["ID", "AP", "Sara"])
    def test_create_project_success(self, mock_input):
        manager = ProjectManager()
        project = manager.create_project("ID", "AP", "Sara")
        self.assertIsNotNone(project)

    @patch("main.ProjectManager.load_projects")
    @patch("main.input", side_effect=["ID", "Title", "Owner"])
    def test_create_project_duplicate_ids(self, mock_input, mock_load_projects):
        mock_load_projects.return_value = {"ID": {"title": "Existing Title", "owner": "Existing Owner"}}
        manager = ProjectManager()
        project = manager.create_project("ID", "Title", "Owner")
        self.assertIsNone(project)

    @patch("main.ProjectManager.load_projects")
    @patch("main.input", side_effect=["NewID", "Title", "Owner"])
    def test_create_project_duplicate_titles(self, mock_input, mock_load_projects):
        mock_load_projects.return_value = {"ExistingID": {"title": "Title", "owner": "Owner"}}
        manager = ProjectManager()
        project = manager.create_project("NewID", "Title", "Owner")
        self.assertIsNone(project)

if __name__ == "__main__":
    unittest.main()
