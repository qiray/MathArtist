
# Copyright (c) 2018, Yaroslav Zotov, https://github.com/qiray/
# All rights reserved.

# This file is part of MathArtist.

# MathArtist is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# MathArtist is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with MathArtist.  If not, see <https://www.gnu.org/licenses/>.

################################################################################

# This file uses code from Andrej Bauer's randomart project under 
# following conditions:

# Copyright (c) 2010, Andrej Bauer, http://andrej.com/
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

# cython: language_level=3

import random
import math

cimport libc.math as cmath

from common import (average, well, tent, parse_color, sin_curve, abs_sin,
    color_binary, wave)
from palettes import palettes

# We next define classes that represent expression trees.

# Each object that reprents and expression should have an eval(self, x, y) method
# which computes the value of the expression at (x, y). The __init__ should
# accept the objects representing its subexpressions. The class definition
# should contain the arity attribute which tells how many subexpressions should
# be passed to the __init__ constructor. Classes with arity == 0 are called
# terminals, the others are called nonterminals.The __repr__ method is used to
# print each object as a string. The mindepth attribute shows depth of
# expression tree where it is allowed to use this object.

# Some operators are adopted from https://github.com/vshymanskyy/randomart

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
    def eval(self, x, y):
        return self.c

class Chess():
    arity = 0
    mindepth = 5
    def __init__(self, wX=None, wY=None):
        if wX and wY: #for parsing
            self.wX = wX
            self.wY = wY
            return
        self.wX = random.uniform(0.1, 1.0)
        self.wY = random.uniform(0.1, 1.0)
    def __repr__(self):
        return "Chess(%g, %g)" % (self.wX, self.wY)
    def eval(self, x, y):
        isOdd = False
        isOdd ^= int(cmath.floor(x/self.wX)) & 1
        isOdd ^= int(cmath.floor(y/self.wY)) & 1
        return (-1, -1, -1) if isOdd else (1, 1, 1)

class Fibonacci():
    arity = 0
    mindepth = 3
    fib_array = [0, 1]
    def __init__(self):
        pass
    def __repr__(self):
        return "Fibonacci()"
    def eval(self, x, y):
        result = (self.fibonacci(len(Fibonacci.fib_array) + 1)%255)/255 - 128
        return (result, result, result)
    def fibonacci(self, n):
        if n < 0:
            return Fibonacci.fib_array[0]
        elif n < len(Fibonacci.fib_array):
            return Fibonacci.fib_array[n]
        else:
            max_limit = 200 if n > 200 else n + 1
            for i in range(len(Fibonacci.fib_array), max_limit): 
                Fibonacci.fib_array.append(Fibonacci.fib_array[i - 1] + Fibonacci.fib_array[i - 2])
            return Fibonacci.fib_array[max_limit - 1]

# Nonterminals:

class Well():
    arity = 1
    mindepth = 3
    def __init__(self, e):
        self.e = e
        self.e_func = self.e.eval
    def __repr__(self):
        return 'Well(%s)' % self.e
    def eval(self, x, y):
        (r, g, b) = self.e_func(x, y)
        return (well(r), well(g), well(b))

class Tent():
    arity = 1
    mindepth = 3
    def __init__(self, e):
        self.e = e
        self.e_func = self.e.eval
    def __repr__(self):
        return 'Tent(%s)' % self.e
    def eval(self, x, y):
        (r, g, b) = self.e_func(x, y)
        return (tent(r), tent(g), tent(b))

class Sin():
    arity = 1
    mindepth = 0
    def __init__(self, e, phase = None, freq = None):
        self.e = e
        self.e_func = self.e.eval
        if phase and freq: #for parsing
            self.phase = phase
            self.freq = freq
            return
        self.phase = random.uniform(0, math.pi)
        self.freq = random.uniform(1.0, 6.0)
    def __repr__(self):
        return 'Sin(%s, %g, %g)' % (self.e, self.phase, self.freq)
    def eval(self, x, y):
        (r1, g1, b1) = self.e_func(x, y)
        r2 = cmath.sin(self.phase + self.freq * r1)
        g2 = cmath.sin(self.phase + self.freq * g1)
        b2 = cmath.sin(self.phase + self.freq * b1)
        return (r2, g2, b2)

class Not():
    arity = 1
    mindepth = 3
    def __init__(self, e):
        self.e = e
        self.e_func = self.e.eval
    def __repr__(self):
        return "Not(%s)" % self.e
    def eval(self, x, y):
        (r, g, b) = self.e_func(x, y)
        return (-r, -g, -b)

class SinCurve():
    arity = 1
    mindepth = 0
    def __init__(self, e):
        self.e = e
        self.e_func = self.e.eval
    def __repr__(self):
        return 'SinCurve(%s)' % self.e
    def eval(self, x, y):
        (r, g, b) = self.e_func(x, y)
        return (sin_curve(r), sin_curve(g), sin_curve(b))

