from typing import TextIO, Optional
from enum import Enum


class Command(Enum):
    # Arithmetic-Logic binary
    ADD = "add"
    SUB = "sub"
    AND = "and"
    OR = "or"

    # Arithmetic-Logic unary
    NEG = "neg"
    NOT = "not"

    # Comparison
    EQ = "eq"
    GT = "gt"
    LT = "lt"

    # Push/pop
    PUSH = "push"
    POP = "pop"

    # Branching
    LABEL = "label"
    GOTO = "goto"
    IF_GOTO = "if-goto"

    # Function
    FUNCTION = "function"
    CALL = "call"
    RETURN = "return"


class Segment(Enum):
    LOCAL = "local"
    ARGUMENT = "argument"
    THIS = "this"
    THAT = "that"
    TEMP = "temp"
    STATIC = "static"
    POINTER = "pointer"
    CONSTANT = "constant"


class SegmentPointerLabel:
    SP = "SP"
    LCL = "LCL"
    ARG = "ARG"
    THIS = "THIS"
    THAT = "THAT"


def _join_with_newline(*args) -> str:
    return "\n".join(args)


class AsmCode:
    decrement_sp = _join_with_newline(f"@{SegmentPointerLabel.SP}", "M=M-1")
    increment_sp = _join_with_newline(f"@{SegmentPointerLabel.SP}", "M=M+1")
    goto_sp = _join_with_newline(f"@{SegmentPointerLabel.SP}", "A=M")
    decrement_sp_and_goto_sp = _join_with_newline(decrement_sp, "A=M")
    unconditional_jump = "0;JMP"
    push_D = _join_with_newline(goto_sp, "M=D", f"@{SegmentPointerLabel.SP}", "M=M+1")


