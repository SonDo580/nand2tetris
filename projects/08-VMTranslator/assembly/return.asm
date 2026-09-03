// === Implement: return ===
// =========================

// Get end address of caller's frame: endFrame = callee's LCL
@LCL
D=M
@endFrame
M=D

// Get return address: returnAddress = *(endFrame - 5)
@5
D=A
@endFrame
D=M-D
A=D
D=M
@returnAddress
M=D

// Put callee's return value right above working stack of caller
@SP
M=M-1   // SP--
A=M
D=M     // D = return value
@ARG
A=M
M=D     // *ARG = D = return value

// Reposition SP (discard callee's stack)
@ARG
D=M
@SP
M=D+1   // SP = ARG + 1

// Restore THAT: THAT = *(endFrame - 1)
@1
D=A
@endFrame
D=M-D
A=D
D=M
@THAT
M=D

// Restore THIS: THIS = *(endFrame - 2)
@2
D=A
@endFrame
D=M-D
A=D
D=M
@THIS
M=D

// Restore ARG: // ARG = *(endFrame - 3)
@3
D=A
@endFrame
D=M-D
A=D
D=M
@ARG
M=D

// Restore LCL: LCL = *(endFrame - 4)
@4
D=A
@endFrame
D=M-D
A=D
D=M
@LCL
M=D

// Jump to return address
@returnAddress
A=M
0;JMP