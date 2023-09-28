// Implement: and
@SP
M=M-1   // SP--
A=M     // go to y
D=M     // D = y

@SP     
M=M-1   // SP--
A=M     // go to x
M=D&M   // x = x & y

@SP
M=M+1   // SP++

// Implement: or
@SP
M=M-1   // SP--
A=M     // go to y
D=M     // D = y

@SP     
M=M-1   // SP--
A=M     // go to x
M=D|M   // x = x | y

@SP
M=M+1   // SP++

// Implement: not
@SP
M=M-1   // SP--
A=M     // go to y
M=!M     // y = !y

@SP
M=M+1   // SP++