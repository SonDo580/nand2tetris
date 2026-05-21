// x, y are on top of stack

// Implement: and
@SP
M=M-1   // SP--
A=M     // go to address of y
D=M     // D = y

@SP     
M=M-1   // SP--
A=M     // go to address of x
M=D&M   // x = y & x

@SP
M=M+1   // SP++

// Implement: or
@SP
M=M-1   // SP--
A=M     // go to address of y
D=M     // D = y

@SP     
M=M-1   // SP--
A=M     // go to address of x
M=D|M   // x = y | x

@SP
M=M+1   // SP++

// Implement: not
@SP
M=M-1   // SP--
A=M     // go to address of y
M=!M    // y = !y

@SP
M=M+1   // SP++