class AbsSin():
    arity = 1
    mindepth = 3
    def __init__(self, e):
        self.e = e
        self.e_func = self.e.eval
    def __repr__(self):
        return 'AbsSin(%s)' % self.e
    def eval(self, x, y):
        (r, g, b) = self.e_func(x, y)
        return (abs_sin(r), abs_sin(g), abs_sin(b))

class Atan():
    arity = 1
    mindepth = 0
    def __init__(self, e):
        self.e = e
        self.e_func = self.e.eval
    def __repr__(self):
        return 'Atan(%s)' % (self.e)
    def eval(self, x, y):
        (r, g, b) = self.e_func(x, y)
        return (cmath.atan(r)*2/cmath.pi, cmath.atan(g)*2/cmath.pi, cmath.atan(b)*2/cmath.pi)

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
    def eval(self, x, y):
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
        return color_binary(self.e1.eval(x, y), self.e2.eval(x, y), lambda x1,x2 : x1 & x2)

class Or():
    arity = 2
    mindepth = 0
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return 'Or(%s, %s)' % (self.e1, self.e2)
    def eval(self, x, y):
        return color_binary(self.e1.eval(x, y), self.e2.eval(x, y), lambda x1,x2 : x1 | x2)

class Xor():
    arity = 2
    mindepth = 0
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return 'Xor(%s, %s)' % (self.e1, self.e2)
    def eval(self, x, y):
        return color_binary(self.e1.eval(x, y), self.e2.eval(x, y), lambda x1,x2 : x1 ^ x2)

class Wave():
    arity = 2
    mindepth = 0
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return 'Wave(%s, %s)' % (self.e1, self.e2)
    def eval(self, x, y):
        (r1, g1, b1) = self.e1.eval(x, y)
        (r2, g2, b2) = self.e2.eval(x, y)
        return (wave(r1, r2), wave(g1, g2), wave(b1, b2))

class Level():
    arity = 3
    mindepth = 0
    def __init__(self, level, e1, e2, treshold = None):
        self.treshold = treshold if treshold else random.uniform(-1.0, 1.0) #for parsing
        self.level = level
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return 'Level(%s, %s, %s, %g)' % (self.level, self.e1, self.e2, self.treshold)
    def eval(self, x, y):
        (r1, g1, b1) = self.level.eval(x, y)
        (r2, g2, b2) = self.e1.eval(x, y)
        (r3, g3, b3) = self.e2.eval(x, y)
        r4 = r2 if r1 < self.treshold else r3
        g4 = g2 if g1 < self.treshold else g3
        b4 = b2 if b1 < self.treshold else b3
        return (r4, g4, b4)

class Mix():
    arity = 3
    mindepth = 0
    def __init__(self, w, e1, e2):
        self.w = w
        self.e1 = e1
        self.e2 = e2
        self.w_func = self.w.eval
        self.e1_func = self.e1.eval
        self.e2_func = self.e2.eval
    def __repr__(self):
        return 'Mix(%s, %s, %s)' % (self.w, self.e1, self.e2)
    def eval(self, x, y):
        w = 0.5 * (self.w_func(x, y)[0] + 1.0)
        c1 = self.e1_func(x, y)
        c2 = self.e2_func(x, y)
        return average(c1, c2, w)

class RGB():
    arity = 3
    mindepth = 4
    def __init__(self, e1, e2, e3):
        self.e1 = e1
        self.e2 = e2
        self.e3 = e3
        self.e1_func = self.e1.eval
        self.e2_func = self.e2.eval
        self.e3_func = self.e3.eval
    def __repr__(self):
        return 'RGB(%s, %s, %s)' % (self.e1, self.e2, self.e3)
    def eval(self, x, y):
        (r, _, _) = self.e1_func(x, y)
        (_, g, _) = self.e2_func(x, y)
        (_, _, b) = self.e3_func(x, y)
        return (r, g, b)

class Closest():
    arity = 3
    mindepth = 3
    def __init__(self, target, e1, e2):
        self.target = target
        self.e1 = e1
        self.e2 = e2
        self.target_func = self.target.eval
        self.e1_func = self.e1.eval
        self.e2_func = self.e2.eval
    def __repr__(self):
        return 'Closest(%s, %s, %s)' % (self.target, self.e1, self.e2)
    def eval(self, x, y):
        (r1, g1, b1) = self.target_func(x, y)
        (r2, g2, b2) = self.e1_func(x, y)
        (r3, g3, b3) = self.e2_func(x, y)
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
        self.target_func = self.target.eval
        self.e1_func = self.e1.eval
        self.e2_func = self.e2.eval
    def __repr__(self):
        return 'Far(%s, %s, %s)' % (self.target, self.e1, self.e2)
    def eval(self, x, y):
        (r1, g1, b1) = self.target_func(x, y)
        (r2, g2, b2) = self.e1_func(x, y)
        (r3, g3, b3) = self.e2_func(x, y)
        #distances between colors:
        d1 = math.sqrt((r2-r1)**2+(g2-g1)**2+(b2-b1)**2)
        d2 = math.sqrt((r3-r1)**2+(g3-g1)**2+(b3-b1)**2)

        return (r2, g2, b2) if d1 > d2 else (r3, g3, b3)
