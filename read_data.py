#!/usr/bin/python

# Copyright (c) 2018, Yaroslav Zotov, https://github.com/qiray/
# All rights reserved.

import parser
import re
from operators import (VariableX, VariableY, Random, Sum, Product, Mod, Sin, And,
    Tent, Well, Level, Mix, Palette, Not, RGB, Closest, White, SinCurve, AbsSin, 
    Or, Xor, Atan, Far, Wave, Chess)
from coords import (linear_coord, tent_coord, sin_coord, polar, rotate_coord)

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
        for line in f.readlines():
            if line.startswith("Use depth:"):
                use_depth = line.split(':')[1].replace(" ", "")
            elif line.startswith("Coordinates transfrom:"):
                coord_transform = line.split(':')[1].replace(" ", "")
            elif line.startswith("Polar shift:"):
                polar_shift = line.split(':')[1].replace(" ", "")
            elif line.startswith("Formula:"):
                art = line.split(':')[1].replace(" ", "")
        return art, use_depth, coord_transform, polar_shift
    except:
        return "", "", "", None
