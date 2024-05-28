import unittest
from unittest.mock import patch
from main import ProjectManager

class TestDeleteProject(unittest.TestCase):

    @patch('builtins.input', return_value='y')
    def test_delete_project_confirmation_yes(self, mock_input):
        mock_project = {'project_id': '1', 'title': 'ap'}
        with patch.object(ProjectManager, 'select_project', return_value=mock_project):
            manager = ProjectManager()
            self.assertTrue(manager.delete_project('Sara_Nasher'))

    @patch('builtins.input', return_value='n')
    def test_delete_project_confirmation_no(self, mock_input):
        mock_project = {'project_id': '1', 'title': 'ap'}
        with patch.object(ProjectManager, 'select_project', return_value=mock_project):
            manager = ProjectManager()
            self.assertFalse(manager.delete_project('Sara_Nasher'))

    def test_delete_project_nonexistent_project(self):
        with patch.object(ProjectManager, 'select_project', return_value=None):
            manager = ProjectManager()
            self.assertFalse(manager.delete_project('owner'))

if __name__ == '__main__':
    unittest.main()
