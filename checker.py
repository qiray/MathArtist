
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

def functions_count(total, functions):
    result = 0
    for i in functions:
        if i in total:
            result += total[i]
    return result

def check_art(functions, coord_system, depth):
    """Image is probably bad if:
    art's depth is small (1 or 2);
    there are too many same functions;
    there are many Well and Tent."""

    depth = depth if depth > 0 else 1
    count = sum(functions.values())
    result = 0
    for _, v in functions.items():
        result += 5 # add small value for each used operator
        if v >= count*0.6: # if some operator is used to commonly:
            result -= v/count*100
    count -= functions_count(functions, ['VariableX', 'VariableY'])
    well_tent = functions_count(functions, ['Well', 'Tent'])
    if well_tent >= 0.6*count: #there are too many well and tent functions
        result -= int(well_tent/count*100)
    if depth <= 2 and well_tent >= 0.5*count: #small depth and many well and tent functions
        result -= 30/depth
    if coord_system == 'polar': # If coord_system is polar, image is often good
        result = result if result > 0 else 10
    if coord_system == 'rotate_coord' or coord_system == 'center': # Add some extra score
        result += 50
    #TODO: add drawing checker for single color
    # if image is one-color it's maybe bad (But how can we check it without drawing? Maybe find some random dots and calc result for them? Or maybe roughly draw image)
    # Add fuzzy logic?
    return result
