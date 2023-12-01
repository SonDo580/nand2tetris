"""
Complete implementation of the Jack Analyzer.
Xxx.jack => output Xxx.xml or Xxx.vm 
Default: output .vm file
"""

import sys
import os
from argparse import ArgumentParser

from tokenizer import Tokenizer
from xmlEngine import XmlEngine
from compileEngine import CompileEngine


def get_jack_files(dir_path):
    jack_files = []
    for item in os.listdir(dir_path):
        if item.endswith(".jack"):
            jack_files.append(os.path.join(dir_path, item))
    return jack_files


def get_output_path(input_path, generate_xml):
    root, _ = os.path.splitext(input_path)
    if generate_xml:
        return f"xml{os.path.sep}{root}.xml"
    return f"output{os.path.sep}{root}.vm"


def process_file(input_path, generate_xml):
    output_path = get_output_path(input_path, generate_xml)
    with open(input_path) as input_file, open(output_path, "w") as output_file:
        tokenizer = Tokenizer(input_file)
        if generate_xml:
            ce = XmlEngine(tokenizer, output_file)
        else:
            ce = CompileEngine(tokenizer, output_file)
        ce.compile()


def main():
    parser = ArgumentParser(description="Compile Jack program into VM program")
    parser.add_argument(
        "jack_program", help="path to Jack file or Jack program directory"
    )
    parser.add_argument(
        "-x", "--xml", action="store_true", help="only generate XML output"
    )

    args = parser.parse_args()
    path = args.jack_program
    generate_xml = args.xml

    if os.path.isfile(path):
        if not path.endswith(".jack"):
            print("Not a Jack file")
            sys.exit(1)
        process_file(path, generate_xml)

    elif os.path.isdir(path):
        jack_files = get_jack_files(path)
        if len(jack_files) == 0:
            print("Not a Jack program")
            sys.exit(1)
        for filepath in jack_files:
            process_file(filepath, generate_xml)

    else:
        print("File or folder not exist")
        sys.exit(1)


if __name__ == "__main__":
    main()
