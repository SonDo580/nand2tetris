// Implement: label LABEL
(LABEL)

// Implement: goto LABEL
@LABEL
0;JMP

// Implement: if-goto LABEL
@SP
M=M-1   // SP--
A=M     // go to address stored in SP
D=M     // D = RAM[SP]

@LABEL
D;JNE   // jump to LABEL if D != false
