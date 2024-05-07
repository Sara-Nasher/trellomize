from argparse import ArgumentParser
import os
import json


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


