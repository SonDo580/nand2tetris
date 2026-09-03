// === Implement: function Foo.main 4 ===
// ======================================
// 
// - nVars = 4 = number of local variables

// Inject entry point label
(Foo.main)

// Initialize function's local variables
// . set i = nVars = 4
@4
D=A
@i
M=D     // i = 4

// . each iteration: push 0 onto stack to save slot
(Foo.main$init)
@SP
A=M
M=0    
@SP
M=M+1

// . decrement i
@i
M=M-1
D=M

// D != 0 (i > 0) -> push next local variable
@Foo.main$init
D;JNE