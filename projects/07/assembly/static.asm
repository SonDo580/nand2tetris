// Implement: pop static 5
// SP--
// Foo.5 = RAM[SP]
@SP
M=M-1   // SP--

A=M     // go to address SP points to
D=M     // D = RAM[SP]

@Foo.5
M=D     // Foo.5 = RAM[SP]

// ++++++++++
// ++++++++++
// ++++++++++

// Implement: push static 2
// RAM[SP] = Foo.2
//  SP++
@Foo.2
D=M

@SP
A=M
M=D     // RAM[SP] = Foo.2

@SP
M=M+1   // SP++

// ++++++++++
// ++++++++++
// ++++++++++

// The Hack Assembler will map these references (Foo.5, Foo.2) on to RAM[16] -> RAM[255]
// Order by appearance, not index