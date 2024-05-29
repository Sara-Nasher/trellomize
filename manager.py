from argparse import ArgumentParser
import os
import json
from main import UserManager
from main import logger, clear_screen
class AdminManager:
    def __init__(self):
        self.admin_file = 'admin.json'

    def create_admin(self, username, password):
        admin_info = {'Username': username, 'Password': password}

        if os.path.exists(os.path.join('Account', self.admin_file)):
            print('Error: Admin already exists.')
        else:
            with open(os.path.join('Account', self.admin_file), 'w') as file:
                json.dump(admin_info, file, indent=4)
            print('Admin created successfully.')
            return admin_info  

    def purge_data(self):
        confirmation = input("Are you sure you want to delete all data? (yes/no): ")
        if confirmation.lower() == 'yes':
            for root, dirs, files in os.walk('Account'):
                for file in files:
                    os.remove(os.path.join(root, file))
            print('All data has been deleted.')
        else:
            print('Operation canceled.')
    
    def block_user(self):
        users = UserManager().load_users()
        active_users = [user for user in users.values() if user.get('active', True)]

        print('Active Users:')
        for i, user in enumerate(active_users, start=1):
            if "username" in user:
                print(f'{i}. {user["username"]} (active: {user.get("active", True)})')
            else:
                print(f'{i}. User with ID {user["id"]} (active: {user.get("active", True)})')

        while True:
            try:
                user_index = int(input('Select a user to block (by number): ')) - 1
                user = active_users[user_index]

                if user:
                    print(f'Are you sure you want to block user {user["username"]}?')
                    decision = input('Enter "yes" to confirm, or any other key to cancel: ')
                    if decision.lower() == 'yes':
                        user['active'] = False
                        UserManager().save_users(users)
                        print(f'[bold green]User {user["username"]} has been blocked.[/bold green]')
                        logger.info("User has been blocked.")
                    else:
                        print('[bold red]Operation canceled.[/bold red]')
                        logger.error("Operation canceled.")
                    break
                else:
                    print('Invalid user.')
                    logger.error("Invalid user.")

            except (ValueError, IndexError):
                print('Invalid input.')
                logger.error("Invalid input.")

    def unblock_user(self):
        users = UserManager().load_users()
        inactive_users = [user for user in users.values() if user.get('active', False) is False]

        print('Inactive Users:')
        for i, user in enumerate(inactive_users, start=1):
            if "username" in user:
                print(f'{i}. {user["username"]} (active: {user.get("active", False)})')
            else:
                print(f'{i}. User with ID {user["id"]} (active: {user.get("active", False)})')

        while True:
            try:
                user_index = int(input('Select a user to unblock (by number): ')) - 1
                user = inactive_users[user_index]

                if user:
                    print(f'Are you sure you want to unblock user {user["username"]}?')
                    decision = input('Enter "yes" to confirm, or any other key to cancel: ')
                    if decision.lower() == 'yes':
                        user['active'] = True
                        UserManager().save_users(users)
                        print(f'[bold green]User {user["username"]} has been unblocked.[/bold green]')
                        logger.info("User has been unblocked.")
                    else:
                        print('[bold red]Operation canceled.[/bold red]')
                        logger.error("Operation canceled.")
                    break
                else:
                    print('Invalid user.')
                    logger.error("Invalid user.")

            except (ValueError, IndexError):
                print('Invalid input.')
                logger.error("Invalid input.")


def main():
    parser = ArgumentParser(description='Manage system admins')
    parser.add_argument('command', choices=['create-admin', 'purge-data', 'block-user', 'unblock-user'], help='Specify the command')
    parser.add_argument('--username', help='Admin username')
    parser.add_argument('--password', help='Admin password')

    args = parser.parse_args()

    admin_manager = AdminManager()

    if args.command == 'create-admin':
        admin_info = admin_manager.create_admin(args.username, args.password)
        if admin_info:  
            print(f'Admin info saved in Account/{admin_manager.admin_file}')

    elif args.command == 'purge-data':
        admin_manager.purge_data()

    elif args.command == 'block-user':
        clear_screen()
        admin_manager.block_user()

    elif args.command == 'unblock-user':
        clear_screen()
        admin_manager.unblock_user()


if __name__ == '__main__':
    main()
