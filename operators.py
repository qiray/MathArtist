#!/usr/bin/python

# We next define classes that represent expression trees.

# Each object that reprents and expression should have an eval(self,x,y) method
# which computes the value of the expression at (x,y). The __init__ should
# accept the objects representing its subexpressions. The class definition
# should contain the arity attribute which tells how many subexpressions should
# be passed to the __init__ constructor.

import random
import math
from common import average, well, tent, parse_color, invert
from palettes import palettes

class VariableX():
    arity = 0
    mindepth = 4
    def __init__(self): pass
    def __repr__(self): return "x"

    def eval(self,x,y): return (x,x,x)

class VariableY():
    arity = 0
    mindepth = 4
    def __init__(self): pass
    def __repr__(self): return "y"
    def eval(self,x,y): return (y,y,y)

class Random():
    arity = 0
    mindepth = 4
    def __init__(self):
        self.c = (random.uniform(0,1), random.uniform(0,1), random.uniform(0,1))
    def __repr__(self):
        return 'Random(%g,%g,%g)' % self.c
    def eval(self,x,y): 
        return self.c

class Sum():
    arity = 2
    mindepth = 2
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return 'Sum(%s, %s)' % (self.e1, self.e2)
    def eval(self,x,y):
        return average(self.e1.eval(x,y), self.e2.eval(x,y))

class Product():
    arity = 2
    mindepth = 2
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return 'Product(%s, %s)' % (self.e1, self.e2)
    def eval(self,x,y):
        (r1,g1,b1) = self.e1.eval(x,y)
        (r2,g2,b2) = self.e2.eval(x,y)
        r3 = r1 * r2
        g3 = g1 * g2
        b3 = b1 * b2
        return (r3, g3, b3)

class Mod():
    arity = 2
    mindepth = 3
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return 'Mod(%s, %s)' % (self.e1, self.e2)
    def eval(self,x,y):
        (r1,g1,b1) = self.e1.eval(x,y)
        (r2,g2,b2) = self.e2.eval(x,y)
        try:
            r3 = r1 % r2
            g3 = g1 % g2
            b3 = b1 % b2
            return (r3, g3, b3)
        except:
            return (0,0,0)

class Well():
    arity = 1
    mindepth = 3
    def __init__(self, e):
        self.e = e
    def __repr__(self):
        return 'Well(%s)' % self.e
    def eval(self,x,y):
        (r,g,b) = self.e.eval(x,y)
        return (well(r), well(g), well(b))

class Tent():
    arity = 1
    mindepth = 3
    def __init__(self, e):
        self.e = e
    def __repr__(self):
        return 'Tent(%s)' % self.e
    def eval(self,x,y):
        (r,g,b) = self.e.eval(x,y)
        return (tent(r), tent(g), tent(b))

class Sin():
    arity = 1
    mindepth = 0
    def __init__(self, e):
        self.e = e
        self.phase = random.uniform(0, math.pi)
        self.freq = random.uniform(1.0, 6.0)
    def __repr__(self):
        return 'Sin(%g + %g * %s)' % (self.phase, self.freq, self.e)
    def eval(self,x,y):
        (r1,g1,b1) = self.e.eval(x,y)
        r2 = math.sin(self.phase + self.freq * r1)
        g2 = math.sin(self.phase + self.freq * g1)
        b2 = math.sin(self.phase + self.freq * b1)
        return (r2,g2,b2)

class Level():
    arity = 3
    mindepth = 0
    def __init__(self, level, e1, e2):
        self.treshold = random.uniform(-1.0,1.0)
        self.level = level
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return 'Level(%g, %s, %s, %s)' % (self.treshold, self.level, self.e1, self.e2)
    def eval(self,x,y):
        (r1, g1, b1) = self.level.eval(x,y)
        (r2, g2, b2) = self.e1.eval(x,y)
        (r3, g3, b3) = self.e2.eval(x,y)
        r4 = r2 if r1 < self.treshold else r3
        g4 = g2 if g1 < self.treshold else g3
        b4 = b2 if b1 < self.treshold else b3
        return (r4,g4,b4)

