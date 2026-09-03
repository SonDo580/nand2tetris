// Bootstrap code

// Initialize SP
@256
D=A
@SP
M=D     // SP = 256

// Set LCL, ARG, THIS, THAT to invalid values
@1
D=-A
@LCL
M=D     // LCL = -1

@2
D=-A
@ARG
M=D     // ARG = -2

@3
D=-A
@THIS
M=D     // THIS = -3

@4
D=-A
@THAT
M=D     // THAT = -4

// Call Sys.init: call Sys.init 0
// Save the return address label
@Sys$ret
D=A

@SP
A=M
M=D
@SP
M=M+1   // push return address to stack

// Save segment pointers
@LCL
D=M

@SP
A=M
M=D
@SP
M=M+1   // push LCL to stack

//... push current ARG, THIS, THAT to stack

// Reposition ARG: ARG = SP - 5
@5
D=A   
@SP
D=M-D
@ARG
M=D

// Repositions LCL: LCL = SP 
@SP
D=M
@LCL
M=D

// goto Sys.init
@Sys.init
0;JMP

// Inject the return address label
(Sys$ret)