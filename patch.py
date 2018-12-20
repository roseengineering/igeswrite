#!/usr/bin/python3

from igeswrite import Iges

bw = 100
bl = 80
h = 1.6
l = 29.2   # length of patch
w = 50.8   # width of patch
dw = 1.3   # width of quarter wave line
dl = 18    # length of quarter wave line
zw = 3.0   # width of 50 ohm line
de = 0.5   # offset from edge

cx = bw / 2
cy = bl / 2
ext = h * .44 * (1 - dw / zw) 

# board
iges = Iges()
iges.cube(bw, bl, -h, origin=(-cx, -cy, 0))

# patch
iges.plane(w, l, origin=(-w/2, -l/2, 0))

# transmission line
d0 = l/2 + dl + ext
d1 = cy - de
iges.plane(dw, dl + ext, origin=(-dw/2, -d0, 0))
iges.plane(zw, d1 - d0, origin=(-zw/2, -d1, 0))

# port
iges.xzplane(zw, -h/2, origin=(-zw/2, -d1, 0))
iges.xzplane(zw, -h/2, origin=(-zw/2, -d1, -h/2))

# write result
iges.write("patch.igs")

