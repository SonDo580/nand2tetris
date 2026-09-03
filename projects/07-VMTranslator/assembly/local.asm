// === Implement: pop local i === 
// ==============================
//
// (i is numeric value, not label)
// . address = RAM[LCL] + i
// . RAM[SP]--
// . RAM[address] = RAM[RAM[SP]]

@i
D=A     // D = i
@LCL
D=D+M   // D = i + RAM[LCL]
@address
M=D     // RAM[address] = RAM[LCL] + i

@SP
M=M-1   // RAM[SP]--
A=M     // go to RAM[SP] (slot above top element of stack, contains popped value)
D=M     // D = RAM[RAM[SP]]

@address
A=M     // go to RAM[address] = RAM[LCL] + i
M=D     // RAM[RAM[LCL] + i] = RAM[SP]


// === Implement: push local i === 
// ===============================
//
// (i is numeric value, not label)
// . address = RAM[LCL] + i
// . RAM[RAM[SP]] = RAM[address]
// . RAM[SP]++

@i
D=A     // D = i
@LCL
D=D+M   // D = i + RAM[LCL]

@address
M=D     // RAM[address] = RAM[LCL] + i
A=M     // go to RAM[address] = RAM[LCL] + i
D=M     // D = RAM[RAM[LCL] + i]

@SP
A=M     // go to RAM[SP] (slot above top element of stack)
M=D     // RAM[RAM[SP]] = RAM[RAM[LCL] + i]

@SP
M=M+1   // RAM[SP]++


// === argument, this, that ===
// ============================
// (similar implementations)