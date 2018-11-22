
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
    average_r = (r1 + r2)/2
    delta_r = (r1 -r2)**2
    delta_g = (g1 - g2)**2
    delta_b = (b1 - b2)**2
    return math.sqrt(2*delta_r + 4*delta_g + 3*delta_b + (average_r*(delta_r - delta_b))/256)

def preview_score(art, coord_system):
    shift = [0, 0]
    d = 16
    y = 0
    size = SIZE #Is it normal?
    colors = []
    for y in range(0, size, d):
        for x in range(0, size, d):
            u, v = coord_system(x, y, d, size, shift)
            (r, g, b) = art.eval(u, v)
            colors.append((float_color_to_int(r), float_color_to_int(g), float_color_to_int(b)))
    set_colors = set(colors)
    if len(set_colors) == 1:
        return -100
    distances = []
    it_colors = list(set_colors)
    for i in range(len(it_colors) - 1):
        distances.append(color_distance(it_colors[i], it_colors[i + 1]))
    if max(distances) <= 20:
        return -50
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
    if result < 0 and random.random() > 0.8: #sometimes even a bad picture should get a chance
        result = 1
    return result
