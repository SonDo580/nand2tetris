// === Bootstrap code ===

// Initialize SP: SP = 256
@256
D=A
@SP
M=D

// Set LCL, ARG, THIS, THAT to invalid values
// . LCL = -1
@1
D=-A
@LCL
M=D     
// . ARG = -2
@2
D=-A
@ARG
M=D
// . THIS = -3
@3
D=-A
@THIS
M=D
// . THAT = -4
@4
D=-A
@THAT
M=D

// Call Sys.init: `call Sys.init 0`

// Save return address
@Sys$ret
D=A
// . push onto stack
@SP
A=M
M=D
@SP
M=M+1   

// Save segment pointers: LCL, ARG, THIS, THAT
@LCL
D=M
// . push onto stack
@SP
A=M
M=D
@SP
M=M+1   

// (... ARG, THIS, THAT is similar)

// Reposition ARG: ARG = SP - 5 - nArgs = SP - 5
@5
D=A   
@SP
D=M-D
@ARG
M=D

// Reposition LCL: LCL = SP
@SP
D=M
@LCL
M=D

// Goto Sys.init
@Sys.init
0;JMP

// Inject the return address label
(Sys$ret)