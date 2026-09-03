// === Implement: push temp i ===
// ==============================
//
// (i is numeric value, not label)
// . address = 5 + i
// . RAM[RAM[SP]] = RAM[address]
// . RAM[SP]++ 

@i
D=A     // D = i
@5
D=D+A   // D = i + 5

@address
M=D     // RAM[address] = 5 + i
A=M     // go to RAM[address] = 5 + i
D=M     // D = RAM[5 + i]

@SP
A=M     // go to RAM[SP] (slot above top element of stack)
M=D     // RAM[RAM[SP]] = RAM[5 + i]

@SP
M=M+1   // RAM[SP]++


// === Implement: pop temp i ===
// =============================
//
// (i is numeric value, not label)
// . address = 5 + i
// . RAM[SP]--
// . RAM[address] = RAM[RAM[SP]]

@i
D=A     // D = i
@5
D=D+A   // D = i + 5
@address
M=D     // RAM[address] = 5 + i

@SP
M=M-1   // RAM[SP]--
A=M     // go to RAM[SP] (slot above top element of stack, contains popped value)
D=M     // D = RAM[RAM[SP]]

@address
A=M     // go to RAM[address] = 5 + i
M=D     // RAM[5 + i] = RAM[RAM[SP]]
