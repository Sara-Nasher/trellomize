import unittest
from unittest.mock import patch, MagicMock
from main import TaskManager, Priority, Status, ProjectManager
from datetime import datetime, timedelta
from rich.console import Console
class TestTaskManager(unittest.TestCase):

    @patch('main.TaskManager.get_valid_datetime')
    @patch('builtins.input', side_effect=["TaskLabel", "TaskTitle", "TaskDescription", "", "1", "1,2", "3", "5", "Comments"])
    def test_create_task_valid_input(self, mock_input, mock_get_valid_datetime):
        task_manager = TaskManager()
        selected_project = {"project_id": "1", "owner": "Sara_Nasher"}
        mock_get_valid_datetime.return_value = datetime.now() + timedelta(days=1)
        task_manager.create_task("Sara_Nasher", selected_project)

    @patch('main.TaskManager.get_valid_datetime')
    @patch('builtins.input', side_effect=["", "TaskTitle", "TaskDescription", "TaskLabel", "1", "1,2", "3", "5", "Comments"])
    def test_create_task_empty_label(self, mock_input, mock_get_valid_datetime):
        task_manager = TaskManager()
        selected_project = {"project_id": "1", "owner": "Sara_Nasher"}
        mock_get_valid_datetime.return_value = datetime.now() + timedelta(days=1)
        yield
        task_manager.create_task("Sara_Nasher", selected_project)



    @patch('main.TaskManager.get_valid_datetime')
    @patch('builtins.input', side_effect=["TaskLabel", "TaskTitle", "TaskDescription", "", "1", "1,2", "3", "6", "Comments"])
    def test_create_task_invalid_status(self, mock_input, mock_get_valid_datetime):
        task_manager = TaskManager()
        selected_project = {"project_id": "1", "owner": "Sara_Nasher"}
        mock_get_valid_datetime.return_value = datetime.now() + timedelta(days=1)
        task_manager.create_task("Sara_Nasher", selected_project)


    @patch('main.TaskManager.get_valid_datetime')
    @patch('builtins.input', side_effect=["TaskLabel", "TaskTitle", "TaskDescription", "", "1", "1,2", "5", "1", "Comments"])
    def test_create_task_invalid_priority(self, mock_input, mock_get_valid_datetime):
        task_manager = TaskManager()
        selected_project = {"project_id": "1", "owner": "Sara_Nasher"}
        mock_get_valid_datetime.return_value = datetime.now() + timedelta(days=1)
        task_manager.create_task("Sara_Nasher", selected_project)

    @patch('main.TaskManager.get_valid_datetime')
    @patch('builtins.input', side_effect=["TaskLabel", "", "TaskDescription", "", "1", "1,2", "3", "5", "Comments"])
    def test_create_task_empty_title(self, mock_input, mock_get_valid_datetime):
        task_manager = TaskManager()
        selected_project = {"project_id": "1", "owner": "Sara_Nasher"}
        mock_get_valid_datetime.return_value = datetime.now() + timedelta(days=1)
        yield
        task_manager.create_task("Sara_Nasher", selected_project)


    @patch('main.TaskManager.get_valid_datetime')
    @patch('builtins.input', side_effect=["TaskLabel", "TaskTitle", "TaskDescription", "", "1", "", "3", "5"])
    def test_create_task_empty_comment(self, mock_input, mock_get_valid_datetime):
        task_manager = TaskManager()
        selected_project = {"project_id": "1", "owner": "Sara_Nasher"}
        mock_get_valid_datetime.return_value = datetime.now() + timedelta(days=1)
        task_manager.create_task("Sara_Nasher", selected_project)

if __name__ == '__main__':
    unittest.main()