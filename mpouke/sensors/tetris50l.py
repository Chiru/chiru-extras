import curses
from random import randrange
curses.initscr()
curses.curs_set(0)
win = curses.newwin(18,18,0,0) # Create window and draw border
win.keypad(1)
win.nodelay(1)
f = [ [0x315,0x4cd,0x13f,0xc47],[0x31d,0x4cf,0x137,0xc45],[0x374,0x374,0x374,0x374],[0x741,0x51c,0xdc3,0xf34],
    [0xfc1,0x73c,0x543,0xd14],[0x311,0x4cc,0x133,0xc44],[0xc34,0x341,0x41c,0x1c3]]
def chkFig(crds,s): # collision detection
    chk = all([win.inch(c[1],c[0]) & 255 == 32 for c in crds])
    for c in crds: win.addch(c[1],c[0],'X' if s==1 else 32) if ((chk and s == 1) or s == 0) else None
    return True if s == 0 else chk
def putFig(FP,s): # decode and put figure on the screen
    c = lambda el,n: -1 if (n >> el & 3) == 3 else 1 if (n >> el & 3) == 1 else 0  
    pos = [ c(i ,f[ FP[3] ][ FP[2] ] ) for i in range(0,15,2)[::-1]]
    return chkFig([map(lambda x,y: x+y, FP[0:2]*4,pos)[i-2:i] for i in range(2,9,2)],s)
def MoveFig(FP,key,d): #figure moving function 
    FP[0] = FP[0] - d if key == curses.KEY_LEFT else FP[0] + d if key == curses.KEY_RIGHT else FP[0]
    FP[1] = FP[1] + d if key in [curses.KEY_DOWN, -1] else FP[1]  
    if key == curses.KEY_UP: FP[2] = 0 if FP[2] + d > 3 else 3 if FP[2] + d < 0 else FP[2] + d 
def chkBoard(score): #kill full lines and increase score
    for i in range(17):
        if all([chr(win.inch(i,x)) == 'X' for x in range(1,17)]):
            win.deleteln()
            win.move(1,1)
            win.insertln()
            score = score + 1
            if score % 10 == 0: win.timeout(300-(score*2))
    return score
def control(key):
	return key
FigPos = [8,3,0,randrange(0,6,1)] # x,y,rotation,figure
score = putFig(FigPos,1) ^ 1 
win.timeout(300) 
while 1: # main loop
    win.border('|','|','-','-','+','+','+','+')  
    win.addstr(0,2,' Score: '+str(score)+' ')
    key = control()
    if key == 27: break
    putFig(FigPos,0) 
    MoveFig(FigPos,key,1)
    if not putFig(FigPos,1):
        MoveFig(FigPos,key, -1)
        putFig(FigPos,1)
        if FigPos[1]==3: break
        if key in [curses.KEY_DOWN,-1]:
            score = chkBoard(score)
            FigPos = [8,3,0,randrange(0,6,1)]
            putFig(FigPos,1)
curses.endwin() # back to console
print '\n  Tetris-50l (by Kris Cieslak),\n  Thanks for playing, your score: '+str(score)+'\n'

"""
TETRIS-50lines by Kris Cieslak (defaultset.blogspot.com)

Controls:  Left,Right,Up,Down - move/rotate
           ESC -quit         

Linux/python 2.6.5
"""

