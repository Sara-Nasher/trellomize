import unittest
from unittest.mock import patch, mock_open

from main import UserManager

class TestUserManager(unittest.TestCase):

    @patch('main.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_save_and_load_users(self, mock_dump, mock_load, mock_open):
        user_manager = UserManager()
        users = {"test_user": {"email": "test@gmail.com", "username": "test_user", "password": "Test@123", "active": True}}
        user_manager.save_users(users)
        mock_dump.assert_called_once_with(users, mock_open.return_value, indent=4)
        
        mock_load.return_value = users
        loaded_users = user_manager.load_users()
        self.assertEqual(loaded_users, users)

    @patch('main.User')
    def test_create_user(self, mock_User):
        user_manager = UserManager()
        email, username, password = 'test@gmail.com', 'test_user', 'Test@123'
        user = user_manager.create_user(email, username, password)
        self.assertEqual(user, mock_User.return_value)
        mock_User.assert_called_with(email, username, password)

    @patch('main.ProjectManager')
    @patch('main.Console')
    def test_get_user_projects(self, mock_console, mock_project_manager):
        user_manager = UserManager()
        username = "test_user"
        projects = {"project1": {"owner": username}, "project2": {"members": [username]}}
        mock_project_manager.return_value.load_projects.return_value = projects
        user_projects = user_manager.get_user_projects(username)
        self.assertEqual(user_projects, list(projects.values()))

    @patch('main.Console')
    def test_display_project_members(self, mock_console):
        user_manager = UserManager()
        project = {"members": ["member1", "member2"]}
        console = mock_console.return_value
        user_manager.display_project_members(project)
        console.print.assert_called()


    @patch('main.Console')
    def test_print_sign_up(self, mock_console):
        user_manager = UserManager()
        console = mock_console.return_value
        user_manager.print_sign_up()
        console.print.assert_called()


    @patch('main.Console')
    def test_print_your_account(self, mock_console):
        user_manager = UserManager()
        console = mock_console.return_value
        user_manager.print_your_account()
        console.print.assert_called()

    @patch('main.Console')
    def test_print_login(self, mock_console):
        user_manager = UserManager()
        console = mock_console.return_value
        user_manager.print_login()
        console.print.assert_called()

    @patch('main.Console')
    @patch('builtins.input', side_effect=['test@gmail.com'])
    def test_is_valid_email_valid(self, mock_input, mock_console):
        user_manager = UserManager()
        email = user_manager.is_valid_email('test@gmail.com')
        self.assertEqual(email, 'test@gmail.com')

    @patch('main.Console')
    @patch('builtins.input', side_effect=['Test@123', 'Test@123'])
    def test_is_valid_password_valid(self, mock_input, mock_console):
        user_manager = UserManager()
        password, email, username = user_manager.is_valid_password('test@gmail.com', 'test_user')
        self.assertEqual(password, 'Test@123')

    @patch('main.Console')
    @patch('builtins.input', side_effect=['test@gmail.com', 'test_user', 'Test@123', 'Test@123', 'test_user', 'Test@123'])
    def test_sign_up_valid(self, mock_input, mock_console):
        user_manager = UserManager()
        user_manager.save_users({})
        user_manager.sign_up()

    @patch('main.Console')
    def test_login_valid(self, mock_console):
        user_manager = UserManager()
        user_manager.save_users({"test_user": {"email": "test@gmail.com", "username": "test_user", "password": "Test@1234", "active": True}})
        with patch('builtins.input', return_value='test_user'):
            user_manager.login()


    @patch('main.Console')
    @patch('builtins.input', side_effect=['3'])
    def test_menu_exit_option_valid(self, mock_input, mock_console):
        user_manager = UserManager()
        with self.assertRaises(SystemExit):
            user_manager.menu()

if __name__ == '__main__':
    unittest.main()
