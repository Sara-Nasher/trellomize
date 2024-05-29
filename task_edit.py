import unittest
import json
from unittest.mock import patch
from main import TaskManager

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.task_manager = TaskManager()
        self.test_task = {
            "task_id": "44da9974-e8b0-4351-9a53-852975067edf",
            "project_id": "1",
            "label": "Tasklabel",
            "title": "TaskTitle",
            "description": "TaskDescription",
            "deadline": "2024-05-25T20:01:37.792616",
            "assignees": ["q"],
            "priority": "MEDIUM",
            "status": "ARCHIVED",
            "comments": [{"username": "Sara_Nasher", "comment": "Comments"}],
            "created_at": "2024-05-24T20:01:45.516700"
        }
        self.selected_project = {"project_id": "1", "owner": "Sara_Nasher"}
        self.selected_task = self.task_manager.tasks["44da9974-e8b0-4351-9a53-852975067edf"]

    @patch('builtins.input', side_effect=['1', 'New Label', ''])
    def test_edit_task_change_label_successfully(self, mock_input):
        new_label = 'New Label'
        self.task_manager.edit_task("q", self.selected_project, self.test_task)
        self.assertEqual(self.test_task["label"], new_label)

    @patch('builtins.input', side_effect=['1', '', ''])
    def test_edit_task_leave_label_unchanged(self, mock_input):
        label_before = self.test_task["label"]
        self.task_manager.edit_task("Another_User", self.selected_project, self.test_task)
        self.assertEqual(self.test_task["label"], label_before)

    @patch('builtins.input', side_effect=['1', 'New Label', ''])
    def test_edit_task_not_allowed_to_change_label(self, mock_input):
        label_before = self.test_task["label"]
        self.task_manager.edit_task("Another_User", self.selected_project, self.test_task)
        self.assertEqual(self.test_task["label"], label_before)

if __name__ == '__main__':
    unittest.main()
