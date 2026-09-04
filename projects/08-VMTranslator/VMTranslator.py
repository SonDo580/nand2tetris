"""
VMTranslator: Drive the translation process
- input: VM file <file>.vm or folder containing VM files <folder>
- output (generated assembly): <file>.asm or <folder>/<folder>.asm
- assumption: input is error-free.
"""

import sys
from pathlib import Path

from Parser import Parser
from CodeWriter import CodeWriter

USAGE_MSG = "Usage: python VMTranslator.py {<file>.vm | <folder>}"


def main():
    if len(sys.argv) != 2:
        print(USAGE_MSG)
        sys.exit(1)

    in_path = Path(sys.argv[1])
    if in_path.is_dir():
        vm_file_paths = [p for p in in_path.glob("*.vm") if p.is_file()]
        if not vm_file_paths:
            print("NO VM files found in folder.")
            sys.exit(1)
        out_path = in_path / f"{in_path.name}.asm"
    else:
        if in_path.suffix != ".vm":
            print(USAGE_MSG)
            sys.exit(1)
        vm_file_paths = [in_path]
        out_path = in_path.with_suffix(".asm")

    with open(out_path, "w") as out_file:
        writer = CodeWriter(out_file)
        if in_path.is_dir():
            writer.writeBootstrap()

        for vm_file_path in vm_file_paths:
            with open(vm_file_path, "r") as in_file:
                writer.setInputFilename(vm_file_path.stem)
                parser = Parser(in_file)

                while parser.advance():
                    instruction = parser.currentInstruction()
                    writer.write(instruction)


if __name__ == "__main__":
    main()
