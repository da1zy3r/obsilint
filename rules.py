from typing import Literal

class Rule:
    """Base class for checking and fixing rules."""

    def check(self, file: str) -> None:
        """Check the specified file for rule violations."""
        return None

    def fix(self, file: str) -> None:
        """Fix rule violations in the specified file."""
        return None

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

    def print_violation(self, file: str, line: int, message: str) -> None:
        print('File {}, line {}'.format(file, line))
        print('\t{}'.format(message))

class ExcessiveWhitespace(Rule):
    """Rule for detecting and fixing excessive whitespace."""

    def check(self, file: str, check_code_blocks: bool = False) -> str | None:
        lines = self.get_lines(file)
        code_block_found = False
        for line_idx, line in enumerate(lines):
            if line.startswith('```'):
                code_block_found = not code_block_found
            if code_block_found and not check_code_blocks:
                continue
            if line.startswith('|') and line.endswith(('|', '|\n')) and len(line) > 1:
                line = [i.strip() for i in line[1:].split('|')]
                line = line[:-1]
                line = ' '.join(line)
            gap_found = False
            gap_start = 0
            for ch_idx, ch in enumerate(line):
                if ch == ' ' and ch_idx > 0 and line[ch_idx - 1] != ' ' and not gap_found:
                    gap_found = True
                    gap_start = ch_idx
                elif ch != ' ' and gap_found:
                    if ch_idx - gap_start > 1:
                        self.print_violation(file, line_idx + 1,
                                             'Found a gap with a length of {}'.format(ch_idx - gap_start))
                    gap_found = False
        return None

    def fix(self, file: str, check_code_blocks: bool = False) -> bool:
        lines = self.get_lines(file)
        new_lines = []
        code_block_found = False
        lines_changed = False
        for line in lines:
            if line.startswith('```'):
                code_block_found = not code_block_found
            if code_block_found and not check_code_blocks:
                new_lines.append(line)
                continue
            if line.startswith('|') and line.endswith(('|', '|\n')) and len(line) > 1:
                new_lines.append(line)
                continue
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
                        lines_changed = True
                    gap_found = False
            new_line += line[last_added:]
            new_lines.append(new_line)
        if lines_changed:
            self.write_lines(file, new_lines)
            return True
        return False

class TrailingBlankLines(Rule):
    """Rule for detecting and fixing trailing blank lines."""

    def check(self, file: str) -> str | None:
        lines = self.get_lines(file)
        line_idx = len(lines) - 1
        while line_idx >= 0 and lines[line_idx] == '\n':
            line_idx -= 1
        if line_idx != len(lines) - 1:
            self.print_violation(file, line_idx + 1,
                                 'Found trailing blank line{}'.format('s' if line_idx < len(lines) - 2 else ''))
        return None

    def fix(self, file: str) -> bool:
        lines = self.get_lines(file)
        line_idx = len(lines) - 1
        lines_changed = False
        while line_idx >= 0 and lines[line_idx] == '\n':
            line_idx -= 1
        if line_idx != len(lines) - 1:
            lines = lines[:line_idx + 1]
            lines_changed = True
        if lines_changed:
            self.write_lines(file, lines)
            return True
        return False

class HorizontalRule(Rule):
    """Rule for detecting and fixing non-standard horizontal rules."""

    def check(self, file: str) -> str | None:
        lines = self.get_lines(file)
        for line_idx, line in enumerate(lines):
            count = {'-': 0, '_': 0, '*': 0, ' ': 0, '\t': 0, '\n': 0}
            for ch in line:
                if ch in count.keys():
                    count[ch] += 1
                else:
                    break
            else:
                if line != '---\n' and (count['-'] >= 3 or count['_'] >= 3 or count['*'] >= 3):
                    self.print_violation(file, line_idx + 1,
                                         "Found non-standard horizontal rule: '{}'".format(line.replace('\n', '')))
        return None

    def fix(self, file: str) -> bool:
        lines = self.get_lines(file)
        new_lines = []
        lines_changed = False
        for line in lines:
            count = {'-': 0, '_': 0, '*': 0, ' ': 0, '\t': 0, '\n': 0}
            for ch in line:
                if ch in count.keys():
                    count[ch] += 1
                else:
                    new_lines.append(line)
                    break
            else:
                if line != '---\n' and (count['-'] >= 3 or count['_'] >= 3 or count['*'] >= 3):
                    new_lines.append('---\n')
                    lines_changed = True
                else:
                    new_lines.append(line)
        if lines_changed:
            self.write_lines(file, new_lines)
        return lines_changed

class BlankLinesAroundBlocks(Rule):
    """Ensure blocks are surrounded by blank lines."""

    def __init__(self, block: Literal['code', 'math']):
        self.block = block
        self.block_marker = {'code': '```', 'math': '$$'}[block]

    def check(self, file: str) -> str | None:
        lines = self.get_lines(file)
        previous_line = None
        block_start_found = False
        block_start_idx = 0
        block_end_found = False
        for line_idx, line in enumerate(lines):
            if block_start_found and block_end_found:
                if previous_line != '\n':
                    self.print_violation(file, block_start_idx,
                                         'No blank line before {} block'.format(self.block))
                if line != '\n':
                    self.print_violation(file, line_idx,
                                         'No blank line after {} block'.format(self.block))
                block_start_found = block_end_found = False
            if line.startswith(self.block_marker):
                if block_start_found:
                    block_end_found = True
                    continue
                else:
                    block_start_found = True
                    block_start_idx = line_idx + 1
            if not block_start_found:
                previous_line = line
        return None

    def fix(self, file: str) -> bool:
        return False
