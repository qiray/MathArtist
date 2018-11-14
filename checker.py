
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

def check_art(functions, coord_system, depth):
    print(functions)
    print(coord_system)
    print(depth)
    #TODO:
    # Image is probably bad if:
    # art's depth is small (1 to 3 or 1 to 2)
    # there are too many same functions
    # many of Well, Tent
    # maybe also Sin, SinCurve
    # But if coord_system is polar or rotate image is often good
    # if image is one-color it's maybe bad (But how can we check it without drawing? Maybe find some random dots and calc result for them? Or maybe roughly draw image)
    # Make checker with fuzzy logic
    return True
