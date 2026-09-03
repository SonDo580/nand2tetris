// Implement: call Foo.mult 2
// Context: we are in a function/method foo of class Foo

// Save the return address label (Foo.foo$ret.{index})
@Foo.foo$ret.1
D=A

@SP
A=M
M=D
@SP
M=M+1   // push D to stack

// Save the caller's segment pointers
@LCL
D=M

@SP
A=M
M=D
@SP
M=M+1   // push D to stack

//... ARG, THIS, THAT are similar to LCL

// Reposition ARG: ARG = SP - 5 - nArgs
// 5: spaces for return adress and caller's segment pointers
@2  
D=A
@5
D=D+A   
@SP
D=M-D
@ARG
M=D

// Repositions LCL: LCL = SP 
@SP
D=M
@LCL
M=D

// goto Foo.mult
@Foo.mult
0;JMP

// Inject the return address label: (Foo.foo$ret.{index})
(Foo.foo$ret.1)