#!/usr/bin/python

# Copyright (c) 2010, Andrej Bauer, http://andrej.com/
# Copyright (c) 2018, Yaroslav Zotov, https://github.com/qiray/
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import random
import math
from common import (average, well, tent, parse_color, sin_curve, abs_sin, 
    color_binary, wave)
from palettes import palettes

# We next define classes that represent expression trees.

# Each object that reprents and expression should have an eval(self,x, y) method
# which computes the value of the expression at (x, y). The __init__ should
# accept the objects representing its subexpressions. The class definition
# should contain the arity attribute which tells how many subexpressions should
# be passed to the __init__ constructor. Classes with arity == 0 are called 
# terminals, the others are called nonterminals.The __repr__ method is used to 
# print each object as a string. The mindepth attribute shows depth of 
# expression tree where it is allowed to use this object.

# Some operators are copied from https://github.com/vshymanskyy/randomart

# Terminals:

class VariableX():
    arity = 0
    mindepth = 4
    def __init__(self):
        pass
    def __repr__(self):
        return "x"
    def eval(self, x, y):
        return (x, x, x)

class VariableY():
    arity = 0
    mindepth = 4
    def __init__(self):
        pass
    def __repr__(self):
        return "y"
    def eval(self, x, y):
        return (y, y, y)

class Random():
    arity = 0
    mindepth = 4
    def __init__(self, r = None, g = None, b = None):
        if r and g and b: #for parsing
            self.c = (r, g, b)
            return
        self.c = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
    def __repr__(self):
        return 'Random(%g,%g,%g)' % self.c
    def eval(self, x, y): 
        return self.c

class Palette():
    arity = 0
    mindepth = 3
    palette = palettes[0]
    paletteIndex = 0
    def __init__(self, r = None, g = None, b = None):
        if r and g and b: #for parsing
            self.c = (r, g, b)
            return
        self.hex = Palette.palette[Palette.paletteIndex]
        Palette.paletteIndex += 1
        if Palette.paletteIndex >= len(Palette.palette):
            Palette.paletteIndex = 0
        self.c = tuple([x/128.0 - 1.0 for x in parse_color(self.hex)])
    def __repr__(self):
        return "Palette(%g, %g, %g)" % self.c
    def eval(self, x, y):
        return self.c

    @staticmethod
    def randomPalette(): #set random palette
        Palette.palette = random.choice(palettes)
        Palette.paletteIndex = 0

class White():
    arity = 0
    mindepth = 4
    def __init__(self, r = None, g = None, b = None): #unused arguments for parsing
        self.c = (1, 1, 1)
    def __repr__(self):
        return 'White(%g, %g, %g)' % self.c
    def eval(self,x, y): 
        return self.c

class Chess():
    arity = 0
    mindepth = 5
    def __init__(self, wX = None, wY = None):
        if wX and wY: #for parsing
            self.wX = wX
            self.wY = wY
        self.wX = random.uniform(0.1, 1.0)
        self.wY = random.uniform(0.1, 1.0)
    def __repr__(self):
        return "Chess(%g, %g)" % (self.wX, self.wY)
    def eval(self, x, y):
        isOdd = False
        isOdd ^= math.floor(x/self.wX) & 1
        isOdd ^= math.floor(y/self.wY) & 1
        return (-1, -1, -1) if isOdd else (1, 1, 1)

# Nonterminals:

class Well():
    arity = 1
    mindepth = 3
    def __init__(self, e):
        self.e = e
    def __repr__(self):
        return 'Well(%s)' % self.e
    def eval(self,x, y):
        (r,g,b) = self.e.eval(x, y)
        return (well(r), well(g), well(b))

class Tent():
    arity = 1
    mindepth = 3
    def __init__(self, e):
        self.e = e
    def __repr__(self):
        return 'Tent(%s)' % self.e
    def eval(self,x, y):
        (r,g,b) = self.e.eval(x, y)
        return (tent(r), tent(g), tent(b))

class Sin():
    arity = 1
    mindepth = 0
    def __init__(self, e, phase = None, freq = None):
        self.e = e
        if phase and freq: #for parsing
            self.phase = phase
            self.freq = freq
            return
        self.phase = random.uniform(0, math.pi)
        self.freq = random.uniform(1.0, 6.0)
    def __repr__(self):
        return 'Sin(%g, %g, %s)' % (self.phase, self.freq, self.e)
    def eval(self,x, y):
        (r1,g1,b1) = self.e.eval(x, y)
        r2 = math.sin(self.phase + self.freq * r1)
        g2 = math.sin(self.phase + self.freq * g1)
        b2 = math.sin(self.phase + self.freq * b1)
        return (r2,g2,b2)

class Not():
    arity = 1
    mindepth = 3
    def __init__(self, e):
        self.e = e
    def __repr__(self):
        return "Not(%s)" % self.e
    def eval(self, x, y):
        (r, g, b) = self.e.eval(x, y)
        return (-r, -g, -b)

class SinCurve():
    arity = 1
    mindepth = 0
    def __init__(self, e):
        self.e = e
    def __repr__(self):
        return 'SinCurve(%s)' % self.e
    def eval(self,x, y):
        (r,g,b) = self.e.eval(x, y)
        return (sin_curve(r), sin_curve(g), sin_curve(b))

