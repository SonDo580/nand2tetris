// x, y is the 2 last addresses in the stack

// Implement: add
@SP
M=M-1   // SP--
A=M     // go to y
D=M     // D = y

@SP     
M=M-1   // SP--
A=M     // go to x
M=D+M   // x = x + y

@SP
M=M+1   // SP++


// Implement: sub
@SP
M=M-1   // SP--
A=M     // go to y
D=M     // D = y

@SP     
M=M-1   // SP--
A=M     // go to x
M=M-D   // x = x - y

@SP
M=M+1   // SP++

// Implement: neg
@SP
M=M-1   // SP--
A=M     // go to y
M=-M    // y = -y

@SP
M=M+1   // SP++