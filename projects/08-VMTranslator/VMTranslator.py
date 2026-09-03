import sys
import os

from utils import bootstrap, to_asm


def get_vm_files(dir_path):
    vm_files = []
    for item in os.listdir(dir_path):
        if item.endswith(".vm"):
            vm_files.append(os.path.join(dir_path, item))
    return vm_files


def get_fout_name(input_path):
    root, extension = os.path.splitext(input_path)
    if extension == ".vm":
        return f"{root}.asm"

    output_name = root.split(os.path.sep)[-1]
    return f"{root}{os.path.sep}{output_name}.asm"


def generate_output(fname, fout_handle):
    # Open input file
    fhandle = open(fname)

    # Get file name without extension (for static variables)
    name_space = (os.path.splitext(fname)[0]).split(os.path.sep)[-1]

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

    # Close the input file
    fhandle.close()


def main():
    # Check for correct usage
    if len(sys.argv) != 2:
        print("Usage: python VMTranslator.py <VM file | VM program>")
        exit(1)

    path = sys.argv[1]
    if os.path.isfile(path):
        if not path.endswith(".vm"):
            print("Not a VM file")
            sys.exit(1)

        # Open output file in write mode
        fout_name = get_fout_name(path)
        fout_handle = open(fout_name, "w")

        # Generate output
        generate_output(path, fout_handle)

        # Close the output file
        fout_handle.close()

    elif os.path.isdir(path):
        vm_files = get_vm_files(path)

        # Open output file in append mode
        fout_name = get_fout_name(path)
        fout_handle = open(fout_name, "a")

        # Add bootstrap code
        fout_handle.write(f"// Bootstrap code\n")
        fout_handle.write(bootstrap())

        # Generate output from all .vm files
        for fname in vm_files:
            generate_output(fname, fout_handle)

        # Close the output file
        fout_handle.close()

    else:
        print("File or folder not exist")
        sys.exit(1)


if __name__ == "__main__":
    main()
