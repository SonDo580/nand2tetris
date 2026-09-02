// Stack: | ... | x | y |   
//                        ^
//                     RAM[SP]

// === Implement: add ===
// ======================

@SP
M=M-1   // RAM[SP]--
A=M     // go to address of y
D=M     // D = y

@SP     
M=M-1   // RAM[SP]--
A=M     // go to address of x
M=D+M   // x = y + x

@SP
M=M+1   // RAM[SP]++


// === Implement: sub ===
// ======================

@SP
M=M-1   // RAM[SP]--
A=M     // go to address of y
D=M     // D = y

@SP     
M=M-1   // RAM[SP]--
A=M     // go to address of x
M=M-D   // x = x - y

@SP
M=M+1   // RAM[SP]++



// === Implement: neg ===
// ======================

@SP
M=M-1   // RAM[SP]--
A=M     // go to address of y
M=-M    // y = -y

@SP
M=M+1   // RAM[SP]++