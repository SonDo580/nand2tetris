// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(LOOP)
    // initialize/reset iteration variable
    @i
    M=0     

    // check what key is being pressed
    @KBD
    D=M     

    // jump to 'white' if KBD value is 0
    @WHITE
    D;JEQ

    // jump to 'black' if KBD value is not 0
    @BLACK
    0;JMP


(BLACK)
    // 8192: number of 16-bit registers in screen memory map
    @8192
    D=A     

    // jump to 'loop' when i reaches 8192
    @i
    D=D-M
    @LOOP
    D;JEQ

    // goto the i-th register in the screen memory
    // blacken 16 points on the screen
    @SCREEN
    D=A
    @i
    A=D+M   
    M=-1    
    
    // increase iteration variable
    @i
    M=M+1   

    // next iteration of 'black'
    @BLACK
    0;JMP   
    

(WHITE)
    // 8192: number of 16-bit registers in screen memory map
    @8192
    D=A

    // jump to outer loop when i reaches 8192
    @i
    D=D-M
    @LOOP
    D;JEQ   

    // goto the i-th register in the screen memory
    // whiten 16 points on the screen
    @SCREEN
    D=A
    @i
    A=D+M   
    M=0    
    
    // increase iteration variable
    @i
    M=M+1   

    // next iteration of white
    @WHITE
    0;JMP   