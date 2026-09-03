// === Implement: push pointer 0/1 ===
//  
// . RAM[RAM[SP]] = RAM[THIS/THAT]
// . RAM[SP]++

// Implement: pop pointer 0/1
// . RAM[SP]--
// . RAM[THIS/THAT] = RAM[RAM[SP]]

// push pointer 0
@THIS
D=M     // D = RAM[THIS]
@SP
A=M
M=D     // RAM[RAM[SP]] = RAM[THIS]
@SP
M=M+1   // RAM[SP]++

// pop pointer 1
@SP
M=M-1   // RAM[SP]--
A=M
D=M     // D = RAM[RAM[SP]]
@THAT
M=D     // RAM[THAT] = RAM[RAM[SP]]