class AbsSin():
    arity = 1
    mindepth = 3
    def __init__(self, e):
        self.e = e
    def __repr__(self):
        return 'AbsSin(%s)' % self.e
    def eval(self,x, y):
        (r,g,b) = self.e.eval(x, y)
        return (abs_sin(r), abs_sin(g), abs_sin(b))

class Atan():
    arity = 1
    mindepth = 0
    def __init__(self, e):
        self.e = e
    def __repr__(self):
        return 'Atan(%s)' % (self.e)
    def eval(self, x, y):
        (r,g,b) = self.e.eval(x, y)
        return (math.atan(r)*2/math.pi, math.atan(g)*2/math.pi, math.atan(b)*2/math.pi)

class Sum():
    arity = 2
    mindepth = 2
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return 'Sum(%s, %s)' % (self.e1, self.e2)
    def eval(self, x, y):
        return average(self.e1.eval(x, y), self.e2.eval(x, y))

class Product():
    arity = 2
    mindepth = 2
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return 'Product(%s, %s)' % (self.e1, self.e2)
    def eval(self,x, y):
        (r1, g1, b1) = self.e1.eval(x, y)
        (r2, g2, b2) = self.e2.eval(x, y)
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
    def eval(self, x, y):
        (r1, g1, b1) = self.e1.eval(x, y)
        (r2, g2, b2) = self.e2.eval(x, y)
        try:
            r3 = r1 % r2
            g3 = g1 % g2
            b3 = b1 % b2
            return (r3, g3, b3)
        except:
            return (0, 0, 0)

class And():
    arity = 2
    mindepth = 0
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return 'And(%s, %s)' % (self.e1, self.e2)
    def eval(self, x, y):
        return color_binary(self.e1.eval(x, y), self.e2.eval(x, y), lambda x1, x2 : x1 & x2)

class Or():
    arity = 2
    mindepth = 0
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return 'Or(%s, %s)' % (self.e1, self.e2)
    def eval(self, x, y):
        return color_binary(self.e1.eval(x, y), self.e2.eval(x, y), lambda x1, x2 : x1 | x2)

class Xor():
    arity = 2
    mindepth = 0
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return 'Xor(%s, %s)' % (self.e1, self.e2)
    def eval(self, x, y):
        return color_binary(self.e1.eval(x, y), self.e2.eval(x, y), lambda x1, x2 : x1 ^ x2)

class Wave():
    arity = 2
    mindepth = 0
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return 'Wave(%s, %s)' % (self.e1, self.e2)
    def eval(self, x, y):
        (r1,g1,b1) = self.e1.eval(x, y)
        (r2,g2,b2) = self.e2.eval(x, y)
        return (wave(r1, r2), wave(g1, g2), wave(b1, b2))

class Level():
    arity = 3
    mindepth = 0
    def __init__(self, level, e1, e2, treshold = None):
        self.treshold = treshold if treshold else random.uniform(-1.0,1.0) #for parsing
        self.level = level
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return 'Level(%g, %s, %s, %s)' % (self.treshold, self.level, self.e1, self.e2)
    def eval(self,x, y):
        (r1, g1, b1) = self.level.eval(x, y)
        (r2, g2, b2) = self.e1.eval(x, y)
        (r3, g3, b3) = self.e2.eval(x, y)
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
    def eval(self,x, y):
        w = 0.5 * (self.w.eval(x, y)[0] + 1.0)
        c1 = self.e1.eval(x, y)
        c2 = self.e2.eval(x, y)
        return average(c1,c2,w)

class RGB():
    arity = 3
    mindepth = 4
    def __init__(self, e1, e2, e3):
        self.e1 = e1
        self.e2 = e2
        self.e3 = e3
    def __repr__(self):
        return 'RGB(%s, %s, %s)' % (self.e1, self.e2, self.e3)
    def eval(self, x, y):
        (r, _, _) = self.e1.eval(x, y)
        (_, g, _) = self.e2.eval(x, y)
        (_, _, b) = self.e3.eval(x, y)
        return (r, g, b)

class Closest():
    arity = 3
    mindepth = 3
    def __init__(self, target, e1, e2):
        self.target = target
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return 'Closest(%s, %s, %s)' % (self.target, self.e1, self.e2)
    def eval(self, x, y):
        (r1, g1, b1) = self.target.eval(x, y)
        (r2, g2, b2) = self.e1.eval(x, y)
        (r3, g3, b3) = self.e2.eval(x, y)
        #distances between colors:
        d1 = math.sqrt((r2-r1)**2+(g2-g1)**2+(b2-b1)**2)
        d2 = math.sqrt((r3-r1)**2+(g3-g1)**2+(b3-b1)**2)

        return (r2, g2, b2) if d1 < d2 else (r3, g3, b3)

class Far():
    arity = 3
    mindepth = 3
    def __init__(self, target, e1, e2):
        self.target = target
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return 'Far(%s, %s, %s)' % (self.target, self.e1, self.e2)
    def eval(self, x, y):
        (r1, g1, b1) = self.target.eval(x, y)
        (r2, g2, b2) = self.e1.eval(x, y)
        (r3, g3, b3) = self.e2.eval(x, y)
        #distances between colors:
        d1 = math.sqrt((r2-r1)**2+(g2-g1)**2+(b2-b1)**2)
        d2 = math.sqrt((r3-r1)**2+(g3-g1)**2+(b3-b1)**2)

        return (r2, g2, b2) if d1 > d2 else (r3, g3, b3)
