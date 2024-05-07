import json
import os
from main import print_your_account
from rich.console import Console, OverflowMethod
from rich.table import Table
from rich import print
from typing import List



class User:
    def __init__(self, username):
        self.username = username

class Project:
    def __init__(self, project_id, title, owner):
        self.project_id = project_id
        self.title = title
        self.owner = owner
        self.members = []

    def add_member(self, member):
        if member != self.owner and member not in self.members:
            self.members.append(member)