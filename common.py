#!/usr/bin/python

import math
import itertools

CANVAS = 1
IMAGE = 2

# Utility functions

def float_color_to_int(c):
    return max(0, min(255, int(128 * (c + 1))))

def average(c1, c2, w=0.5):
    '''Compute the weighted average of two colors. With w = 0.5 we get the average.'''
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2
    r3 = w * r1 + (1 - w) * r2
    g3 = w * g1 + (1 - w) * g2
    b3 = w * b1 + (1 - w) * b2
    return (r3, g3, b3)

def rgb(r,g,b):
    '''Convert a color represented by (r,g,b) to a string understood by tkinter.'''
    u = float_color_to_int(r)
    v = float_color_to_int(g)
    w = float_color_to_int(b)
    return '#%02x%02x%02x' % (u, v, w)

def well(x):
    '''A function which looks a bit like a well.'''
    return 1 - 2 / (1 + x*x) ** 8

def tent(x):
    '''A function that looks a bit like a tent.'''
    return 1 - 2 * abs(x)

def sin_curve(x):
    val = x if x != 0 else 1
    return math.sin(1/val)

def abs_sqrt(x):
    return math.sin(math.fabs(x))

def parse_color(str):
    h = str.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))

def color_and(c1, c2):
    colors1 = tuple([float_color_to_int(x) for x in c1])
    colors2 = tuple([float_color_to_int(x) for x in c2])
    return tuple([2*(x1 & x2)/255.0 - 1 for x1, x2 in zip(colors1, colors2)])

def color_or(c1, c2):
    colors1 = tuple([float_color_to_int(x) for x in c1])
    colors2 = tuple([float_color_to_int(x) for x in c2])
    return tuple([2*(x1 | x2)/255.0 - 1 for x1, x2 in zip(colors1, colors2)])

def color_xor(c1, c2):
    colors1 = tuple([float_color_to_int(x) for x in c1])
    colors2 = tuple([float_color_to_int(x) for x in c2])
    return tuple([2*(x1 | x2)/255.0 - 1 for x1, x2 in zip(colors1, colors2)])
