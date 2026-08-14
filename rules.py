import os

class Rule:
    def check(self, file):
        pass

    def fix(self, file):
        pass

    def get_lines(self, file):
        file_read = open(file, 'r', encoding='utf-8')
        lines = file_read.readlines()
        file_read.close()
        return lines

    def write_lines(self, file, lines):
        file_write = open(file, 'w', encoding='utf-8')
        file_write.writelines(lines)
        file_write.close()

class ExcessiveWhitespace(Rule):
    def check(self, file):
        if not os.path.isfile(file):
            return 'The file {} does not exist'.format(file)
        lines = self.get_lines(file)
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

    def fix(self, file):
        if not os.path.isfile(file):
            return 'The file {} does not exist'.format(file)
        lines = self.get_lines(file)
        new_lines = []
        for line in lines:
            gap_found = False
            gap_start = 0
            new_line = ''
            last_added = 0
            for ch_idx, ch in enumerate(line):
                if ch == ' ' and ch_idx > 0 and line[ch_idx - 1] != ' ' and not gap_found:
                    gap_found = True
                    gap_start = ch_idx
                elif ch != ' ' and gap_found:
                    if ch_idx - gap_start > 1:
                        new_line += line[last_added:gap_start + 1] + line[ch_idx]
                        last_added = ch_idx + 1
                    gap_found = False
            new_line += line[last_added:]
            new_lines.append(new_line)
        self.write_lines(file, new_lines)
        return None
