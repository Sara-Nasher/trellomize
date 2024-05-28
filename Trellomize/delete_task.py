import unittest
import json
from main import TaskManager
from unittest.mock import patch
from datetime import datetime
import io

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.task_manager = TaskManager()
        self.test_task = {
        "task_id": "44da9974-e8b0-4351-9a53-852975067edf",
        "project_id": "1",
        "label": "TaskLabe",
        "title": "TaskTitle",
        "description": "TaskDescription",
        "deadline": "2024-05-25T20:01:37.792616",
        "assignees": [
            "q"
        ],
        "priority": "MEDIUM",
        "status": "ARCHIVED",
        "comments": [
            {
                "username": "Sara_Nasher",
                "comment": "Comments"
            }
        ],
        "created_at": "2024-05-24T20:01:45.516700"
        }
        self.task_manager.tasks["44da9974-e8b0-4351-9a53-852975067edf"] = self.test_task


    @patch('builtins.input', return_value='y')
    def test_delete_task_valid_input(self, mock_input):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.task_manager.delete_task("Sara_Nasher", {"project_id": "1", "owner": "Sara_Nasher"})
            self.assertIn("44da9974-e8b0-4351-9a53-852975067edf", self.task_manager.tasks)

    @patch('builtins.input', return_value='y')
    def test_delete_task_invalid_project_id(self, mock_input):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.task_manager.delete_task("Sara_Nasher", {"project_id": "2", "owner": "Sara_Nasher"})
            self.assertIn("44da9974-e8b0-4351-9a53-852975067edf", self.task_manager.tasks)

    @patch('builtins.input', return_value='y')
    def test_delete_task_insufficient_permissions(self, mock_input):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.task_manager.delete_task("Sara_Nasher", {"project_id": "1", "owner": "someone else"})
            self.assertIn("44da9974-e8b0-4351-9a53-852975067edf", self.task_manager.tasks)

    @patch('builtins.input', return_value='n')
    def test_delete_task_no_tasks_for_user(self, mock_input):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            initial_tasks = self.task_manager.tasks.copy()
            self.task_manager.delete_task("Sara_Nasher", {"project_id": "1", "owner": "someone else"})
            self.assertDictEqual(initial_tasks, self.task_manager.tasks)


if __name__ == "__main__":
    unittest.main()