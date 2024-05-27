import unittest
import json
from unittest.mock import patch
from main import TaskManager

class TestTaskManagerUpdateTask(unittest.TestCase):

    def setUp(self):
        self.task_manager = TaskManager(tasks_file="test_tasks.json", history_file="test_history.json")
        self.task_manager.tasks = {
            "6c82d293-a091-4734-951c-39d7eec350a9": {
                "task_id": "6c82d293-a091-4734-951c-39d7eec350a9",
                "project_id": "1",
                "title": "d",
                "description": "dw",
                "deadline": "2024-05-17T02:30:28.880163",
                "assignees": ["yasi"],
                "priority": "CRITICAL",
                "status": "TODO",
                "comments": [{"username": "a", "comment": "ef"}],
                "created_at": "2024-05-16T02:30:35.389614"
            }
        }
        self.updated_task = {
            "title": "Updated Title",
            "assignees": ["yasi", "q"],
            "priority": "HIGH",
            "status": "DOING",
            "comments": [{"username": "b", "comment": "updated comment"}]
        }
        with open("Account/tasks.json", "w") as file:
            json.dump(self.task_manager.tasks, file)


    def test_update_existing_task(self):
        task_id = "6c82d293-a091-4734-951c-39d7eec350a9"
        self.task_manager.update_task(task_id, self.updated_task)
        updated_task = self.task_manager.tasks[task_id]
        self.assertEqual(updated_task["title"], "Updated Title")
        self.assertIn("q", updated_task["assignees"])
        self.assertEqual(updated_task["priority"], "HIGH")
        self.assertEqual(updated_task["status"], "DOING")
        self.assertTrue(any(comment["username"] == "b" for comment in updated_task["comments"]))

    def test_update_non_existing_task(self):
        task_id = "non_existent_task_id"
        self.task_manager.update_task(task_id, self.updated_task)
        self.assertNotIn(task_id, self.task_manager.tasks)
    
    def test_update_task_empty_input(self):
        task_id = "6c82d293-a091-4734-951c-39d7eec350a9"
        self.task_manager.update_task(task_id, {})
        updated_task = self.task_manager.tasks[task_id]
        self.assertEqual(updated_task["title"], "d")
        self.assertEqual(updated_task["assignees"], ["yasi"])
        self.assertEqual(updated_task["priority"], "CRITICAL")
        self.assertEqual(updated_task["status"], "TODO")
        self.assertTrue(any(comment["username"] == "a" for comment in updated_task["comments"]))

if __name__ == '__main__':
    unittest.main()
