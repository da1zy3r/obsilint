import os
from collections import deque

class Vault:
    def __init__(self, path):
        self.path = path.replace('/', '\\')
        self.files = []

    def read(self):
        if not os.path.isdir(self.path):
            return "You must specify a directory of Obsidian vault after '-v'.\nGiven: {}".format(self.path)
        queue = deque(os.listdir(self.path))
        for i in range(len(queue)):
            file = queue.popleft()
            queue.append(os.path.join(self.path, file))
        while queue:
            file_path = queue.popleft()
            if os.path.isdir(file_path):
                for file in os.listdir(file_path):
                    queue.append(os.path.join(file_path, file))
            else:
                self.files.append(file_path)
                print('File read:', file_path)
        return 'The files have been read successfully'

    def check(self, rules):
        for file in self.files:
            for rule in rules:
                rule.check(file)
        return None

    def fix(self, rules):
        for file in self.files:
            for rule in rules:
                rule.fix(file)
            print('The file {} has been fixed'.format(file))
        print('The files have been fixed successfully')
        return None
