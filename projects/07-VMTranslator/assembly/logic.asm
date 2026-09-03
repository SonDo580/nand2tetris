// Stack: | ... | x | y |   
//                        ^
//                     RAM[SP]

// === Implement: and ===
// ======================

@SP
M=M-1   // RAM[SP]--
A=M     // go to address of y
D=M     // D = y

@SP     
M=M-1   // RAM[SP]--
A=M     // go to address of x
M=D&M   // x = y & x

@SP
M=M+1   // RAM[SP]++


// === Implement: or ===
// =====================

@SP
M=M-1   // RAM[SP]--
A=M     // go to address of y
D=M     // D = y

@SP     
M=M-1   // RAM[SP]--
A=M     // go to address of x
M=D|M   // x = y | x

@SP
M=M+1   // RAM[SP]++


// === Implement: not ===
// =====================

@SP
M=M-1   // RAM[SP]--
A=M     // go to address of y
M=!M    // y = !y

@SP
M=M+1   // RAM[SP]++