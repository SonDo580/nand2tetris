import sys
from utils import to_asm


def main():
    # Check for correct usage
    if len(sys.argv) != 2:
        print("Usage: python VMTranslator.py <.vm file>")
        exit(1)

    # Open input file
    fname = sys.argv[1]
    try:
        fhandle = open(fname)
    except:
        print(f"File cannot be opened: {fname}")
        exit(1)

    # Get file name without extension (for static variables)
    file = fname.split("/")[-1]
    name_space = file.split(".")[0]

    # Create and open output file
    fout_name = fname.replace(".vm", ".asm")
    fout_handle = open(fout_name, "w")

    for line in fhandle:
        # Remove whitespaces at 2 ends
        line = line.strip()

        # Ignore comments and empty lines
        if line.startswith("//") or len(line) == 0:
            continue

        # Remove inline comments
        indexComment = line.find("//")
        if indexComment != -1:
            line = line[:indexComment].rstrip()

        # Add a comment to the output file (the vm code)
        fout_handle.write(f"// {line}\n")

        # Convert the VM command to Hack assembly
        fout_handle.write(to_asm(line, name_space))

    # Close the files
    fhandle.close()
    fout_handle.close()


if __name__ == "__main__":
    main()
