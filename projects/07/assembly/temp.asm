// Implement: push temp i
// . address = 5 + i
// . RAM[SP] = RAM[address]
// . SP++ 

@i
D=A     // D = i
@5
D=D+A   // D = i + 5

@address
M=D     // RAM[address] = 5 + i
A=M     // go to addr_value = RAM[address] = 5 + i
D=M     // D = RAM[5 + i]

@SP
A=M     // go to address stored in SP
M=D     // RAM[SP] = RAM[5 + i]

@SP
M=M+1   // SP++

// ++++++++++
// ++++++++++
// ++++++++++

// Implement: pop temp i 
// . address = 5 + i
// . SP--
// . RAM[address] = RAM[SP]

@i
D=A     // D = i
@5
D=D+A   // D = i + 5
@address
M=D     // RAM[address] = 5 + i

@SP
M=M-1   // SP--
A=M     // go to address stored in SP
D=M     // D = RAM[SP]

@address
A=M     // go to RAM[address] = 5 + i
M=D     // RAM[5 + i] = RAM[SP]
