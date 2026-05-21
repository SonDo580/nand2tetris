// Implement: pop local i
// . address = RAM[LCL] + i 
// . SP--
// . RAM[address] = RAM[SP]

@i
D=A     // D = i
@LCL
D=D+M   // D = i + RAM[LCL]
@address
M=D     // RAM[address] = RAM[LCL] + i

@SP
M=M-1   // SP--
A=M     // go to address stored in SP
D=M     // D = RAM[SP]

@address
A=M     // go to addr_value = RAM[address]
M=D     // RAM[addr_value] = RAM[SP]

// ++++++++++++++++++++++++++++++++++++++++
// ++++++++++++++++++++++++++++++++++++++++
// ++++++++++++++++++++++++++++++++++++++++


// Implement: push local i
// . address = RAM[LCL] + i
// . RAM[SP] = RAM[address]
// . SP++

@i
D=A     // D = i
@LCL
D=D+M   // D = i + RAM[LCL]

@address
M=D     // RAM[address] = RAM[LCL] + i
A=M     // go to addr_value = RAM[address]
D=M     // D = RAM[addr_value]

@SP
A=M     // go to address stored in SP
M=D     // RAM[SP] = RAM[addr_value]

@SP
M=M+1   // SP++

// ++++++++++++++++++++++++++++++++++++++++
// ++++++++++++++++++++++++++++++++++++++++
// ++++++++++++++++++++++++++++++++++++++++

// argument, this, that: similar implementations