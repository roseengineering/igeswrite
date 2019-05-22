#!/usr/bin/python3

from igeswrite import Iges
import numpy as np

iges = Iges()

iges.yslabline(10, .2, (10, 0, 0))
iges.xslabline(10, .2, (0,  -1, 0))

# write result
iges.write("slabline.igs")

