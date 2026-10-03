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
            return "You must specify an Obsidian vault directory after '-v'.\nGiven: {}".format(self.path)
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
        return '\nThe files have been read successfully\n'

    def get_lines(self, file: str) -> list[str]:
        """Read and return all lines from the specified file."""
        file_read = open(file, 'r', encoding='utf-8')
        lines = file_read.readlines()
        file_read.close()
        return lines

    def write_lines(self, file: str, lines: list[str]) -> None:
        """Write the specified lines to the file."""
        file_write = open(file, 'w', encoding='utf-8')
        file_write.writelines(lines)
        file_write.close()
        return None

    def check(self, rules: list[Rule]) -> None:
        """Check all vault files using the specified rules."""
        violations_count = 0
        for file in self.files:
            lines = self.get_lines(file)
            for rule in rules:
                violations_count += rule.check(file, lines)
        if violations_count == 0:
            print('No rule violations found')
        else:
            print('{} rule violations found'.format(violations_count))
        return None

    def fix(self, rules: list[Rule]) -> None:
        """Fix all vault files using the specified rules."""
        fixed_count = 0
        for file in self.files:
            fixed = False
            lines = self.get_lines(file)
            for rule in rules:
                lines, was_fixed = rule.fix(lines)
                fixed += was_fixed
            if fixed:
                self.write_lines(file, lines)
                print('Fixed: {}\n'.format(file))
                fixed_count += 1
        if fixed_count == 0:
            print('No files have been fixed')
        else:
            print('{} files have been fixed'.format(fixed_count))
        return None
