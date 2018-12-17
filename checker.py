
# Copyright (c) 2018, Yaroslav Zotov, https://github.com/qiray/
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

'''Module for checking generated art'''

import math
import random
from common import SIZE, float_color_to_int

def functions_count(total, functions):
    result = 0
    for i in functions:
        if i in total:
            result += total[i]
    return result

def color_distance(c1, c2):
    (r1, g1, b1) = c1
    (r2, g2, b2) = c2
    r = abs(r1 - r2)/255
    g = abs(g1 - g2)/255
    b = abs(b1 - b2)/255
    return (r + g + b) / 3 #1 means opposit colors, 0 means same colors

def get_hue(color):
    (r, g, b) = color
    R = r / 255
    G = g / 255
    B = b / 255
    c_max = max(r, g, b)
    c_min = min(r, g, b)
    result = 0
    delta = c_max - c_min
    if delta == 0:
        return 0
    if c_max== r:
        result = (G - B)/delta
    elif c_max == g:
        result = 2.0 + (B - R)/delta
    else:
        result = 4.0 + (R - G)/delta
    result *= 60
    result = result if result > 0 else 360 + result
    return result

def preview_score(art, coord_system):
    """Check colors count"""
    shift = [0, 0]
    d = 16
    size = SIZE #Is it normal?
    colors = []
    hues = []
    for y in range(0, size, d):
        for x in range(0, size, d):
            u, v = coord_system(x, y, size, shift)
            (r, g, b) = art.eval(u, v)
            color = (float_color_to_int(r), float_color_to_int(g), float_color_to_int(b))
            colors.append(color)
            hues.append(get_hue(color))
    set_colors = set(colors)
    if len(set_colors) == 1:
        return -1000
    set_hues = set(hues)
    print(set_hues)
    #TODO: calc distances for hues
    # distances = []
    # list_colors = list(set_colors)
    # list_colors.sort()
    # for i in range(len(list_colors) - 1):
    #     distances.append(color_distance(list_colors[i], list_colors[i + 1]))

    # print(color_distance(list_colors[0], list_colors[-1]))
    # if max(distances) <= 0.05:
    #     return -100
    # elif max(distances) <= 0.2:
    #     return -10
    return 1

def check_art(art, functions, coord_system, depth):
    """Generated art quality checker.
    Image is probably bad if:
    art's depth is small (1 or 2);
    there are too many same functions;
    there are many Well and Tent."""

    coord_system_name = coord_system.__name__
    depth = depth if depth > 0 else 1
    count = sum(functions.values())
    if count >= 10000: #Too difficult formula
        return -1000
    result = 5*len(functions)
    count -= functions_count(functions, ['VariableX', 'VariableY'])
    well_tent = functions_count(functions, ['Well', 'Tent'])
    if well_tent >= 0.6*count: #there are too many well and tent functions
        result -= int(well_tent/count*100)
    if depth <= 2 and well_tent >= 0.5*count: #small depth and many well and tent functions
        result -= 30/depth
    if coord_system_name == 'polar': # If coord_system is polar, image is often good
        result = result if result > 0 else 10
    if coord_system_name == 'rotate_coord' or coord_system_name == 'center': # Add some extra score
        result += 50
    result += preview_score(art, coord_system)
    if result < 0 and result > -50 and random.random() > 0.8: #sometimes even a bad picture should get a chance
        result = 1
    elif result < -50 and random.random() > 0.99:
        result = 0.1
    return result
