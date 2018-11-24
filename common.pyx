
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

################################################################################

# This file uses code from Andrej Bauer's randomart project under 
# following conditions:

# Copyright (c) 2010, Andrej Bauer, http://andrej.com/
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# cython: language_level=3

cimport libc.math as cmath
import itertools

CONSOLE = 1
GUI = 2
SIZE = 512

ctypedef (double, double, double) color

# File with utility functions

# Math functions

cpdef double well(double x):
    '''A function which looks a bit like a well.'''
    cdef double result = 1 - 2 / cmath.pow(1 + x*x, 8)
    result = 1 if result < -1 else result
    return result

cpdef double tent(double x):
    '''A function that looks a bit like a tent.'''
    return 1 - 2 * cmath.fabs(x)

cpdef double sin_curve(double x):
    cdef double val = x if x != 0 else 1
    return cmath.sin(1/val)

cpdef double abs_sin(double x):
    return cmath.sin(cmath.fabs(x))

cpdef double wave(double x, double y):
    return cmath.sin(cmath.sqrt(x**2 + y**2))

# Color functions

cpdef int float_color_to_int(double c):
    return max(0, min(255, int(128 * (c + 1))))

cpdef color average(color c1, color c2, double w=0.5):
    '''Compute the weighted average of two colors. With w = 0.5 we get the average.'''
    (r1, g1, b1) = c1
    (r2, g2, b2) = c2
    cdef double r3 = w * r1 + (1 - w) * r2
    cdef double g3 = w * g1 + (1 - w) * g2
    cdef double b3 = w * b1 + (1 - w) * b2
    return (r3, g3, b3)

cpdef (int, int, int, int) int_rgb(double r, double g, double b):
    return (float_color_to_int(r), float_color_to_int(g), float_color_to_int(b), 255)

def rgb(r,g,b):
    '''Convert a color represented by (r,g,b) to a string understood by tkinter.'''
    cdef int u = float_color_to_int(r)
    cdef int v = float_color_to_int(g)
    cdef int w = float_color_to_int(b)
    return '#%02x%02x%02x' % (u, v, w)

def parse_color(str):
    h = str.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))

cpdef color color_binary(c1, c2, operator):
    cdef (int, int, int) colors1 = tuple([float_color_to_int(x) for x in c1])
    cdef (int, int, int) colors2 = tuple([float_color_to_int(x) for x in c2])
    return tuple([2*operator(x1, x2)/255.0 - 1 for x1, x2 in zip(colors1, colors2)])
