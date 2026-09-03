from enum import Enum
from typing import TextIO, Optional


class InstructionType(Enum):
    A = "A"  # @xxx
    C = "C"  # dest=comp;jump
    L = "L"  # (label)


class Parser:
    """Read and parse instructions."""

    def __init__(self, in_file: TextIO):
        self._in_file = in_file
        self._current_instruction: Optional[str] = None

    # === Get current instruction ===
    # ===============================

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

    # === Parse current instruction ===
    # =================================

    def instructionType(self) -> InstructionType:
        if self._current_instruction.startswith("("):
            return InstructionType.L
        elif self._current_instruction.startswith("@"):
            return InstructionType.A
        return InstructionType.C

    def symbol(self) -> str:
        """
        Return the instruction's symbol.
        Only use if current instruction is A or L.
        """
        if self.instructionType() == InstructionType.L:
            return self._current_instruction[1:-1]  # exclude '(' and  ')'
        elif self.instructionType() == InstructionType.A:
            return self._current_instruction[1:]  # exclude '@'

    def dest(self) -> str:
        """
        Return the instruction's dest field.
        Only use if current instruction is C.
        """
        assign_idx = self._current_instruction.find("=")
        return self._current_instruction[:assign_idx] if assign_idx != -1 else ""

    def comp(self) -> str:
        """
        Return the instruction's comp field.
        Only use if current instruction is C.
        """
        assign_idx = self._current_instruction.find("=")
        semicolon_idx = self._current_instruction.find(";")

        start_idx = assign_idx + 1 if assign_idx != -1 else 0
        end_idx = semicolon_idx if semicolon_idx != -1 else None

        return self._current_instruction[start_idx:end_idx]

    def jump(self) -> str:
        """
        Return the instruction's jump field.
        Only use if current instruction is C.
        """
        semicolon_idx = self._current_instruction.find(";")
        return (
            self._current_instruction[semicolon_idx + 1 :]
            if semicolon_idx != -1
            else ""
        )
