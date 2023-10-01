import sys
import os
from utils import bootstrap, to_asm


def get_vm_files(path):
    vm_files = []
    dir_list = os.listdir(path)

    for x in dir_list:
        if x.endswith(".vm"):
            vm_files.append(f"{path}/{x}")

    return vm_files


def get_fout_name(path):
    program_name = path.rstrip("/").split("/")[-1]
    return os.path.join(path, f"{program_name}.asm")


def generate_output(fname, fout_handle):
    # Open input file
    fhandle = open(fname)

    # Get file name without extension (for static variables)
    name_space = fname.split("/")[-1][:-3]  # get rid of '.vm' part

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
        print("Usage: python3 vmTranslator.py <VM program folder>")
        exit(1)

    # Get VM files
    path = sys.argv[1]
    vm_files = get_vm_files(path)

    # Create and open output file in append mode
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


if __name__ == "__main__":
    main()
