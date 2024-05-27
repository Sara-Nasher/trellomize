import unittest
from main import TaskManager
from unittest.mock import patch
from io import StringIO
import json
from datetime import datetime, timedelta

class TestGetValidDateTime(unittest.TestCase):
    @patch('builtins.input', side_effect=["2024-09-04 04:09"])
    def test_valid_datetime_input(self, mock_input):
        task_manager = TaskManager()
        valid_datetime = task_manager.get_valid_datetime()
        self.assertEqual(valid_datetime, datetime(2024, 9, 4, 4, 9))

    @patch('builtins.input', side_effect=[""])
    def test_empty_input(self, mock_input):
        task_manager = TaskManager()
        valid_datetime = task_manager.get_valid_datetime()
        self.assertIsNone(valid_datetime)

    @patch('builtins.input', side_effect=[(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"), ""])
    def test_past_datetime_input(self, mock_input):
        task_manager = TaskManager()
        valid_datetime = task_manager.get_valid_datetime()
        self.assertIsNone(valid_datetime)

    
    @patch('builtins.input', side_effect=["InvalidFormat", ""])
    def test_invalid_format_input(self, mock_input):
        task_manager = TaskManager()
        valid_datetime = task_manager.get_valid_datetime()
        self.assertIsNone(valid_datetime)




if __name__ == '__main__':
    unittest.main()