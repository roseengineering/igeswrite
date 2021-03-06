#!/usr/bin/python3

from igeswrite import Iges

iges = Iges()
bw = 50
bl = 100
zw = 3.0
h = 1.6
d = .5

cx = bw / 2
cy = bl / 2

# transmission line
iges.plane((zw, bl - 2 * d), origin=(-zw/2, -cy + d, 0))

# port 1
iges.xzplane((zw, -h/2), origin=(-zw/2, -cy + d, 0))
iges.xzplane((zw, -h/2), origin=(-zw/2, -cy + d, -h/2))

# port 2
iges.xzplane((zw, -h/2), origin=(-zw/2, cy - d, 0))
iges.xzplane((zw, -h/2), origin=(-zw/2, cy - d, -h/2))

# region and ground plane
iges.cube((bw, bl, -h), origin=(-cx, -cy, 0))

# write result
iges.write("microstrip.igs")

