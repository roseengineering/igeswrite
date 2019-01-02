
import sys
import svgwrite

class Board:

    def pos(self, pos, origin=(0, 0)):
        k = 3.779527559
        vx, vy = self.viewport
        x = pos[0] + origin[0] - vx
        y = pos[1] + origin[1] - vy
        if self.flip: y = self.size[1] - y
        if self.rotate: x, y = y, x
        return (k * x, k * y)

    def __init__(self, **kw):
        self.initialize(**kw)

    ############

    def initialize(self, viewport=(0,0), size=(100,100), flip=False, rotate=False):
        w, h = size
        self.dwg = svgwrite.Drawing(profile='tiny')
        self.flip = flip
        self.rotate = rotate
        self.size = size
        self.viewport = viewport
        if rotate: w, h = h, w
        self.dwg['width'] = w * svgwrite.mm
        self.dwg['height'] = h * svgwrite.mm

    def rect(self, size, origin=(0,0), **kw):
        w, h = size
        self.poly([(0, 0), (w, 0), (w, h), (0, h)], origin)

    def poly(self, points, origin=(0,0), **kw):
        points = map(lambda x: self.pos(x, origin), points)
        el = self.dwg.polygon(points)
        self.dwg.add(el)

    def write(self, filename=None, pretty=True):
        f = open(filename, "w") if filename else sys.stdout
        self.dwg.write(f, pretty=pretty)
        if filename: f.close()


