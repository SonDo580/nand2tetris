// Implement: return

// Get the end address of caller's frame 
@LCL
D=M
@endFrame
M=D       // endFrame = LCL

// Get the return address
@5
D=A
@endFrame
D=M-D
A=D
D=M
@returnAddress
M=D        // returnAddress = *(endFrame - 5)

// Handle the return value for the caller
@SP
M=M-1   // SP--
A=M
D=M     // D = return value
@ARG
A=M
M=D     // *ARG = D = return value

// Reposition SP
@ARG
D=M
@SP
M=D+1   // SP = ARG + 1

// Restore THAT
@1
D=A
@endFrame
D=M-D
A=D
D=M
@THAT
M=D        // THAT = *(endFrame - 1)

// Restore THIS
@2
D=A
@endFrame
D=M-D
A=D
D=M
@THIS
M=D        // THAT = *(endFrame - 2)

// Restore ARG
@3
D=A
@endFrame
D=M-D
A=D
D=M
@ARG
M=D        // THAT = *(endFrame - 3)

// Restore LCL
@4
D=A
@endFrame
D=M-D
A=D
D=M
@LCL
M=D        // THAT = *(endFrame - 4)

// go to returnAddress
@returnAddress
A=M
0;JMP