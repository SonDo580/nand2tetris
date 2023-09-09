# Predefined symbols
SYMBOLS = {
    "SCREEN": 16384,
    "KBD": 24576,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
}

for i in range(16):
    SYMBOLS[f"R{str(i)}"] = i


# Assembly to machine code mapping

# Dest code
DEST_CODE_DICT = {
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
}

# Jump code
JUMP_CODE_DICT = {
    "JGT": "001",
    "JEQ": "010",
    "JLT": "100",
    "JGE": "011",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}

# Comp code
COMP_CODE_DICT = {
    "0": "101010",
    "1": "111111",
    "-1": "111010",
    "D": "001100",
    "!D": "001101",
    "-D": "001111",
    "D+1": "011111",
    "D-1": "001110",
}

for operand2 in ["A", "M"]:
    additional_comp_code = {
        f"{operand2}": "110000",
        f"!{operand2}": "110001",
        f"-{operand2}": "110011",
        f"{operand2}+1": "110111",
        f"{operand2}-1": "110010",
        f"D+{operand2}": "000010",
        f"D-{operand2}": "010011",
        f"{operand2}-D": "000111",
        f"D&{operand2}": "000000",
        f"D|{operand2}": "010101",
    }

    COMP_CODE_DICT.update(additional_comp_code)
