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

    def check_file(self, file):
        if not os.path.isfile(file):
            return 'The file {} does not exist'.format(file)
        lines = open(file, 'r').readlines()
        for line_idx, line in enumerate(lines):
            gap_found = False
            gap_start = 0
            for ch_idx, ch in enumerate(line):
                if ch == ' ' and ch_idx > 0 and line[ch_idx - 1] != ' ' and not gap_found:
                    gap_found = True
                    gap_start = ch_idx
                elif ch != ' ' and gap_found:
                    if ch_idx - gap_start > 1:
                        print('File {}, line {}'.format(file, line_idx + 1))
                        print('\tFound a gap with a length of {}'.format(ch_idx - gap_start))
                    gap_found = False
        return None

    def check(self):
        for file in self.files:
            self.check_file(file)
        return None

    def fix(self):
        pass
