#!/usr/bin/python

# Copyright (c) 2010, Andrej Bauer, http://andrej.com/
# Copyright (c) 2018, Yaroslav Zotov, https://github.com/qiray/
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

# http://www.random-art.org/
# http://math.andrej.com/category/random-art/

import math
import random
import time
import hashlib
import sys
import signal
from datetime import datetime
from tkinter import Tk, ALL, Canvas, Button
from PIL import Image, ImageDraw, ImageTk

from common import rgb, IMAGE, CANVAS
from operators import (VariableX, VariableY, Random, Sum, Product, Mod, Sin, And,
    Tent, Well, Level, Mix, Palette, Not, RGB, Closest, White, SinCurve, AbsSqrt, 
    Or, Xor)

# The following list of all classes that are used for generation of expressions is
# used by the generate function below.

operatorsLists = [
    (VariableX, VariableY, Random, Sum, Product, Mod, Sin, Tent, AbsSqrt, Xor,
        Well, Level, Mix, Palette, Not, RGB, Closest, White, SinCurve, And, Or),
    (VariableX, VariableY, Mix, Well),
    (VariableX, VariableY, Random, Mix, Well),
    (VariableX, VariableY, Palette, Mix, Well),
    (VariableX, VariableY, Palette, Mix, Well, Tent),
    (VariableX, VariableY, Palette, Mix, Well, Tent, SinCurve),
    (VariableX, VariableY, Palette, Sin, SinCurve, Mix),
    (VariableX, VariableY, Palette, AbsSqrt, Sin, Mix),
    (VariableX, VariableY, Palette, And, Or, Xor),
]

def coord_default(x, y, d, size):
    u = 2 * float(x + d/2)/size - 1.0
    v = 2 * float(y + d/2)/size - 1.0
    return u, v

def simple_linear_coord(x, y, d, size):
    u = 2 * float(x)/size - 1.0
    v = 2 * float(y)/size - 1.0
    return u, v

def tent_coord(x, y, d, size):
    u = 1 - 2 * abs(float(x)/size)
    v = 1 - 2 * abs(float(y)/size)
    return u, v

def sin_coord(x, y, d, size):
    u = math.sin(x/size)
    v = math.sin(y/size)
    return u, v

coord_transforms = [coord_default, simple_linear_coord, tent_coord, sin_coord] #TODO: add multiple conversions

#TODO: generate operators' lists or find nice examples and make them predefined
#TODO: make 2 versions: Python and Golang

class Art():
    """A simple graphical user interface for random art. It displays the image,
       and the 'Again!' button."""
    operatorsList = random.choice(operatorsLists)
    terminals = [op for op in operatorsList if op.arity == 0]
    nonterminals = [op for op in operatorsList if op.arity > 0]
    use_depth = True
    coord_transform = coord_transforms[0]

    @staticmethod
    def init_static_data():
        Art.operatorsList = random.choice(operatorsLists)
        Art.terminals = [op for op in Art.operatorsList if op.arity == 0]
        Art.nonterminals = [op for op in Art.operatorsList if op.arity > 0]
        Art.use_depth = True if random.random() >= 0.5 else False
        Art.coord_transform = random.choice(coord_transforms)

    @staticmethod
    def generate(k=8, depth=0):
        '''Randonly generate an expession of a given size.'''
        if k <= depth:
            # We used up available size, generate a leaf of the expression tree
            op = random.choice(Art.terminals)
            return op()
        # randomly pick an operator whose arity > 0 and mindepth <= depth
        if Art.use_depth and False:
            op = random.choice([x for x in Art.nonterminals if x.mindepth <= depth])
        else:
            op = random.choice(Art.nonterminals)
        # generate subexpressions
        args = [] # the list of generated subexpression
        depth += 1
        for _ in range(0, op.arity):
            args.append(Art.generate(k, depth))
        return op(*args)

    def __init__(self, master, size=256, draw_style=CANVAS, hash_string=None):
        self.root = master
        self.root.title('Random art')
        # We precompute those operators that have arity 0 and arity > 0

        def close(event):
            self.root.withdraw()
            sys.exit()
        self.root.bind('<Escape>', close)

        if hash_string:
            hex_string = hashlib.md5(hash_string.encode('utf-8'))
            hexdigest = hex_string.hexdigest()
            random.seed(int(hexdigest, 16))
        else:
            random.seed(datetime.now())
        self.draw_style = draw_style
        self.size = size
        self.size_log = int(math.log(self.size, 2))
        self.filepath = '1.png'
        self.img = Image.new('RGB', (size, size))
        self.imageDraw = ImageDraw.Draw(self.img)
        self.photoImage = ImageTk.PhotoImage(image=self.img)
        self.canvas = Canvas(self.root, width=size, height=size)
        self.canvas.grid(row=0,column=0)
        b = Button(self.root, text='Again!', command=self.redraw)
        b.grid(row=1,column=0)
        self.draw_alarm = None
        self.redraw()

    def redraw(self):
        Art.init_static_data()
        Palette.randomPalette()
        self.start = time.time()
        if self.draw_alarm: 
            self.canvas.after_cancel(self.draw_alarm)
        self.canvas.delete(ALL)
        self.art = Art.generate(random.randrange(1, self.size_log + 1))
        self.print_art()
        self.d = 64   # current square size
        self.y = 0    # current row
        self.draw()
        if self.draw_style == IMAGE:
            self.photoImage = ImageTk.PhotoImage(image=self.img)
            self.img.save(self.filepath)
            self.canvas.create_image(0, 0, image=self.photoImage, anchor="nw")

    def draw(self):
        if self.y >= self.size:
            self.y = 0
            self.d = self.d // 4
        if self.d >= 1:
            for x in range(0, self.size, self.d):
                #Convert coordinates to diapason [-1, 1]
                u, v = Art.coord_transform(x, self.y, self.d, self.size)
                (r, g, b) = self.art.eval(u, v)
                if self.draw_style == IMAGE:
                    self.imageDraw.rectangle(
                        ((x, self.y), (x + self.d, self.y + self.d)),
                        fill=rgb(r, g, b)
                    )
                else:
                    self.canvas.create_rectangle(
                        x, self.y, x+self.d, self.y+self.d,
                        width=0, fill=rgb(r, g, b)
                    )
            self.y += self.d
            if self.draw_style == IMAGE:
                self.draw()
            else:
                self.draw_alarm = self.canvas.after(1, self.draw)
        else:
            self.draw_alarm = None
            self.end = time.time()
            print("Time for drawing:", self.end - self.start)

    def print_art(self):
        print("Using operators:", [x.__name__ for x in Art.operatorsList])
        print("Use depth:", Art.use_depth)
        print("Coordinates transfrom:", Art.coord_transform.__name__)
        print(self.art, '\n') #draw art tree

# Main program

def sigint_handler(sig, frame):
    print("Closing...")
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

win = Tk()
arg = Art(win)
win.mainloop()

# Using operators: ['VariableX', 'VariableY', 'Palette', 'Sin', 'SinCurve', 'Mix']
# Use depth: False
# Coordinates transfrom: sin_coord
# SinCurve(Sin(1.00736 + 3.24802 * Mix(y, x, Const(0.960938, 0.539062, 0.195312))))

# Using operators: ['VariableX', 'VariableY', 'Palette', 'Mix', 'Well', 'Tent']
# Use depth: False
# Coordinates transfrom: tent_coord
# Tent(Mix(x, y, Const(0.820312, 0.75, 0.632812)))