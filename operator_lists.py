#!/usr/bin/python

# Copyright (c) 2018, Yaroslav Zotov, https://github.com/qiray/
# All rights reserved.

import random

from operators import (VariableX, VariableY, Random, Sum, Product, Mod, Sin, And,
    Tent, Well, Level, Mix, Palette, Not, RGB, Closest, White, SinCurve, AbsSin, 
    Or, Xor, Atan, Far, Wave, Chess)

# The following lists of classes that are used for generation of expressions is
# used by the generate function below. Each list should contain at least one
# terminal and nonterminal class.

fulllist = (VariableX, VariableY, Random, Sum, Product, Mod, Sin, Tent, AbsSin,
        Well, Level, Mix, Palette, Not, RGB, Closest, White, SinCurve, And, Or,
        Atan, Xor, Far, Wave, Chess)

operatorsLists = [
    fulllist,
    (VariableX, VariableY, Random, Sum, Product, Mod, Sin, Tent, Well, Level, Mix, Palette),
    (VariableX, VariableY, Mix, Well),
    (VariableX, VariableY, Random, Mix, Well),
    (VariableX, VariableY, Palette, Mix, Well),
    (VariableX, VariableY, Palette, Mix, Well, Tent),
    (VariableX, VariableY, Palette, Mix, Well, Tent, SinCurve),
    (VariableX, VariableY, Palette, Sin, SinCurve, Mix), #50/50
    (VariableX, VariableY, Palette, AbsSin, Sin, Mix),
    (VariableX, VariableY, Palette, And, Or, Xor),
    (VariableX, VariableY, Random, Palette, Mix, Well, Sin, SinCurve, Tent, AbsSin),
    (VariableX, VariableY, White, Palette, Random, AbsSin, Mix, Level, RGB, Sum, Mod),
    (VariableX, VariableY, White, Palette, Random, AbsSin, Mix, Level, RGB, Product, 
        Sum, Mod, Well, Tent),
    (VariableX, VariableY, White, Palette, Random, RGB),
    (VariableX, VariableY, White, Palette, Random, RGB, Sin, SinCurve, Atan, Mix, Closest),
    (VariableX, VariableY, White, Palette, Random, RGB, Far, Closest, Mix, Well),
    (VariableX, VariableY, White, Palette, Random, RGB, Far, Closest, Mix, Well, Wave), #Not bad but...
    (VariableX, VariableY, Palette, Sin, SinCurve, Mix, Wave),
    (VariableX, VariableY, Palette, Sin, SinCurve, Atan, Wave), #not impressive
    (VariableX, VariableY, Mix, Well, Not, Palette),
    (VariableX, VariableY, Palette, Random, Mix, Well, Tent, Chess),
    (VariableX, VariableY, Palette, Random, Mix, Well, Tent, SinCurve),
    (VariableX, VariableY, Palette, Random, Mix, SinCurve, Sin, AbsSin, Atan),

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
]

def generate_lists(fulllist):
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

