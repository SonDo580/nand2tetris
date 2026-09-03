"""
VMTranslator: Drive the translation process
- input (VM file): a text file named <filename>.vm
- output (generated assembly): a text file named <filename>.asm
- assumption: <prog>.vm is error-free.
"""

import sys
from pathlib import Path

from Parser import Parser
from CodeWriter import CodeWriter

USAGE_MSG = "Usage: python VMTranslator.py <filename>.vm"


def main():
    if len(sys.argv) != 2:
        print(USAGE_MSG)
        sys.exit(1)

    in_path = Path(sys.argv[1])
    if in_path.suffix != ".vm":
        print(USAGE_MSG)
        sys.exit(1)
    namespace = in_path.stem

    out_path = in_path.with_suffix(".asm")

    with open(in_path, "r") as in_file, open(out_path, "w") as out_file:
        parser = Parser(in_file)
        writer = CodeWriter(out_file)

        while parser.advance():
            instruction = parser.current_instruction()
            writer.write(instruction, namespace)


if __name__ == "__main__":
    main()
