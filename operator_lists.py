#!/usr/bin/python

# Copyright (c) 2018, Yaroslav Zotov, https://github.com/qiray/
# All rights reserved.

import random

def generate_lists(fulllist):
    terminals = [op for op in fulllist if op.arity == 0]
    nonterminals = [op for op in fulllist if op.arity > 0]

    length = random.randint(0, len(terminals) - 1) #There should be at least one element
    random.shuffle(terminals)
    terminals = terminals[length:] #Get a part of a list

    length = random.randint(0, len(nonterminals) - 1)
    random.shuffle(nonterminals)
    nonterminals = nonterminals[length:] #Get a part of a list

    return terminals, nonterminals

