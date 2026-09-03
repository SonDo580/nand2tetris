class Code:
    """Generate binary code for C-instruction."""

    def __init__(self):
        self._dest_code_dict = {
            "": "000",
            "M": "001",
            "D": "010",
            "MD": "011",
            "A": "100",
            "AM": "101",
            "AD": "110",
            "AMD": "111",
        }

        self._jump_code_dict = {
            "": "000",
            "JGT": "001",
            "JEQ": "010",
            "JLT": "100",
            "JGE": "011",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111",
        }

        self._comp_code_dict = {
            "0": "0101010",
            "1": "0111111",
            "-1": "0111010",
            "D": "0001100",
            "!D": "0001101",
            "-D": "0001111",
            "D+1": "0011111",
            "D-1": "0001110",
        }
        for operand in ["A", "M"]:
            a_bit = "0" if operand == "A" else "1"
            self._comp_code_dict.update(
                {
                    f"{operand}": f"{a_bit}110000",
                    f"!{operand}": f"{a_bit}110001",
                    f"-{operand}": f"{a_bit}110011",
                    f"{operand}+1": f"{a_bit}110111",
                    f"{operand}-1": f"{a_bit}110010",
                    f"D+{operand}": f"{a_bit}000010",
                    f"D-{operand}": f"{a_bit}010011",
                    f"{operand}-D": f"{a_bit}000111",
                    f"D&{operand}": f"{a_bit}000000",
                    f"D|{operand}": f"{a_bit}010101",
                }
            )

    def dest(self, d: str) -> str:
        """Return binary representation (3 bits) of the parsed 'dest' field."""
        return self._dest_code_dict[d]

    def comp(self, c: str) -> str:
        """Return binary representation (7 bits) of the parsed 'comp' field."""
        return self._comp_code_dict[c]

    def jump(self, j: str) -> str:
        """Return binary representation (3 bits) of the parsed 'jump' field."""
        return self._jump_code_dict[j]
