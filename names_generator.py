#!/usr/bin/python

# Copyright (c) 2018, Yaroslav Zotov, https:github.com/qiray/
# All rights reserved.

# Some ideas and texts from http://ironigardinen.net/generatorer/art2/index.html

import random
from names_data import *

def adj_noun():
    return "%s %s" % (
        random.choice(adjectives),
        random.choice(nouns))
        
def pronoun_noun():
    return "%s %s" % (
        random.choice(pronouns),
        random.choice(nouns))

def pronoun_adj_noun():
    return "%s %s %s" % (
        random.choice(pronouns),
        random.choice(adjectives),
        random.choice(nouns))

def noun_prep_noun():
    return "%s %s %s" % (
        random.choice(nouns),
        random.choice(prepositions),
        random.choice(nouns))

def noun_prep_adj_noun():
    return "%s %s %s %s" % (
        random.choice(nouns),
        random.choice(prepositions),
        random.choice(adjectives),
        random.choice(nouns))

generators = [adj_noun, pronoun_noun, pronoun_adj_noun, noun_prep_noun, noun_prep_adj_noun]

def generate_name():
    generator = random.choice(generators)
    return generator()

# TODO:
# adjective + noun + noun
# pronoun + noun + noun
# adjective + noun + preposition + adjective + noun
# cylced
