// === Implement: push constant i ===
// ==================================
//
// (i is numeric value, not label)
// . RAM[RAM[SP]] = i
// . RAM[SP]++

@i
D=A     // D = i

@SP
A=M     // go to RAM[SP] (slot above top element of stack)
M=D     // RAM[RAM[SP]] = D = i

@SP
M=M+1   // RAM[SP]++