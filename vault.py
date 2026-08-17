import os
from collections import deque
from rules import Rule

class Vault:
    def __init__(self, path: str):
        """Initialize a vault with the specified path."""
        self.path = path.replace('/', '\\')
        self.files = []

    def read(self, ignored_paths: list[str]) -> str:
        """Read all files from the vault except ignored paths."""
        if not os.path.isdir(self.path):
            return "You must specify a directory of Obsidian vault after '-v'.\nGiven: {}".format(self.path)
        queue = deque([os.path.join(self.path, file) for file in os.listdir(self.path)])
        while queue:
            file_path = queue.popleft()
            skip = False
            for ignored_path in ignored_paths:
                if file_path.endswith(ignored_path):
                    skip = True
                    break
            if skip:
                continue
            if os.path.isdir(file_path):
                for file in os.listdir(file_path):
                    queue.append(os.path.join(file_path, file))
            elif os.path.isfile(file_path) and file_path.endswith('.md'):
                self.files.append(file_path)
                print('File read:', file_path)
        return '\nThe files have been read successfully\n'

    def check(self, rules: list[Rule]) -> None:
        """Check all vault files using the specified rules."""
        for file in self.files:
            for rule in rules:
                rule.check(file)
        return None

    def fix(self, rules: list[Rule]) -> None:
        """Fix all vault files using the specified rules."""
        for file in self.files:
            fixed = False
            for rule in rules:
                fixed += rule.fix(file)
            if fixed:
                print('The file {} has been fixed'.format(file))
        print('The files have been fixed successfully')
        return None
