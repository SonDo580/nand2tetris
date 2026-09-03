from typing import TextIO
from enum import Enum


class Command(Enum):
    ADD = "add"
    SUB = "sub"
    AND = "and"
    OR = "or"

    NEG = "neg"
    NOT = "not"

    EQ = "eq"
    GT = "gt"
    LT = "lt"

    PUSH = "push"
    POP = "pop"


class Segment(Enum):
    LOCAL = "local"
    ARGUMENT = "argument"
    THIS = "this"
    THAT = "that"
    TEMP = "temp"
    STATIC = "static"
    POINTER = "pointer"
    CONSTANT = "constant"


class AsmLabel:
    SP = "SP"
    LCL = "LCL"
    ARG = "ARG"
    THIS = "THIS"
    THAT = "THAT"


def _join_with_newline(*args) -> str:
    return "\n".join(args)


class AsmCode:
    decrement_sp = _join_with_newline(f"@{AsmLabel.SP}", "M=M-1")
    increment_sp = _join_with_newline(f"@{AsmLabel.SP}", "M=M+1")
    goto_sp = _join_with_newline(f"@{AsmLabel.SP}", "A=M")
    decrement_sp_and_goto_sp = _join_with_newline(decrement_sp, "A=M")


class CodeWriter:
    """Generate assembly code from parsed VM instruction."""

    def __init__(self, out_file: TextIO):
        self._out_file = out_file
        self._comparison_label_count: int = 0

    def write(self, instruction: str, namespace: str):
        """Output assembly code for current instruction."""
        components = instruction.split()
        asm = self.__asm(components, namespace)
        self._out_file.write(f"// {instruction}\n")  # (optional)
        self._out_file.write(asm)

    def __asm(self, components: list[str], namespace: str) -> str:
        command = Command(components[0])
        if command in [Command.ADD, Command.SUB, Command.AND, Command.OR]:
            return self.__asmArithmeticLogicBinary(command)
        elif command in [Command.NEG, Command.NOT]:
            return self.__asmArithmeticLogicUnary(command)
        elif command in [Command.EQ, Command.GT, Command.LT]:
            return self.__asmComparison(command)
        elif command in [Command.PUSH, Command.POP]:
            segment = Segment(components[1])
            index = int(components[2])
            return self.__asmPushPop(command, segment, index, namespace)

    def __asmArithmeticLogicBinary(self, command: Command) -> str:
        operation = {
            Command.ADD: "M=D+M",
            Command.SUB: "M=M-D",
            Command.AND: "M=D&M",
            Command.OR: "M=D|M",
        }[command]

        return _join_with_newline(
            AsmCode.decrement_sp_and_goto_sp,
            "D=M",
            AsmCode.decrement_sp_and_goto_sp,
            operation,
            AsmCode.increment_sp,
            "",
        )

    def __asmArithmeticLogicUnary(self, command: Command) -> str:
        operation = {
            Command.NEG: "M=-M",
            Command.NOT: "M=!M",
        }[command]

        return _join_with_newline(
            AsmCode.decrement_sp_and_goto_sp, operation, AsmCode.increment_sp, ""
        )

    def __asmComparison(self, command: Command) -> str:
        jump = {Command.EQ: "JEQ", Command.GT: "JGT", Command.LT: "JLT"}[command]
        true_label = f"TRUE-{self._comparison_label_count}"
        continue_label = f"CONTINUE-{self._comparison_label_count}"
        self._comparison_label_count += 1

        return _join_with_newline(
            AsmCode.decrement_sp_and_goto_sp,
            "D=M",
            AsmCode.decrement_sp_and_goto_sp,
            "D=M-D",
            f"@{true_label}",
            f"D;{jump}",
            AsmCode.goto_sp,
            "M=0",
            f"@{continue_label}",
            "0;JMP",
            f"({true_label})",
            AsmCode.goto_sp,
            "M=-1",
            f"({continue_label})",
            AsmCode.increment_sp,
            "",
        )

    def __asmPushPop(
        self, command: Command, segment: Segment, index: int, namespace: str
    ) -> str:
        if segment == Segment.CONSTANT:
            return self.__asmPushConstant(index)
        elif segment == Segment.STATIC:
            return self.__asmPushPopVariable(command, f"{namespace}.{index}")
        elif segment == Segment.POINTER:
            label = [AsmLabel.THIS, AsmLabel.THAT][index]
            return self.__asmPushPopVariable(command, label)
        else:
            return self.__asmPushPopGeneral(command, segment, index)

    def __asmPushConstant(self, constant: int) -> str:
        return _join_with_newline(
            f"@{constant}", "D=A", AsmCode.goto_sp, "M=D", AsmCode.increment_sp, ""
        )

    def __asmPushPopVariable(self, command: Command, variable: str) -> str:
        if command == Command.PUSH:
            return _join_with_newline(
                f"@{variable}", "D=M", AsmCode.goto_sp, "M=D", AsmCode.increment_sp, ""
            )
        elif command == Command.POP:
            return _join_with_newline(
                AsmCode.decrement_sp_and_goto_sp, "D=M", f"@{variable}", "M=D", ""
            )

    def __asmPushPopGeneral(
        self, command: Command, segment: Segment, index: int
    ) -> str:
        if segment == Segment.TEMP:
            calculate_address = _join_with_newline("@5", "D=D+A")
        else:
            segment_label = {
                Segment.LOCAL: AsmLabel.LCL,
                Segment.ARGUMENT: AsmLabel.ARG,
                Segment.THIS: AsmLabel.THIS,
                Segment.THAT: AsmLabel.THAT,
            }[segment]
            calculate_address = _join_with_newline(f"@{segment_label}", "D=D+M")

        address_variable = "address"
        set_address = _join_with_newline(
            f"@{index}",
            "D=A",
            calculate_address,
            f"@{address_variable}",
            "M=D",
        )
        goto_address = _join_with_newline(f"@{address_variable}", "A=M")
        set_address_and_goto_address = _join_with_newline(set_address, "A=M")

        if command == Command.PUSH:
            return _join_with_newline(
                set_address_and_goto_address,
                "D=M",
                AsmCode.goto_sp,
                "M=D",
                AsmCode.increment_sp,
                "",
            )
        elif command == Command.POP:
            return _join_with_newline(
                set_address,
                AsmCode.decrement_sp_and_goto_sp,
                "D=M",
                goto_address,
                "M=D",
                "",
            )
