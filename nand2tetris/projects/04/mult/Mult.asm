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
// MUL = 0
//for i = 0; i < R1; ++i:
//  MUL = MUL + R0

//Set MUL = 0
@0
D = A
@mul
M = D
//Set i = 0
@i
M = D
(LOOP)
//Check i < R1
@R1
D = M
@i
D = M - D
@END
D, JEQ // i == D
//Process:
@R0
D = M
@mul
M = M + D
//i++
@1
D = A
@i
M = M + D
//Return LOOP:
@0
D = A
@LOOP
D, JEQ

(END)
@mul
D = M
@R2
M=D

(EXIT)
@0
D=0
@EXIT
D, JEQ

