# Constants
SEGMENT_POINTERS = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
ARITHMETIC_LOGIC_COMMANDS = ["add", "sub", "neg", "and", "or", "not"]
COMPARISON_COMMANDS = ["eq", "gt", "lt"]

# Common ASM blocks
decrement_SP = "@SP\nM=M-1\n"
increment_SP = "@SP\nM=M+1\n"
load_A_with_M = "A=M\n"
load_D_with_M = "D=M\n"
load_M_with_D = "M=D\n"
load_SP_to_A = "@SP\nA=M\n"

# Produce Hack assembly from Arithmetic/Logic command
ARITHMETIC_LOGIC_OPERATIONS = {
    "add": "M=D+M",
    "sub": "M=M-D",
    "neg": "M=-M",
    "and": "M=D&M",
    "or": "M=D|M",
    "not": "M=!M",
}


def arithmetic_logic_to_asm(command):
    operation = ARITHMETIC_LOGIC_OPERATIONS[command] + "\n"

    if command in ["add", "sub", "and", "or"]:
        return (
            decrement_SP
            + load_A_with_M
            + load_D_with_M
            + decrement_SP
            + load_A_with_M
            + operation
            + increment_SP
        )

    if command in ["neg", "not"]:
        return decrement_SP + load_A_with_M + operation + increment_SP


# Produce Hack assembly from Comparison command
COMPARISON_JUMPS = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}


def comparison_to_asm(command, label_count):
    jump = COMPARISON_JUMPS[command]

    compare = f"""D=M-D
@TRUE-{label_count}
D;{jump}
@SP
A=M
M=0
@CONTINUE-{label_count}
0;JMP
(TRUE-{label_count})
@SP
A=M
M=-1
(CONTINUE-{label_count})
"""

    return (
        decrement_SP
        + load_A_with_M
        + load_D_with_M
        + decrement_SP
        + load_A_with_M
        + compare
        + increment_SP
    )


# Produce Hack assembly from Push/Pop command
def push_pop_static_to_asm(operation, constant, name_space):
    # {name_space}.{constant} is a static variable
    goto = f"@{name_space}.{constant}\n"

    if operation == "push":
        return goto + load_D_with_M + load_SP_to_A + load_M_with_D + increment_SP

    if operation == "pop":
        return decrement_SP + load_A_with_M + load_D_with_M + goto + load_M_with_D


def push_pop_pointer_to_asm(operation, constant):
    if constant == "0":
        goto = "@THIS\n"
    elif constant == "1":
        goto = "@THAT\n"

    if operation == "push":
        return goto + load_D_with_M + load_SP_to_A + load_M_with_D + increment_SP

    if operation == "pop":
        return decrement_SP + load_A_with_M + load_D_with_M + goto + load_M_with_D


def save_constant_asm(constant):
    return f"@{constant}\nD=A\n"


def set_address_asm(segment):
    if segment in SEGMENT_POINTERS:
        return f"""@{SEGMENT_POINTERS[segment]}
D=D+M
@address
M=D
"""
    if segment == "temp":
        return f"""@5
D=D+A
@address
M=D
"""


def save_popped_value_asm():
    return f"""@address
A=M
M=D
"""


def push_pop_to_asm(command, name_space):
    words = command.split(" ")
    operation = words[0]
    segment = words[1]
    constant = words[2]

    if segment == "static":
        return push_pop_static_to_asm(operation, constant, name_space)

    if segment == "pointer":
        return push_pop_pointer_to_asm(operation, constant)

    save_constant = save_constant_asm(constant)
    if segment == "constant":
        return save_constant + load_SP_to_A + load_M_with_D + increment_SP

    # Handle remaining segments: local, arguments, temp
    set_address = set_address_asm(segment)
    save_popped_value = save_popped_value_asm()

    if operation == "push":
        return (
            save_constant
            + set_address
            + load_A_with_M
            + load_D_with_M
            + load_SP_to_A
            + load_M_with_D
            + increment_SP
        )

    if operation == "pop":
        return (
            save_constant
            + set_address
            + decrement_SP
            + load_A_with_M
            + load_D_with_M
            + save_popped_value
        )


# This function produce Hack assembly from a VM command
comparison_label_count = 0


def to_asm(line, name_space):
    words = line.split(" ")

    if words[0] in ["push", "pop"]:
        return push_pop_to_asm(line, name_space)

    elif words[0] in ARITHMETIC_LOGIC_COMMANDS:
        return arithmetic_logic_to_asm(words[0])

    elif words[0] in COMPARISON_COMMANDS:
        global comparison_label_count
        comparison_label_count += 1
        return comparison_to_asm(words[0], comparison_label_count)