class CodeWriter:
    """Generate assembly code from parsed VM instruction."""

    def __init__(self, out_file: TextIO):
        self._out_file = out_file
        self._comparison_label_count: int = 0
        self._current_input_filename: Optional[str] = None
        self._current_function_name: Optional[str] = None
        self._current_function_return_count: int = 0

    def write(self, instruction: str):
        """Output assembly code for current instruction."""
        components = instruction.split()
        asm = self.__asmInstruction(components)
        self._out_file.write(f"// {instruction}\n")
        self._out_file.write(asm)

    def setInputFilename(self, name: str):
        """Set current input file name without '.vm' extension."""
        self._current_input_filename = name

    def writeBootstrap(self):
        """Output bootstrap code."""
        self._current_function_name = "Sys.init"
        self._out_file.write(f"// bootstrap\n")
        self._out_file.write(
            _join_with_newline(
                *self.__initSegmentPointersLines(), self.__asmCall("Sys.init", 0)
            )
        )

    def __initSegmentPointersLines(self) -> list[str]:
        segment_pointer_default = {
            SegmentPointerLabel.SP: 256,
            SegmentPointerLabel.LCL: -1,
            SegmentPointerLabel.ARG: -2,
            SegmentPointerLabel.THIS: -3,
            SegmentPointerLabel.THAT: -4,
        }

        asm_lines: list[str] = []
        for label, value in segment_pointer_default.items():
            if value < 0:
                asm_lines.extend([f"@{-value}", "D=-A"])
            else:
                asm_lines.extend([f"@{value}", "D=A"])
            asm_lines.extend([f"@{label}", "M=D"])

        return asm_lines

    def __asmInstruction(self, components: list[str]) -> str:
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
            return self.__asmPushPop(command, segment, index)
        elif command in [Command.LABEL, Command.GOTO, Command.IF_GOTO]:
            label = components[1]
            return self.__asmBranching(command, label)
        elif command == Command.FUNCTION:
            self._current_function_name = components[1]
            num_local_variables = int(components[2])
            self._current_function_return_count = 0  # reset
            return self.__asmFunction(self._current_function_name, num_local_variables)
        elif command == Command.CALL:
            function_name = components[1]
            num_arguments = int(components[2])
            return self.__asmCall(function_name, num_arguments)
        elif command == Command.RETURN:
            return self.__asmReturn()

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

    def __asmPushPop(self, command: Command, segment: Segment, index: int) -> str:
        if segment == Segment.CONSTANT:
            return self.__asmPushConstant(index)
        elif segment == Segment.STATIC:
            static_variable = f"{self._current_input_filename}.{index}"
            return self.__asmPushPopVariable(command, static_variable)
        elif segment == Segment.POINTER:
            label = [SegmentPointerLabel.THIS, SegmentPointerLabel.THAT][index]
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
            calculate_address_lines = ["@5", "D=D+A"]
        else:
            segment_label = {
                Segment.LOCAL: SegmentPointerLabel.LCL,
                Segment.ARGUMENT: SegmentPointerLabel.ARG,
                Segment.THIS: SegmentPointerLabel.THIS,
                Segment.THAT: SegmentPointerLabel.THAT,
            }[segment]
            calculate_address_lines = [f"@{segment_label}", "D=D+M"]

        address_variable = "address"
        set_address_lines = [
            f"@{index}",
            "D=A",
            *calculate_address_lines,
            f"@{address_variable}",
            "M=D",
        ]
        goto_address_lines = [f"@{address_variable}", "A=M"]
        set_address_and_goto_address_lines = [*set_address_lines, "A=M"]

        if command == Command.PUSH:
            return _join_with_newline(
                *set_address_and_goto_address_lines,
                "D=M",
                AsmCode.goto_sp,
                "M=D",
                AsmCode.increment_sp,
                "",
            )
        elif command == Command.POP:
            return _join_with_newline(
                *set_address_lines,
                AsmCode.decrement_sp_and_goto_sp,
                "D=M",
                *goto_address_lines,
                "M=D",
                "",
            )

    def __asmBranching(self, command: Command, label: str) -> str:
        if command == Command.LABEL:
            return f"({label})\n"
        elif command == Command.GOTO:
            return _join_with_newline(f"@{label}", AsmCode.unconditional_jump, "")
        elif command == Command.IF_GOTO:
            return _join_with_newline(
                AsmCode.decrement_sp_and_goto_sp, "D=M", f"@{label}", "D;JNE", ""
            )

    def __asmFunction(self, function_name: str, num_local_variables: int) -> str:
        if num_local_variables == 0:
            return f"({function_name})\n"

        iteration_variable = "i"
        set_iteration_variable_lines = [
            f"@{num_local_variables}",
            "D=A",
            f"@{iteration_variable}",
            "M=D",
        ]

        init_label = f"{function_name}$init"
        init_local_variables_lines = [
            f"({init_label})",
            AsmCode.goto_sp,
            "M=0",
            AsmCode.increment_sp,
            f"@{iteration_variable}",
            "M=M-1",
            "D=M",
            f"@{init_label}",
            "D;JNE",
        ]

        return _join_with_newline(
            f"({function_name})",
            *set_iteration_variable_lines,
            *init_local_variables_lines,
            "",
        )

    def __asmCall(self, function_name: str, num_arguments: int) -> str:
        return_label = (
            f"{self._current_function_name}$ret.{self._current_function_return_count}"
        )
        self._current_function_return_count += 1

        save_return_address_lines = [
            f"@{return_label}",
            "D=A",
            AsmCode.push_D,
        ]

        reposition_LCL_lines = [
            f"@{SegmentPointerLabel.SP}",
            "D=M",
            f"@{SegmentPointerLabel.LCL}",
            "M=D",
        ]

        if num_arguments == 0:
            calculate_ARG_offset_lines = ["@5", "D=A"]
        else:
            calculate_ARG_offset_lines = [f"@{num_arguments}", "D=A", "@5", "D=D+A"]
        reposition_ARG_lines = [
            *calculate_ARG_offset_lines,
            f"@{SegmentPointerLabel.SP}",
            "D=M-D",
            f"@{SegmentPointerLabel.ARG}",
            "M=D",
        ]

        execute_callee_lines = [f"@{function_name}", AsmCode.unconditional_jump]

        return _join_with_newline(
            *save_return_address_lines,
            *self.__saveSegmentPointersLines(),
            *reposition_ARG_lines,
            *reposition_LCL_lines,
            *execute_callee_lines,
            f"({return_label})",
            "",
        )

    def __saveSegmentPointersLines(self) -> list[str]:
        asm_lines: list[str] = []
        for label in [
            SegmentPointerLabel.LCL,
            SegmentPointerLabel.ARG,
            SegmentPointerLabel.THIS,
            SegmentPointerLabel.THAT,
        ]:
            asm_lines.extend([f"@{label}", "D=M", AsmCode.push_D])

        return asm_lines

    def __asmReturn(self) -> str:
        end_frame_variable = "endFrame"
        return_address_variable = "returnAddress"

        get_end_frame_lines = [
            f"@{SegmentPointerLabel.LCL}",
            "D=M",
            f"@{end_frame_variable}",
            "M=D",
        ]

        save_return_value_lines = [
            AsmCode.decrement_sp_and_goto_sp,
            "D=M",
            f"@{SegmentPointerLabel.ARG}",
            "A=M",
            "M=D",
        ]

        discard_callee_frame_lines = [
            f"@{SegmentPointerLabel.ARG}",
            "D=M",
            f"@{SegmentPointerLabel.SP}",
            "M=D+1",
        ]

        jump_to_return_address_lines = [
            f"@{return_address_variable}",
            "A=M",
            AsmCode.unconditional_jump,
        ]

        return _join_with_newline(
            *get_end_frame_lines,
            *save_return_value_lines,
            *discard_callee_frame_lines,
            *self.__restoreSegmentPointersAndReturnAddressLines(
                end_frame_variable, return_address_variable
            ),
            *jump_to_return_address_lines,
            "",
        )

    def __restoreSegmentPointersAndReturnAddressLines(
        self, end_frame_variable: str, return_address_variable: str
    ) -> list[str]:
        # Offsets of returnAddress and caller's segment pointers from endFrame
        # (saved_value = *(endFrame - offset))
        saved_value_offset = {
            SegmentPointerLabel.THAT: 1,
            SegmentPointerLabel.THIS: 2,
            SegmentPointerLabel.ARG: 3,
            SegmentPointerLabel.LCL: 4,
            return_address_variable: 5,
        }

        asm_lines: list[str] = []
        for label, offset in saved_value_offset.items():
            asm_lines.extend(
                [
                    f"@{offset}",
                    "D=A",
                    f"@{end_frame_variable}",
                    "D=M-D",
                    "A=D",
                    "D=M",
                    f"@{label}",
                    "M=D",
                ]
            )

        return asm_lines
