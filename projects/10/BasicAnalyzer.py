"""
Basic implementation of the Jack Analyzer.
Xxx.jack => output XxxT.xml
"""

import sys
import os

from Tokenizer import Tokenizer


def tokenize(tokenizer, output_file):
    output_file.write(f"<tokens>\n")
    token = tokenizer.next_token()
    while token is not None:
        token_type = tokenizer.token_type()
        output_file.write(f"<{token_type}> {token} </{token_type}>\n")
        token = tokenizer.next_token()
    output_file.write(f"</tokens>\n")


def get_jack_files(dir_path):
    jack_files = []
    for item in os.listdir(dir_path):
        if item.endswith(".jack"):
            jack_files.append(os.path.join(dir_path, item))
    return jack_files


def get_output_path(input_path):
    root, _ = os.path.splitext(input_path)
    return f"output{os.path.sep}{root}T.xml"


def process_file(input_path):
    output_path = get_output_path(input_path)
    with open(input_path) as input_file, open(output_path, "w") as output_file:
        tokenizer = Tokenizer(input_file)
        tokenize(tokenizer, output_file)


def main():
    if len(sys.argv) != 2:
        print("Usage: python BasicAnalyzer.py <Jack program>")
        sys.exit(1)

    path = sys.argv[1]

    if os.path.isfile(path):
        if not path.endswith(".jack"):
            print("Not a Jack file")
            sys.exit(1)
        process_file(path)

    elif os.path.isdir(path):
        jack_files = get_jack_files(path)
        if len(jack_files) == 0:
            print("Not a Jack program")
            sys.exit(1)
        for filepath in jack_files:
            process_file(filepath)

    else:
        print("File or folder not exist")
        sys.exit(1)


if __name__ == "__main__":
    main()
