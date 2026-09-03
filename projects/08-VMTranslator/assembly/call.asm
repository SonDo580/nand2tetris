// === Implement: call Foo.mult 2 ===
// ==================================
//
// - caller: function/method 'foo' of class 'Foo'.
// - nArgs = 2 = number of arguments pushed (by caller) onto the stack.


// Save return address: label (Foo.foo$ret.{index})
@Foo.foo$ret.1
D=A
// . push onto stack
@SP
A=M
M=D
@SP
M=M+1

// Save the caller's segment pointers (push onto stack)
@LCL
D=M
// . push onto stack
@SP
A=M
M=D
@SP
M=M+1

//... ARG, THIS, THAT are similar to LCL

// Reposition ARG for callee: ARG = SP - 5 - nArgs
// (5: number of slots for return address and caller's segment pointers)
@2
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D

// Reposition LCL for callee: LCL = SP
@SP
D=M
@LCL
M=D

// Goto Foo.mult
@Foo.mult
0;JMP

// Inject the return address label: (Foo.foo$ret.{index})
(Foo.foo$ret.1)