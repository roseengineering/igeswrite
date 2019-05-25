
import sys, math

def hollerith(s):
    return "{}H{}".format(len(s), s)


class Iges:

    def __init__(self):
        self.buffer = { 'D':"", 'P':"" }
        self.lineno= { 'D':0, 'P':0 }

    def add_line(self, section, line, index=""):
        index = str(index)
        self.lineno[section] += 1
        lineno = self.lineno[section]
        buf = "{:64s}{:>8s}{}{:7d}\n".format(line, index, section, lineno)
        self.buffer[section] += buf

    def update(self, section, params, index=""):
        line = None
        for s in params:
            s = str(s)
            if line is None:
                line = s
            elif len(line + s) + 1 < 64:
                line += "," + s
            else:
                self.add_line(section, line + ',', index=index)
                line = s
        self.add_line(section, line + ';', index=index)

    def start_section(self, comment=""):
        self.buffer["S"] = ""
        self.lineno["S"] = 0
        self.update("S", [comment])

    def global_section(self, filename=""):
        self.buffer["G"] = ""
        self.lineno["G"] = 0
        self.update("G", [
            "1H,",       # 1  parameter delimiter 
            "1H;",       # 2  record delimiter 
            "6HNoname",  # 3  product id of sending system
            hollerith(filename),  # 4  file name
            "6HNoname",  # 5  native system id
            "6HNoname",  # 6  preprocessor system  
            "32",        # 7  binary bits for integer
            "38",        # 8  max power represented by float
            "6",         # 9  number of significant digits in float
            "308",       # 10 max power represented in double
            "15",        # 11 number of significant digits in double
            "6HNoname",  # 12 product id of receiving system
            "1.00",      # 13 model space scale
            "6",         # 14 units flag (2=mm, 6=m)
            "1HM",       # 15 units name (2HMM)
            "1",         # 16 number of line weight graduations
            "1.00",      # 17 width of max line weight
            "15H20181210.181412",  # 18 file generation time
            "1.0e-006",  # 19 min resolution
            "0.00",      # 20 max coordinate value
            "6HNoname",  # 21 author
            "6HNoname",  # 22 organization
            "11",        # 23 specification version
            "0",         # 24 drafting standard
            "15H20181210.181412",  # 25 time model was created
        ])

    def entity(self, code, params, label="", child=False):
        code = str(code)
        status = "00010001" if child else "1"
        dline = self.lineno["D"] + 1
        pline = self.lineno["P"] + 1
        self.buffer['D'] += (
            "{:>8s}{:8d}{:8d}{:8d}{:8d}{:8d}{:8d}{:8d}{:>8s}D{:7d}\n".format(
            code, pline, 0, 0, 0, 0, 0, 0, status, dline) +
            "{:>8s}{:8d}{:8d}{:8d}{:8d}{:8d}{:8d}{:8s}{:8d}D{:7d}\n".format(
            code, 1, 0, 1, 0, 0, 0, label, 0, dline + 1))
        self.update("P", [code] + list(params), index=dline)
        self.lineno["D"] = dline + 1
        return dline

    def pos(self, pt, origin):
        x, y, z = origin
        return (pt[0] + x, pt[1] + y, + pt[2] + z)

    def origin(self, size, origin, centerx=False, centery=False):
        w, h = size
        x, y, z = origin
        if centerx: x -= w / 2
        if centery: y -= h / 2
        return x, y, z

    def mapping(self, points, origin):
        start = points[-1]
        refs = []
        for p in points:
            refs.append(self.line(start, p, origin, child=True))
            start = p
        return self.entity(102, [len(refs)] + refs, child=True) 

    def surface(self, directrix, vector, points, origin):
        surface = self.entity(122, [directrix] + list(vector), child=True)
        mapping = self.mapping(points, origin)
        curve = self.entity(142, [1, surface, 0, mapping, 2], child=True)
        self.entity(144, [surface, 1, 0, curve])

    def cylinder(self, directrix, vector, origin):
        self.entity(120, [directrix, vector, 0, 2 * math.pi])

    ################

    def write(self, filename=None):
        self.start_section()
        self.global_section(filename)
        f = open(filename, "w") if filename else sys.stdout
        f.write(self.buffer['S'])
        f.write(self.buffer['G'])
        f.write(self.buffer['D'])
        f.write(self.buffer['P'])
        f.write("S{:7d}G{:7d}D{:7d}P{:7d}{:40s}T{:7d}\n".format(
            self.lineno['S'], self.lineno['G'], 
            self.lineno['D'], self.lineno['P'], "", 1))
        if filename: f.close()

    def line(self, start, end, origin=(0,0,0), child=False):
        start = self.pos(start, origin)
        end = self.pos(end, origin)
        return self.entity(110, start + end, child=child)

    def xzplane(self, size, origin=(0,0,0)):
        w, h = size
        x, y, z = origin
        points = [(w, 0, 0), (w, 0, h), (0, 0, h), (0, 0, 0)]
        directrix = self.line((0, 0, 0), (w, 0, 0), origin, child=True)
        self.surface(directrix, (x, y, z + h), points, origin)

    def yzplane(self, size, origin=(0,0,0)):
        w, h = size
        x, y, z = origin
        points = [(0, w, 0), (0, w, h), (0, 0, h), (0, 0, 0)]
        directrix = self.line((0, 0, 0), (0, w, 0), origin, child=True)
        self.surface(directrix, (x, y, z + h), points, origin)

    def plane(self, size, origin=(0,0,0), **kw):
        w, h = size
        x, y, z = origin = self.origin(size, origin, **kw)
        points = [(w, 0, 0), (w, h, 0), (0, h, 0), (0, 0, 0)]
        directrix = self.line((0, 0, 0), (w, 0, 0), origin, child=True)
        self.surface(directrix, (x, y + h, z), points, origin)

    def wedge(self, w, h, origin=(0,0,0), flipx=False):
        x, y, z = origin
        if flipx: w, x = -w, x + w
        origin = x, y, z
        points = [(0, 0, 0), (w, 0, 0), (w, h, 0)]
        directrix = self.line((0, 0, 0), (w, 0, 0), origin, child=True)
        self.surface(directrix, (x, y + h, z), points, origin)

    def cube(self, size, origin=(0,0,0)):
        w, l, h = size
        x, y, z = origin
        self.plane((w, l), origin=origin)
        self.plane((w, l), origin=(x, y, z + h))
        self.yzplane((l, h), origin=origin)
        self.yzplane((l, h), origin=(x + w, y, z))
        self.xzplane((w, h), origin=origin)
        self.xzplane((w, h), origin=(x, y + l, z))

    def yslabline(self, length, rad, origin=(0,0,0)):
        directrix = self.line((0, 0, 0), (0, 1, 0), origin, child=True)
        vector = self.line((0, 0, 0), (0, 0, rad), origin, child=True)
        self.cylinder(directrix, vector, origin)
        vector = self.line((0, length, 0), (0, length, rad), origin, child=True)
        self.cylinder(directrix, vector, origin)
        vector = self.line((0, 0, rad), (0, length, rad), origin, child=True)
        self.cylinder(directrix, vector, origin)

    def xslabline(self, length, rad, origin=(0,0,0)):
        directrix = self.line((0, 0, 0), (1, 0, 0), origin, child=True)
        vector = self.line((0, 0, 0), (0, 0, rad), origin, child=True)
        self.cylinder(directrix, vector, origin)
        vector = self.line((length, 0, 0), (length, 0, rad), origin, child=True)
        self.cylinder(directrix, vector, origin)
        vector = self.line((0, 0, rad), (length, 0, rad), origin, child=True)
        self.cylinder(directrix, vector, origin)



