// Implement: pop local i 
// address = RAM[LCL] + i
// SP--
// RAM[address] = RAM[SP]
@i
D=A
@LCL
D=D+M   // D = RAM[LCL] + i
@address
M=D     // address = RAM[LCL] + i

@SP
M=M-1   // SP--
A=M     // go to address stored in SP
D=M     // D = RAM[SP]

@address
A=M     // go to 'address'
M=D     // RAM[address] = RAM[SP]

// ++++++++++++++++++++++++++++++++++++++++
// ++++++++++++++++++++++++++++++++++++++++
// ++++++++++++++++++++++++++++++++++++++++


// Implement: push local i
// address = RAM[LCL] + i
// RAM[SP] = RAM[address]
// SP++
@i
D=A
@LCL
D=D+M   // D = RAM[LCL] + i

@address
M=D     // address = RAM[LCL] + i
A=M     // go to 'address'
D=M     // D = RAM[address]

@SP
A=M     // go to address stored in SP
M=D     // RAM[SP] = RAM[address]

@SP
M=M+1   // SP++

// ++++++++++++++++++++++++++++++++++++++++
// ++++++++++++++++++++++++++++++++++++++++
// ++++++++++++++++++++++++++++++++++++++++

// argument, this, that: similar implementation