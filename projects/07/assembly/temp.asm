// Implement: push temp i
// address = 5 + i
// RAM[SP]=RAM[address]
// SP++ 
@i
D=A
@5
D=D+A   // D = 5 + i

@address
M=D     // address = 5 + i
A=M     // go to 'address'
D=M     // D = RAM[5 + i]

@SP
A=M     // go to address stored in SP
M=D     // RAM[SP] = RAM[address]

@SP
M=M+1   // SP++

// ++++++++++
// ++++++++++
// ++++++++++

// Implement: pop temp i 
// address = 5 + i
// SP--
// RAM[address]=RAM[SP]
@i
D=A
@5
D=D+A   // D = 5 + i
@address
M=D     // address = 5 + i

@SP
M=M-1   // SP--
A=M     // go to address stored in SP
D=M     // D = RAM[SP]

@address
A=M     // go to 'address'
M=D     // RAM[address] = RAM[SP]
