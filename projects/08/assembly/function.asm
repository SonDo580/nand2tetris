// Implement: function Foo.main 4

// Inject entry point label
(Foo.main) 

// Initialize function's local variables
@4
D=A
@i
M=D     // initialize i = 4

(Foo.main$init)
@SP
A=M
M=0    
@SP
M=M+1   // push 0 to the stack

@i
M=M-1
D=M

@Foo.main$init
D;JNE   // stop when i == 0