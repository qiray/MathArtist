#!/usr/bin/python

CANVAS = 1
IMAGE = 2

# Utility functions

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
    u = max(0, min(255, int(128 * (r + 1))))
    v = max(0, min(255, int(128 * (g + 1))))
    w = max(0, min(255, int(128 * (b + 1))))
    return '#%02x%02x%02x' % (u, v, w)

def well(x):
    '''A function which looks a bit like a well.'''
    return 1 - 2 / (1 + x*x) ** 8

def tent(x):
    '''A function that looks a bit like a tent.'''
    return 1 - 2 * abs(x)

def parse_color(str):
    h = str.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))

def invert(color):
    (r1,g1,b1) = color
    return (-r1, -g1, -b1)
