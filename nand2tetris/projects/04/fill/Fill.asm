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
//Initialize: 
@temp
M = 0
//Read keyboard register:
(CHECK)
@24576
D = M
//If keyboard == 0: check Screen is white, otherwise, check Screen is black:
@IS_WHITE
D, JEQ

//If Screen has been black, return CHECK 
@temp
D = M
@CHECK
D, JNE
 
//Otherwise, Set screen black
@temp
M = 1
@SET_SCREEN_BLACK
0, JEQ

//If Screen has been WHITE, return CHECK:
(IS_WHITE)
@temp
D = M
@CHECK
D, JEQ
//Otherwise, Set screen white:
@temp
M = 0
@SET_SCREEN_WHITE
0, JEQ

//Loop all Screen register, each set to -1
//arr = &Screen
//for row = 0; row <= 254; ++row:
// for col = 0; col <= 31; ++col:
//  arr[32 * row + col] = -1 
//	return recheck:
//color = white:
(SET_SCREEN_WHITE)
@color
M = 0
@INTIALIZE
0, JEQ
//color = black:
(SET_SCREEN_BLACK)
@color
M = -1
(INTIALIZE)
//row = 0
@row
M = 0
//col = 0
@col
M = 0
//row_mul: Store 32 * row 
@row_mul
M = 0
//&arr = 16384
@16384
D = A
@arr 
M = D
//
//PROCESS
//
(LOOP_ROW)
//if row > 254: Return.
@row
D = M
@255
D=D-A
@RETURN
D,JGT
//if col > 31, col = 0, row++; 
(LOOP_COL) 
@col
D = M
@31
D=D-A
@COL_RESET
D,JGT
//Process:RAM[ARR + 32 * ROW + COL] = -1
@row_mul
D = M
@col
D = D + M
@arr
D = M + D // arr + 32 * row + col
@addr_to_change
M = D
@color
D = M
@addr_to_change
A = M
M = D //BUG: CHUA SET COLOR
//Set col++
@col
M = M+1
//Return LOOP_COL
@0
D=0
@LOOP_COL
D,JEQ

(COL_RESET)
//Set col  = 0
@col
M = 0
//Set row++
@row
M =M+1
@32
D = A
@row_mul
M = D+M
//Return LOOP
@LOOP_ROW
0, JEQ
//Return Check:
(RETURN)
@CHECK
0, JEQ
