import os

class Rule:
    """Base class for checking and fixing rules."""

    def check(self, file: str, check_code_blocks: bool = False) -> None:
        """Check the specified file for rule violations."""
        return None

    def fix(self, file: str, check_code_blocks: bool = False) -> None:
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

class ExcessiveWhitespace(Rule):
    """Rule for detecting and fixing excessive whitespace."""

    def check(self, file: str, check_code_blocks: bool = False) -> str | None:
        if not os.path.isfile(file):
            return 'The file {} does not exist'.format(file)
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
                        print('File {}, line {}'.format(file, line_idx + 1))
                        print('\tFound a gap with a length of {}'.format(ch_idx - gap_start))
                    gap_found = False
        return None

    def fix(self, file: str, check_code_blocks: bool = False) -> str | None:
        if not os.path.isfile(file):
            return 'The file {} does not exist'.format(file)
        lines = self.get_lines(file)
        new_lines = []
        code_block_found = False
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
                    gap_found = False
            new_line += line[last_added:]
            new_lines.append(new_line)
        self.write_lines(file, new_lines)
        return None
