
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

import parser
import re
from operators import (VariableX, VariableY, Random, Sum, Product, Mod, Sin, And,
    Tent, Well, Level, Mix, Palette, Not, RGB, Closest, White, SinCurve, AbsSin,
    Or, Xor, Atan, Far, Wave, Chess)
from coords import (linear_coord, tent_coord, sin_coord, polar, curved_rotate_coord,
    rotate_coord, center)

def parse_formula(formula):
    '''Parse formula and return it's code.'''
    regex_x = re.compile(r"\bx\b")
    regex_y = re.compile(r"\by\b")
    try:
        formula = regex_x.sub("VariableX()", formula)
        formula = regex_y.sub("VariableY()", formula)
        code = parser.expr(formula).compile()
        return eval(code)
    except:
        return eval("VariableX()")

def read_file(filepath):
    try:
        f = open(filepath, "r")
        use_depth = None
        art = None
        coord_transform = None
        polar_shift = None
        name = None
        for line in f.readlines():
            if line.startswith("Use depth:"):
                use_depth = line.split(':')[1].replace(" ", "")
            elif line.startswith("Coordinates transform:"):
                coord_transform = line.split(':')[1].replace(" ", "")
            elif line.startswith("Polar shift:"):
                polar_shift = line.split(':')[1].replace(" ", "")
            elif line.startswith("Formula:"):
                art = line.split(':')[1].replace(" ", "")
            elif line.startswith("Name:"):
                name = line.split(':')[1]
        return art, use_depth, coord_transform, polar_shift, name
    except:
        return "", "", "", None
