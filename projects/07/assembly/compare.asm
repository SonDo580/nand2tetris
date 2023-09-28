// x, y is the 2 last addresses in the stack

// Implement: eq
@SP
M=M-1   // SP--
A=M     // go to y
D=M     // D = y

@SP     
M=M-1   // SP--
A=M     // go to x
D=M-D   // D = x - y

@TRUE-label
D;JEQ   // D == 0 => x == y => jump to TRUE

@SP
A=M     // go to x
M=0     // set x = false

@CONTINUE-label
0;JMP   // jump to CONTINUE

(TRUE-label)
@SP
A=M     // go to x
M=-1    // set x = true

(CONTINUE-label)
@SP
M=M+1   // SP++

// Implement: gt
// ...similar
@TRUE-label
D;JGT   // D > 0 => x > y => jump to TRUE
// ...similar


// Implement: lt
// ...similar
@TRUE-label
D;JLT   // D < 0 => x < y => jump to TRUE
// ...similar