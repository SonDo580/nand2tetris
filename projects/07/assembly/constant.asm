// Implement: push constant i 
// RAM[SP]=i
// SP++

@i
D=A     // D=i

@SP
A=M     // go to address stored in SP
M=D     // RAM[SP]=D=i

@SP
M=M+1   // SP++