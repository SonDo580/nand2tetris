import sys
import re

from constants import SYMBOLS, DEST_CODE_DICT, JUMP_CODE_DICT, COMP_CODE_DICT


def main():
    # Check for correct usage
    if len(sys.argv) != 2:
        print("Usage: python Assembler.py <.asm file>")
        exit(1)

    # Open input file
    fname = sys.argv[1]
    try:
        fhandle = open(fname)
    except:
        print(f"File can not be opened: {fname}")
        exit(1)

    # Create and open output file
    fout_name = fname.replace(".asm", ".hack")
    fout_handle = open(fout_name, "w")

    # First pass: add label symbols
    line_counter = 0
    instructions = []
    for line in fhandle:
        # Remove whitespaces at 2 ends
        line = line.strip()

        # Remove comments and empty lines
        if line.startswith("//") or len(line) == 0:
            continue

        # Add label to symbols table
        if line.startswith("("):
            key = line[1 : (len(line) - 1)]  # Exclude the parentheses
            SYMBOLS[key] = line_counter
            continue

        # Store the instruction and increase line counter
        instructions.append(line)
        line_counter += 1

    # Second pass: add variable symbols and generate machine code
    var_register = 16  # Start storing variables from register 16 in memory
    for line in instructions:
        # Remove inline comments
        index_comment = line.find("//")
        if index_comment != -1:
            line = line[:index_comment].rstrip()

        value = line[1:]
        # Check: A-instruction and symbol not existed
        if (
            line.startswith("@")
            and not re.match("^[0-9]+$", value)
            and value not in SYMBOLS
        ):
            # Store new variable and increase variable register 'index'
            SYMBOLS[value] = var_register
            var_register += 1

        # Generate machine code and write to output file
        machine_code = get_machine_code(line)
        fout_handle.write(f"{machine_code}\n")

    # Close file
    fhandle.close()
    fout_handle.close()


def get_dest_code(dest):
    if dest is None:
        return "000"
    return DEST_CODE_DICT[dest]


def get_jump_code(jump):
    if jump is None:
        return "000"
    return JUMP_CODE_DICT[jump]


def get_bit_a(comp):
    # bit 'a' specifies whether to use A or M in computation
    return str(int(comp.find("M") != -1))


def get_comp_code(comp):
    return COMP_CODE_DICT[comp]


def get_machine_code(line):
    # Handle A-instruction
    if line.startswith("@"):
        value = line[1:]

        # value is numeric
        if re.match("^[0-9]+$", value):
            return "0" + format(int(value), "015b")

        # value is symbol
        else:
            return "0" + format(int(SYMBOLS[value]), "015b")

    # Handle C-instruction
    else:
        index_assign = line.find("=")
        index_semicolon = line.find(";")

        if index_semicolon != -1:
            comp = line[0:index_semicolon]
            jump = line[(index_semicolon + 1) :]
            dest = None

        if index_assign != -1:
            dest = line[0:index_assign]
            comp = line[(index_assign + 1) :]
            jump = None

        return (
            "111"
            + get_bit_a(comp)
            + get_comp_code(comp)
            + get_dest_code(dest)
            + get_jump_code(jump)
        )


if __name__ == "__main__":
    main()
