import unittest
from main import ProjectManager
import json
from unittest.mock import patch, mock_open

class TestProjectManager(unittest.TestCase):
    def test_load_projects_empty(self):
        project_manager = ProjectManager("test_projects_empty.json")
        self.assertEqual(project_manager.load_projects(), {})

    def test_load_projects_non_empty(self):
        project_manager = ProjectManager("test_projects_non_empty.json")
        projects = {"project1": {"title": "Project 1", "owner": "owner1"}, "project2": {"title": "Project 2", "owner": "owner2"}}
        with open("test_projects_non_empty.json", "w") as file:
            file.write(json.dumps(projects))
        self.assertEqual(project_manager.load_projects(), projects)


if __name__ == "__main__":
    unittest.main()
