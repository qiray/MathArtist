
# MathArtist - tool for generating pictures using mathematical formulas.
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

import sys
import math
import random
import time
import hashlib
from datetime import datetime
from PIL import Image, ImageDraw

from common import rgb, int_rgb, SIZE
from operators import Palette
from operator_lists import operatorsLists, fulllist, generate_lists
from coords import coord_transforms
from read_data import parse_formula, read_file
from names_generator import generate_name
from checker import check_art

APP_NAME = "MathArtist"
VERSION_MAJOR = 0
VERSION_MINOR = 9
VERSION_BUILD = 2

class Art():
    """Math art generator class"""
    operatorsList = random.choice(operatorsLists)
    terminals = [op for op in operatorsList if op.arity == 0]
    nonterminals = [op for op in operatorsList if op.arity > 0]
    use_depth = True
    coord_transform = coord_transforms[0]
    polar_shifts = [[0.5, 0.5], [0, 0], [0, 1], [1, 0], [1, 1]]
    polar_shift = [0, 0]
    use_random_lists = True

    @staticmethod
    def init_static_data():
        if Art.use_random_lists:
            # We precompute those operators that have arity 0 and arity > 0
            Art.operatorsList = random.choice(operatorsLists)
            Art.terminals = [op for op in Art.operatorsList if op.arity == 0]
            Art.nonterminals = [op for op in Art.operatorsList if op.arity > 0]

        Art.use_depth = True if random.random() >= 0.5 else False
        Art.coord_transform = random.choice(coord_transforms)
        index = random.randint(-1, len(Art.polar_shifts) - 1)
        if index == -1:
            Art.polar_shift = [random.random(), random.random()]
        else:
            Art.polar_shift = Art.polar_shifts[index]

    @staticmethod
    def generate_lists():
        Art.terminals, Art.nonterminals = generate_lists(fulllist)
        Art.operatorsList = Art.terminals + Art.nonterminals
        Art.use_random_lists = False
        print([x.__name__ for x in Art.operatorsList])

    def __init__(self, hash_string=None, use_checker=False, console=False, load_file=None):
        self.name = self.init_name(hash_string)
        self.use_checker = use_checker
        self.size = SIZE #we always use constant size = 512
        self.size_log = int(math.log(self.size, 2))
        self.img = Image.new('RGB', (self.size, self.size))
        self.image_draw = ImageDraw.Draw(self.img)
        self.functions = {}
        self.output_path = "output/"
        self.console = console
        self.stop_work = False
        self.status = "Drawing"
        self.trigger = None
        self.image_array = self.init_image_array()
        if self.console:
            if load_file:
                self.read_file_data(load_file)
                exit(0)
            self.redraw()

    def stop_drawing(self):
        self.stop_work = True
        self.status = "Stopped"

    def set_trigger(self, trigger):
        self.trigger = trigger

    def init_name(self, hash_string):
        if hash_string:
            hex_string = hashlib.md5(hash_string.encode('utf-8'))
            hexdigest = hex_string.hexdigest()
            random.seed(int(hexdigest, 16))
            return hash_string
        random.seed(datetime.now())
        return generate_name()

    def update_functions_dict(self, name):
        '''Calc used functions count'''
        if not name in self.functions:
            self.functions[name] = 1
        else:
            self.functions[name] += 1

    def generate(self, k=8, depth=0):
        '''Randomly generate an expession of a given size.'''
        if k <= depth:
            # We used up available size, generate a leaf of the expression tree
            op = random.choice(Art.terminals)
            if self.use_checker:
                self.update_functions_dict(op.__name__)
            return op()
        # randomly pick an operator whose arity > 0 and mindepth <= depth
        if Art.use_depth and False:
            op = random.choice([x for x in Art.nonterminals if x.mindepth <= depth])
        else:
            op = random.choice(Art.nonterminals)
        if self.use_checker:
            self.update_functions_dict(op.__name__)
        # generate subexpressions
        args = [] # the list of generated subexpression
        depth += 1
        for _ in range(0, op.arity):
            args.append(self.generate(k, depth))
        return op(*args)

    def init_image_array(self):
        return [[None for _ in range(self.size)] for _ in range(self.size)]

    def redraw(self):
        Art.init_static_data()
        Palette.randomPalette()
        self.start = time.time()
        self.image_array = self.init_image_array()
        self.stop_work = False
        self.functions = {}
        depth = random.randrange(1, self.size_log + 1)
        self.art = self.generate(depth)
        if self.use_checker:
            result = check_art(self.art, self.functions, Art.coord_transform, depth)
            print ('Checker result =', result)
            while result <= 0:
                print ('Generating new art')
                depth = random.randrange(1, self.size_log + 1)
                self.art = self.generate(depth)
                result = check_art(self.art, self.functions, Art.coord_transform, depth)
                print ('Checker result =', result)
        self.name = generate_name()
        self.draw_image()

    def get_output_name(self):
        date = str(datetime.now().strftime('%Y-%m-%d %H-%M '))
        return self.output_path + date + self.name

    def save_image_text(self):
        self.img.save(self.get_output_name() + ".png")
        orig_stdout = sys.stdout #save original stdout
        f = open(self.get_output_name() + ".txt", 'w')
        sys.stdout = f #redirect stdout to file
        self.print_art()
        sys.stdout = orig_stdout #restore original stdout
        f.close()

    def draw_image(self):
        self.status = "Drawing"
        self.print_art()
        self.d = 16   # current square size
        if self.console:
            self.d = 1 #we don't need previews
        self.draw()
        if self.console:
            self.save_image_text()

    # def pair_eval(self, pair): #Used in map function
    #     (x, y) = pair
    #     u, v = Art.coord_transform(x, y, self.d, self.size, Art.polar_shift)
    #     return self.art.eval(u, v)

    def draw(self):
        if self.d < 1 or self.stop_work:
            self.end = time.time()
            print("Time for drawing:", self.end - self.start)
            self.status = "Completed in %g s" % (self.end - self.start)
            return
        # size = self.size // self.d
        # product = ((i, j) for i in range(size) for j in range(size))
        # result = list(map(self.pair_eval, product))
        # print (self.d)
        for y in range(0, self.size, self.d):
            if self.stop_work:
                break
            for x in range(0, self.size, self.d):
                if self.stop_work:
                    break
                #Convert coordinates to range [-1, 1]
                u, v = Art.coord_transform(x, y, self.d, self.size, Art.polar_shift)
                if not self.image_array[x][y]:
                    (r, g, b) = self.art.eval(u, v)
                    self.image_array[x][y] = int_rgb(r, g, b)
                #TODO: optimize drawing!
                self.image_draw.rectangle(
                    ((x, y), (x + self.d, y + self.d)),
                    fill=self.image_array[x][y]
                )
                
