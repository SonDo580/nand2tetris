from typing import TextIO, Optional


class Parser:
    """Read and parse VM code."""

    def __init__(self, in_file: TextIO):
        self._in_file = in_file
        self._current_instruction: Optional[str] = None

    def advance(self) -> bool:
        """
        Get the next instruction and mark it current instruction.
        Return True if found instruction, False if reached EOF.
        """
        while True:
            line = self._in_file.readline()
            if line == "":  # reached EOF
                return False

            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith("//"):
                continue

            # Remove inline comments
            comment_idx = line.find("//")
            if comment_idx != -1:
                line = line[:comment_idx].rstrip()

            self._current_instruction = line
            return True

    def current_instruction(self) -> str:
        return self._current_instruction
