#!/usr/bin/python

# Copyright (c) 2018, Yaroslav Zotov, https:github.com/qiray/
# All rights reserved.

# Text data from 
# https://www.espressoenglish.net/100-common-nouns-in-english/
# https://grammar.yourdictionary.com/parts-of-speech/adjectives/list-of-adjective-words.html
# https://www.talkenglish.com/vocabulary/top-50-prepositions.aspx
# http://ironigardinen.net/generatorer/art2/index.html

# Some ideas from http://ironigardinen.net/generatorer/art2/index.html

import random

def file_to_list(path):
    lines = []
    with open(path) as f:
        lines = f.read().splitlines()
    return lines

nouns = file_to_list("data/nouns.txt")
adjectives = file_to_list("data/adjectives.txt")
pronouns = file_to_list("data/pronouns.txt")
prepositions = file_to_list("data/prepositions.txt")

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

def adj_noun_noun():
    return "%s %s %s" % (
        random.choice(adjectives),
        random.choice(nouns),
        random.choice(nouns))

def pronoun_noun_noun():
    return "%s %s %s" % (
        random.choice(pronouns),
        random.choice(nouns),
        random.choice(nouns))

def adj_noun_prep_adj_noun():
    return "%s %s %s %s %s" % (
        random.choice(adjectives),
        random.choice(nouns),
        random.choice(prepositions),
        random.choice(adjectives),
        random.choice(nouns))

def pronoun_noun_prep_pronoun_noun():
    return "%s %s %s %s %s" % (
        random.choice(pronouns),
        random.choice(nouns),
        random.choice(prepositions),
        random.choice(pronouns),
        random.choice(nouns))

def combined():
    # TODO:
    pass

generators = [adj_noun, pronoun_noun, pronoun_adj_noun, noun_prep_noun, noun_prep_adj_noun,
    adj_noun_noun, pronoun_noun_noun, adj_noun_prep_adj_noun, pronoun_noun_prep_pronoun_noun]

def generate_name():
    result = random.choice(generators)()
    result = result.lower().capitalize()
    return result

print (generate_name())
