# Constants
SEGMENT_POINTERS = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
ARITHMETIC_LOGIC_COMMANDS = ["add", "sub", "neg", "and", "or", "not"]
COMPARISON_COMMANDS = ["eq", "gt", "lt"]
BRANCHING_COMMANDS = ["label", "goto", "if-goto"]
FUNCTION_COMMANDS = ["function", "call", "return"]

# Common ASM blocks
decrement_SP = "@SP\nM=M-1\n"
increment_SP = "@SP\nM=M+1\n"
load_A_with_M = "A=M\n"
load_M_with_D = "M=D\n"
load_D_with_M = "D=M\n"
load_D_with_A = "D=A\n"
load_SP_to_A = "@SP\nA=M\n"
unconditional_jump = "0;JMP\n"

# Global variables
comparison_label_count = 0
current_function_name = ""
function_label_count = 0


# Generate Bootstrap code
def init_pointer(label, value):
    if value < 0:
        create_temp = f"@{-value}\n" + "D=-A\n"
    else:
        create_temp = f"@{value}\n" + load_D_with_A
    return create_temp + f"@{label}\n" + load_M_with_D


def bootstrap():
    init_SP = init_pointer("SP", 256)
    init_LCL = init_pointer("LCL", -1)
    init_ARG = init_pointer("ARG", -2)
    init_THIS = init_pointer("THIS", -3)
    init_THAT = init_pointer("THAT", -4)
    call_sys_init = produce_call_asm("call Sys.init 0", "Sys$ret")
    return init_SP + init_LCL + init_ARG + init_THIS + init_THAT + call_sys_init


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


# Produce Hack assembly from branching command
def branching_to_asm(command, label):
    if command == "label":
        return f"({label})\n"

    if command == "goto":
        return f"@{label}\n" + unconditional_jump

    if command == "if-goto":
        return decrement_SP + load_A_with_M + load_D_with_M + f"@{label}\n" + "D;JNE\n"


# Produce Hack assembly from return command
def restore_value(label, offset):
    return f"""@{offset}
D=A
@endFrame
D=M-D
A=D
D=M
@{label}
M=D    
"""


def produce_return_asm():
    get_end_frame = "@LCL\n" + load_D_with_M + "@endFrame\n" + load_M_with_D
    get_return_address = restore_value("returnAddress", 5)
    save_return_value = (
        decrement_SP
        + load_A_with_M
        + load_D_with_M
        + "@ARG\n"
        + load_A_with_M
        + load_M_with_D
    )
    reposition_SP = "@ARG\n" + load_D_with_M + "@SP\n" + "M=D+1\n"
    restore_that = restore_value("THAT", 1)
    restore_this = restore_value("THIS", 2)
    restore_arg = restore_value("ARG", 3)
    restore_lcl = restore_value("LCL", 4)
    goto_returnAddress = "@returnAddress\n" + load_A_with_M + unconditional_jump

    return (
        get_end_frame
        + get_return_address
        + save_return_value
        + reposition_SP
        + restore_that
        + restore_this
        + restore_arg
        + restore_lcl
        + goto_returnAddress
    )


# Produce Hack assembly from function command
def set_iteration(count):
    return f"""@{count}
D=A
@i
M=D
"""


def init_local_variables(function_name):
    return f"""({function_name}$init)
@SP
A=M
M=0    
@SP
M=M+1
@i
M=M-1
D=M
@{function_name}$init
D;JNE     
"""


def produce_function_asm(line):
    words = line.split(" ")
    function_name = words[1]
    num_vars = int(words[2])

    if num_vars == 0:
        return f"({function_name})\n"

    return (
        f"({function_name})\n"
        + set_iteration(num_vars)
        + init_local_variables(function_name)
    )


# Produce Hack assembly from call command
push_D_to_stack = f"""@SP
A=M
M=D
@SP
M=M+1
"""

reposition_LCL = f"""@SP
D=M
@LCL
M=D    
"""


def reposition_arg(num_args):
    return f"""@{num_args}
D=A
@5
D=D+A   
@SP
D=M-D
@ARG
M=D    
"""


def save_segment_pointer(label):
    return f"@{label}\n" + load_D_with_M + push_D_to_stack


def produce_call_asm(line, return_label):
    words = line.split(" ")
    function_name = words[1]
    num_args = words[2]

    save_return_address = f"@{return_label}\n" + load_D_with_A + push_D_to_stack
    save_LCL = save_segment_pointer("LCL")
    save_ARG = save_segment_pointer("ARG")
    save_THIS = save_segment_pointer("THIS")
    save_THAT = save_segment_pointer("THAT")
    reposition_ARG = reposition_arg(num_args)
    execute_function = f"@{function_name}\n" + unconditional_jump
    inject_return_label = f"({return_label})\n"

    return (
        save_return_address
        + save_LCL
        + save_ARG
        + save_THIS
        + save_THAT
        + reposition_ARG
        + reposition_LCL
        + execute_function
        + inject_return_label
    )


# Produce Hack assembly from function-related command
def get_return_label(function_name, label_count):
    return f"{function_name}$ret.{label_count}"


def function_commands_to_asm(line):
    global current_function_name
    global function_label_count

    words = line.split(" ")
    command = words[0]

    if command == "return":
        return produce_return_asm()

    if command == "function":
        current_function_name = words[1]
        function_label_count = 0  # reset label index
        return produce_function_asm(line)

    if command == "call":
        function_label_count += 1
        return_label = get_return_label(current_function_name, function_label_count)
        return produce_call_asm(line, return_label)


# Produce Hack assembly from a VM command
def to_asm(line, name_space):
    global comparison_label_count
    words = line.split(" ")
    command = words[0]

    if command in ["push", "pop"]:
        return push_pop_to_asm(line, name_space)

    if command in ARITHMETIC_LOGIC_COMMANDS:
        return arithmetic_logic_to_asm(command)

    if command in COMPARISON_COMMANDS:
        comparison_label_count += 1
        return comparison_to_asm(command, comparison_label_count)

    if command in BRANCHING_COMMANDS:
        return branching_to_asm(command, words[1])

    if command in FUNCTION_COMMANDS:
        return function_commands_to_asm(line)
