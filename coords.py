
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

import math

def linear_coord(x, y, size, polar_shift=None):
    u = 2 * x/size - 1.0
    v = 2 * y/size - 1.0
    return u, v

def tent_coord(x, y, size, polar_shift=None):
    u = 1 - 2 * abs(x/size)
    v = 1 - 2 * abs(y/size)
    return u, v

def sin_coord(x, y, size, polar_shift=None):
    u = math.sin(2*math.pi*x/size)
    v = math.sin(2*math.pi*y/size)
    return u, v

def rotate_coord(x, y, size, polar_shift=None):
    d = abs(x - y)/math.sqrt(2)
    u = math.sqrt(8)*d/size - 1
    v = math.sqrt(2*(x*x + y*y - d*d))/size - 1
    return u, v

def curved_rotate_coord(x, y, size, polar_shift=None):
    u = (x - y)/size
    v = math.sqrt(2*(x*x + y*y - u*u))/size - 1
    return u, v

def polar(x, y, size, polar_shift):
    x -= polar_shift[0]*size
    y -= polar_shift[1]*size
    u = math.sqrt(x*x + y*y)/size
    v = 0 if x == 0 else math.atan(y/x)*2/math.pi
    return u, v

def center(x, y, size, polar_shift):
    half = size/2
    if x >= half:
        x = size - x
    if y >= half:
        y = size - y
    u = 2 * x/half - 1.0
    v = 2 * y/half - 1.0
    return u, v

coord_transforms = [linear_coord, tent_coord, sin_coord, polar, curved_rotate_coord, 
    rotate_coord, center] #It's nice to find more conversions
