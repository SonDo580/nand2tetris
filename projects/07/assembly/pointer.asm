// Implement: push pointer 0/1     
// RAM[SP] = THIS/THAT
// SP++

// Implement: pop pointer 0/1
// SP--
// THIS/THAT = RAM[SP]

// push pointer 0
@THIS
D=M
@SP
A=M
M=D     // RAM[SP] = THIS = RAM[3]
@SP
M=M+1   // SP++

// pop pointer 1
@SP
M=M-1   // SP--
A=M
D=M     // D = RAM[SP]
@THAT
M=D     // THAT = RAM[4] = RAM[SP]
