// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

// initialize R2
@R2
M=0     

// iteration variable
@i
M=0     

(LOOP)
    // compute i - R1
    @R1
    D=M
    @i
    D=M-D 

    // go to END if i == R1
    @END
    D;JEQ   

    // add R0 to R2
    @R0
    D=M
    @R2
    M=M+D   

    // increase iteration variable
    @i
    M=M+1   

    // next interation
    @LOOP
    0;JMP   

// End with an infinite loop
(END)
    @END
    0;JMP   
