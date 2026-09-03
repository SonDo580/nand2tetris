class VMWriter:
    def __init__(self, output_file):
        self._output_file = output_file

    def writePush(self, segment, index):
        self._output_file.write(f"push {segment} {index}\n")

    def writePop(self, segment, index):
        self._output_file.write(f"pop {segment} {index}\n")

    def writeArithmetic(self, command):
        self._output_file.write(f"{command}\n")

    def writeLabel(self, label):
        self._output_file.write(f"label {label}\n")

    def writeGoto(self, label):
        self._output_file.write(f"goto {label}\n")

    def writeIf(self, label):
        self._output_file.write(f"if-goto {label}\n")

    def writeCall(self, func, num_vars):
        self._output_file.write(f"call {func} {num_vars}\n")

    def writeFunction(self, func, num_vars):
        self._output_file.write(f"function {func} {num_vars}\n")

    def writeReturn(self):
        self._output_file.write("return\n")