class Mix():
    arity = 3
    mindepth = 0
    def __init__(self, w, e1, e2):
        self.w = w
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return 'Mix(%s, %s, %s)' % (self.w, self.e1, self.e2)
    def eval(self,x,y):
        w = 0.5 * (self.w.eval(x,y)[0] + 1.0)
        c1 = self.e1.eval(x,y)
        c2 = self.e2.eval(x,y)
        return average(c1,c2,w)

class Palette():
    arity = 0
    mindepth = 3
    palette = palettes[0]
    paletteIndex = 0
    def __init__(self):
        self.hex = Palette.palette[Palette.paletteIndex]
        Palette.paletteIndex += 1
        if Palette.paletteIndex >= len(Palette.palette):
            Palette.paletteIndex = 0
        self.c = tuple([x/128.0 - 1.0 for x in parse_color(self.hex)])
    def __repr__(self):
        return "Const(%g, %g, %g)" % self.c
    def eval(self, x, y):
        return self.c

    @staticmethod
    def randomPalette(): #set random palette
        Palette.palette = random.choice(palettes)
        Palette.paletteIndex = 0

class Not():
    arity = 1
    mindepth = 3
    def __init__(self, e):
        self.e = e
    def __repr__(self):
        return "Not(%s)" % self.e
    def eval(self, x, y):
        c = self.e.eval(x, y)
        return invert(c)

# class CVarT {
#     static get arity() { return 0 }
#     static get mindepth() { return 4 }

#     constructor() {
#     }
#     toString() {
#         return "frmT";
#     }
# }

# class CBW {
#     static get arity() { return 0 }
#     static get mindepth() { return 4 }

#     constructor() {
#         this.c = random.uniform(-0.8, 0.8);
#     }
#     toString() {
#         return `BW(${fixStr(this.c)})`;
#     }
# }

# class CRandom {
#     static get arity() { return 0 }
#     static get mindepth() { return 4 }

#     constructor() {
#         this.c = [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)];
#     }
#     toString() {
#         return `Const(${fixStr(this.c[0])}, ${fixStr(this.c[1])}, ${fixStr(this.c[2])})`;
#     }
# }

# /*
#  * Mixers
#  */

# class CRGB {
#     static get arity() { return 3 }
#     static get mindepth() { return 4 }

#     constructor(e1,e2,e3) {
#         this.e1 = e1;
#         this.e2 = e2;
#         this.e3 = e3;
#     }
#     toString() {
#         return `RGB(${this.e1}, ${this.e2}, ${this.e3})`;
#     }
# }

# /*
# class CChBoard {
#     static get arity() { return 0 }
#     static get mindepth() { return 5 }

#     constructor(e1, e2) {
#         this.wX = random.uniform(0.1, 1.0);
#         this.wY = random.uniform(0.1, 1.0);
#     }
#     toString() {
#         return `ChBoard()`;
#     }
#     eval(x, y) {
#         let isOdd = false;
#         isOdd ^= Math.floor(x/this.wX) & 1;
#         isOdd ^= Math.floor(y/this.wY) & 1;

#         return (isOdd) ? [-1,-1,-1] : [1,1,1];
#     }
# }

# class CTurbulence {
#     static get arity() { return 1 }
#     static get mindepth() { return 2 }

#     constructor(e) {
#         this.e = e;

#         this.octaves = random.randrange(3, 6);
#         this.freq = random.uniform(0.1, 4);
#         this.ampl = random.uniform(0.1, 5);
#     }
#     toString() {
#         return `Turbulence(${this.e})`;
#     }
#     eval(x, y) {
#         let r = 0, g = 0, b = 0;
#         let amp = this.ampl;

#         x *= this.freq;
#         y *= this.freq;

#         for (let i=0; i<this.octaves; i++) {
#             let r0, g0, b0;
#             [r0, g0, b0] = this.e.eval(x, y);
#             r += r0 * amp;
#             g += g0 * amp;
#             b += b0 * amp;
#             x *= 2.0;
#             y *= 2.0;
#             amp *= 0.5;
#         }
#         return [r, g, b];
#     }
# }
# */

# class CClosest {
#     static get arity() { return 3 }
#     static get mindepth() { return 3 }

#     constructor(tgt, e1, e2) {
#         this.tgt = tgt;
#         this.e1 = e1;
#         this.e2 = e2;
#     }
#     toString() {
#         return `Closest(${this.tgt}, ${this.e1}, ${this.e2})`;
#     }
# }