# # Create a NumPy array, which has four elements. The top-left should be pure red, the top-right should be pure blue, the bottom-left should be pure green, and the bottom-right should be yellow
# pixels = np.array([[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 0]]])

# # Create a PIL image from the NumPy array
# image = Image.fromarray(pixels.astype('uint8'), 'RGB')
        if self.trigger:
            self.trigger.emit() #emit trigger to redraw image
        self.d = self.d // 4
        self.draw()

    def read_file_data(self, path):
        try:
            art, use_depth, coord_transform, polar_shift, name = read_file(path)
            self.read_art_params(art, use_depth, coord_transform, polar_shift, name)
        except:
            print ("Failed to read file " + path)

    def read_art_params(self, art, use_depth, coord_transform, polar_shift, name):
        self.functions = {}
        self.art = parse_formula(art)
        Art.use_depth = parse_formula(use_depth)
        Art.coord_transform = parse_formula(coord_transform)
        if polar_shift:
            Art.polar_shift = parse_formula(polar_shift)
        if name:
            self.name = name
        else:
            self.name = generate_name()
        self.start = time.time()
        self.draw_image() #draw image with new params

    def print_art(self):
        print("Name:", self.name)
        print("Using operators:", [x.__name__ for x in Art.operatorsList])
        print("Use depth:", Art.use_depth)
        print("Coordinates transfrom:", Art.coord_transform.__name__)
        if Art.coord_transform.__name__ == 'polar':
            print("Polar shift:", Art.polar_shift)
        print("Formula:", self.art, '\n') #draw art tree
