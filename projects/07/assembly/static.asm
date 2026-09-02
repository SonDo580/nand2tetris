// === Implement: pop static 5 ===
// ===============================
//
// . RAM[SP]--
// . RAM[Foo.5] = RAM[RAM[SP]]

@SP
M=M-1   // RAM[SP]--

A=M     // go to RAM[SP] (slot above top element of stack)
D=M     // D = RAM[RAM[SP]]

@Foo.5
M=D     // RAM[Foo.5] = RAM[RAM[SP]]


// === Implement: push static 2 ===
// ================================
//
// . RAM[RAM[SP]] = RAM[Foo.2]
// . RAM[SP]++

@Foo.2
D=M     // D = RAM[Foo.2]

@SP
A=M
M=D     // RAM[RAM[SP]] = RAM[Foo.2]

@SP
M=M+1   // RAM[SP]++


// - The Hack Assembler will map these references (Foo.5, Foo.2) onto RAM[16] -> RAM[255]
// - Order by appearance, not index (Foo.5 may come before Foo.2 in RAM).