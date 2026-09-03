"""
HackAssembler: Drive the translation process.
- input (source assembly program): a text file named <prog>.asm
- output (generated binary code): a text file named <prog>.hack
- assumption: <prog>.asm is error-free.
"""

import sys
import re
from pathlib import Path
from typing import TextIO

from Parser import Parser, InstructionType
from Code import Code
from SymbolTable import SymbolTable


def main():
    if len(sys.argv) != 2:
        print("Usage: python HackAssembler.py <prog>.asm")
        sys.exit(1)

    in_path = Path(sys.argv[1])
    out_path = in_path.with_suffix(".hack")

    code = Code()
    symbol_table = SymbolTable()

    # 1st pass: handle labels
    with open(in_path, "r") as in_file:
        _process_labels(in_file, symbol_table)

    # 2nd pass: generate binary code
    with open(in_path, "r") as in_file, open(out_path, "w") as out_file:
        _generate_binary_code(in_file, out_file, symbol_table, code)


def _process_labels(in_file: TextIO, symbol_table: SymbolTable):
    """Map each label to line number of next instruction."""
    parser = Parser(in_file)
    line_num = 0  # only count instructions

    while parser.advance():
        instruction_type = parser.instructionType()
        if instruction_type == InstructionType.L:
            label = parser.symbol()
            symbol_table.addEntry(label, line_num)
        else:
            line_num += 1


def _generate_binary_code(
    in_file: TextIO, out_file: TextIO, symbol_table: SymbolTable, code: Code
):
    """Parse instructions and output binary code."""
    parser = Parser(in_file)
    var_location = 16  # each variable is bound to a memory address, start at 16

    while parser.advance():
        instruction_type = parser.instructionType()

        if instruction_type == InstructionType.C:
            dest_bits = code.dest(parser.dest())
            comp_bits = code.comp(parser.comp())
            jump_bits = code.jump(parser.jump())
            out_file.write(f"111{comp_bits}{dest_bits}{jump_bits}\n")

        elif instruction_type == InstructionType.A:
            symbol = parser.symbol()
            if re.match("^[0-9]+$", symbol):  # symbol is numeric address
                address = int(symbol)
            else:  # symbol is variable
                if not symbol_table.contains(symbol):
                    symbol_table.addEntry(symbol, var_location)
                    var_location += 1
                address = symbol_table.getAddress(symbol)
            out_file.write(f"{address:016b}\n")


if __name__ == "__main__":
    main()
