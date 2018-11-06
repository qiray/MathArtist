#!/usr/bin/python

# Copyright (c) 2018, Yaroslav Zotov, https://github.com/qiray/
# All rights reserved.

import parser
import re
from operators import (VariableX, VariableY, Random, Sum, Product, Mod, Sin, And,
    Tent, Well, Level, Mix, Palette, Not, RGB, Closest, White, SinCurve, AbsSin, 
    Or, Xor, Atan, Far, Wave, Chess)

def parse_formula(formula):
    '''Parse formula and return it's code. Call eval(result) to use it.'''
    regex_x = re.compile(r"\bx\b")
    regex_y = re.compile(r"\by\b")
    try:
        formula = regex_x.sub("VariableX()", formula)
        formula = regex_y.sub("VariableY()", formula)
        code = parser.expr(formula).compile()
        return code
    except:
        return "VariableX"

code = parse_formula("Tent(Mix(x, y, Palette(0.820312, 0.75, 0.632812)))")
print(eval(code))
