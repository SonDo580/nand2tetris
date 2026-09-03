// === Implement: label LABEL ===
// ==============================
(LABEL)


// === Implement: goto LABEL ===
// =============================
@LABEL
0;JMP


// === Implement: if-goto LABEL ===
// ================================
@SP
M=M-1   // RAM[SP]--
A=M     // go to RAM[SP] (slot above top element of stack, contain popped value)
D=M     // D = RAM[RAM[SP]]

@LABEL
D;JNE   // jump to (LABEL) if D != false (0)
