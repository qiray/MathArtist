#!/usr/bin/python

# Copyright (c) 2018, Yaroslav Zotov, https:github.com/qiray/
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

# Text data from 
# https://www.espressoenglish.net/100-common-nouns-in-english/
# https://grammar.yourdictionary.com/parts-of-speech/adjectives/list-of-adjective-words.html
# https://www.talkenglish.com/vocabulary/top-50-prepositions.aspx
# http://ironigardinen.net/generatorer/art2/index.html

# Some ideas from http://ironigardinen.net/generatorer/art2/index.html

import os
import random

from common import get_app_path

def file_to_list(path):
    lines = []
    with open(os.path.join(get_app_path(), path)) as f:
        lines = f.read().splitlines()
    return lines

nouns = file_to_list("data/nouns.txt")
adjectives = file_to_list("data/adjectives.txt")
pronouns = file_to_list("data/pronouns.txt")
prepositions = file_to_list("data/prepositions.txt")

def adj_or_pronoun():
    return random.choice(adjectives) if random.random() > 0.5 else random.choice(pronouns)

def two_words():
    word = adj_or_pronoun()
    return "%s %s" % (
        word,
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

def desc_noun_noun():
    word = adj_or_pronoun()
    return "%s %s %s" % (
        word,
        random.choice(nouns),
        random.choice(nouns))

def five_words():
    word1 = adj_or_pronoun()
    word2 = adj_or_pronoun()
    return "%s %s %s %s %s" % (
        word1,
        random.choice(nouns),
        random.choice(prepositions),
        word2,
        random.choice(nouns))

def word_chain():
    length = random.randint(1, 2)
    result = five_words()
    for _ in range(length):
        word = adj_or_pronoun()
        result += " %s %s %s" % (
            random.choice(prepositions),
            word,
            random.choice(nouns))
    return result

generators = [two_words, pronoun_adj_noun, noun_prep_noun, noun_prep_adj_noun,
    desc_noun_noun, five_words, word_chain]

def generate_name():
    result = random.choice(generators)()
    result = result.lower().capitalize()
    return result
