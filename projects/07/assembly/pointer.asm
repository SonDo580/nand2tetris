// Implement: push pointer 0/1     
// . RAM[SP] = RAM[THIS/THAT]
// . SP++

// Implement: pop pointer 0/1
// . SP--
// . RAM[THIS/THAT] = RAM[SP]

// push pointer 0
@THIS
D=M     // D = RAM[THIS]
@SP
A=M
M=D     // RAM[SP] = RAM[THIS]
@SP
M=M+1   // SP++

// pop pointer 1
@SP
M=M-1   // SP--
A=M
D=M     // D = RAM[SP]
@THAT
M=D     // RAM[THAT] = RAM[SP]
