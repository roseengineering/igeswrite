
import sys
from boardsvg import Board
from igeswrite import Iges

bh = 100        # 103
bw = 80         # 78
cx = bw / 2
cy = bh / 2
er = 4.2        # loss tangent is .017
h = 1.6         # height of the board
w, l = 30, 27.5 # length and width of patch
zw = 3.1        # width of 50 ohm line
zl = 34.5       # halfwave (before I used 34.25)

# info
line = -l / 2  
line += 25
sd = 25   # 22
sl = 9   # 11.5

board = Board()
iges = Iges()

board.initialize(size=(bw, bh), viewport=(-cx, -cy), rotate=True)
iges.cube((bw, bh, -h), origin=(-cx, -cy, 0))

# patch
iges.plane((w, l), origin=(0, line, 0), centerx=True)
board.rect((w, l), origin=(0, line), centerx=True)

# 50 ohm line
line -= sd
iges.plane((zw, sd), origin=(0, line, 0), centerx=True)
board.rect((zw, sd), origin=(0, line), centerx=True)    

# stub match
iges.plane((sl, zw), origin=(zw / 2, line, 0), centery=True) 
board.rect((sl, zw), origin=(zw / 2, line), centery=True) 

# feed line
line -= zl
if line + cy < 0.5: raise ValueError 
iges.plane((zw, zl), origin=(0, line, 0), centerx=True)    
board.rect((zw, zl), origin=(0, line), centerx=True)    
board.write("stub.svg")

# port
iges.xzplane((zw, -h/2), origin=(-zw/2, line, 0))
iges.xzplane((zw, -h/2), origin=(-zw/2, line, -h/2))
iges.write("stub.igs")

