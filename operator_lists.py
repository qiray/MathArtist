
# Copyright (c) 2018, 2021, Yaroslav Zotov, https://github.com/qiray/
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

import random

from full_list import *

# The following lists of classes that are used for generation of expressions is
# used by the generate function below. Each list should contain at least one
# terminal and nonterminal class.

fulllist = (VariableX, VariableY, Random, Sum, Product, Mod, Sin, Tent, AbsSin,
        Well, Level, Mix, Palette, Not, RGB, Closest, White, SinCurve, And, Or,
        Atan, Xor, Far, Wave, Chess, Fibonacci)

operatorsLists = [
    fulllist,

    (VariableX, VariableY, Random, Sum, Product, Mod, Sin, Tent, Well, Level, Mix),
    (VariableX, VariableY, Random, Sum, Product, Mod, Sin, Tent, Well, Level, Mix, Palette),
    (VariableX, VariableY, Mix, Well), #minimalism
    (VariableX, VariableY, Random, Mix, Well),
    (VariableX, VariableY, Palette, Mix, Well),
    (VariableX, VariableY, Palette, Mix, Well, Tent),
    (VariableX, VariableY, Palette, Mix, Well, Tent, SinCurve), #nice curves
    (VariableX, VariableY, Palette, Sin, SinCurve, Mix), #multiple colors
    (VariableX, VariableY, White, Palette, Random, RGB), #colors only

    (VariableX, VariableY, Palette, AbsSin, Sin, Mix),
    (VariableX, VariableY, Palette, Mix, Well, Tent, SinCurve, AbsSin),
    (VariableX, VariableY, Palette, And, Or, Xor), #squares
    (VariableX, VariableY, Random, Palette, Mix, Well, Sin, SinCurve, Tent, AbsSin),
    (VariableX, VariableY, White, Palette, Random, AbsSin, Mix, Level, RGB, Sum, Mod), #sometimes dark
    (VariableX, VariableY, White, Palette, Random, AbsSin, Mix, Level, RGB, Product,
        Sum, Mod, Well, Tent),
    (VariableX, VariableY, White, Palette, Random, RGB, Sin, SinCurve, Atan, Mix, Closest),
    (VariableX, VariableY, White, Palette, Random, RGB, Far, Closest, Mix, Well),
    (VariableX, VariableY, White, Palette, Random, RGB, Far, Closest, Mix, Well, Wave), #Strange colored spots
    (VariableX, VariableY, Palette, Sin, SinCurve, Mix, Wave),
    (VariableX, VariableY, Palette, Sin, SinCurve, Atan, Wave), #not impressive
    (VariableX, VariableY, Mix, Well, Not, Palette),
    (VariableX, VariableY, Palette, Random, Mix, Well, Tent, Chess),
    (VariableX, VariableY, Palette, Random, Mix, Well, Tent, SinCurve),
    (VariableX, VariableY, Palette, Random, Mix, SinCurve, Sin, AbsSin, Atan),
    (VariableX, VariableY, Fibonacci, Mix),
    (VariableX, VariableY, Fibonacci, Mix, Well),
    (VariableX, VariableY, Random, Sum, Fibonacci, Sin, Tent, Well, Level, Mix, Palette),
    (VariableX, VariableY, Palette, Fibonacci, Mix, Well, Tent, SinCurve),
    (VariableX, VariableY, White, Palette, Random, Palette, Sin, SinCurve, Mix, Fibonacci),

    # these lists were made by this program
    (White, Palette, Random, VariableX, VariableY, Far, Well, Sin, AbsSin, Product),
    (Random, White, VariableY, VariableX, Palette, SinCurve, Level, Atan, Not, Far, Wave, Or, Xor),
    (Palette, Random, VariableY, White, VariableX, Well, Mix, Sin, Sum, Not, Tent, Level, Far, And),
    (VariableY, VariableX, Random, Product, SinCurve, Mod, Closest, Tent, Well, Sum, RGB, Atan, Xor,
        Not, And, Wave, Mix, Level, AbsSin),
    (VariableX, VariableY, SinCurve, AbsSin, Sum, Level),
    (Random, Palette, VariableY, VariableX, And, Sum, Mod),
    (Palette, VariableX, Random, White, VariableY, Atan, Xor, Closest, Mix, Product, RGB, Not, Well),
    (Chess, White, RGB, Xor, Far, Well, And, Level, Wave, SinCurve, Mod, Atan),
    (Random, Chess, White, Level, Mix, Closest, Xor, Tent, Sin, Wave, Product, Or, Sum, Well, Mod,
        Far, Not),
    (White, Random, VariableY, Palette, Xor, Far, Sin, Not, Mod, And, Atan, Sum, Wave, Level, Well),
    (Random, Palette, VariableY, VariableX, Not, Sin, AbsSin, Product, Far, Or, Atan, Tent, Mod, Xor,
        Wave, Sum),
    (VariableX, VariableY, White, Mod, Product, Atan, RGB, Mix, SinCurve, Xor, And, Level, Sin,
        AbsSin, Well, Tent),
]

def generate_lists():
    '''Function for generating operators lists'''
    terminals = [op for op in fulllist if op.arity == 0]
    nonterminals = [op for op in fulllist if op.arity > 0]

    length = random.randint(0, len(terminals) - 1) #There should be at least one element
    random.shuffle(terminals)
    terminals = terminals[length:] #Get a part of a list

    length = random.randint(0, len(nonterminals) - 1)
    random.shuffle(nonterminals)
    nonterminals = nonterminals[length:] #Get a part of a list

    return terminals, nonterminals
