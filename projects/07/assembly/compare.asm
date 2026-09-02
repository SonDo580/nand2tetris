// Stack: | ... | x | y |   
//                        ^
//                     RAM[SP]

// === Implement: eq ===
// =====================

@SP
M=M-1   // RAM[SP]--
A=M     // go to address of y
D=M     // D = y

@SP     
M=M-1   // RAM[SP]--
A=M     // go to address of x
D=M-D   // D = x - y

@TRUE
D;JEQ   // D == 0 -> x == y -> jump to TRUE

@SP
A=M     // go to address of x
M=0     // x = false

@CONTINUE
0;JMP   // jump to CONTINUE

(TRUE)
@SP
A=M     // go to address of x
M=-1    // x = true

(CONTINUE)
@SP
M=M+1   // RAM[SP]++



// === Implement: gt ===
// =====================

// ...similar
@TRUE
D;JGT   // D > 0 -> x > y -> jump to TRUE
// ...similar



// === Implement: lt ===
// =====================

// ...similar
@TRUE
D;JLT   // D < 0 -> x < y -> jump to TRUE
// ...similar