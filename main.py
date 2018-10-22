#!/usr/bin/python

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

######################################################################
# SIMPLE RANDOM ART IN PYTHON
#
# Version 2010-04-21
#
# I get asked every so often to release the source code for my random art
# project at http://www.random-art.org/. The original source is written in Ocaml
# and is not publicly available, but here is a simple example of how you can get
# random art going in python in 250 lines of code.
#
# The idea is to generate expression trees that describe an image. For each
# point (x,y) of the image we evaluate the expression and get a color. A color
# is represented as a triple (r,g,b) where the red, green, blue components are
# numbers between -1 and 1. In computer graphics it is more usual to use the
# range [0,1], but since many operations are symmetric with respect to the
# origin it is more convenient to use the interval [-1,1].
#
# I kept the program as simple as possible, and independent of any non-standard
# Python libraries. Consequently, a number of improvements and further
# experiments are possible:
#
#   * The most pressing problem right now is that the image is displayed as a
#     large number of rectangles of size 1x1 on the tkinter Canvas, which
#     consumes a great deal of memory. You will not be able to draw large images
#     this way. An improved version would use the Python imagining library (PIL)
#     instead.
#
#   * The program uses a simple RGB (Red Green Blue) color model. We could also
#     use the HSV model (Hue Saturation Value), and others. One possibility is
#     to generate a palette of colors and use only colors that are combinations
#     of those from the palette.
#
#   * Of course, you can experiment by introducing new operators. If you are going
#     to play with the source, your first exercise should be a new operator.
#
#   * The program uses cartesian coordinates. You could experiment with polar
#     coordinates.
#
# For more information and further discussion, see http://math.andrej.com/category/random-art/

import math
import random
import time
import hashlib
from datetime import datetime
from tkinter import Tk, ALL, Canvas, Button # Change "Tkinter" to "tkinter" in Python 3
from PIL import Image, ImageDraw, ImageTk

from common import rgb, IMAGE, CANVAS
from operators import VariableX, VariableY, Constant, Sum, Product, Mod, Sin, Tent, Well, Level, Mix

# The following list of all classes that are used for generation of expressions is
# used by the generate function below.

operatorsList = (VariableX, VariableY, Constant, Sum, Product, Mod, Sin, Tent, Well, Level, Mix)
# operatorsList = (VariableX, VariableY, Mix, Well)
# operatorsList = (VariableX, VariableY, Constant, Mix, Well)

#TODO: generate pallettes and operators' lists
#TODO: read https://github.com/vshymanskyy/randomart
#TODO: make 2 versions: Python and Golang

# We precompute those operators that have arity 0 and arity > 0

operators0 = [op for op in operatorsList if op.arity == 0]
operators1 = [op for op in operatorsList if op.arity > 0]

def generate(k = 50):
    '''Randonly generate an expession of a given size.'''
    if k <= 0: 
        # We used up available size, generate a leaf of the expression tree
        op = random.choice(operators0)
        return op()
    else:
        # randomly pick an operator whose arity > 0
        op = random.choice(operators1)
        # generate subexpressions
        i = 0 # the amount of available size used up so far
        args = [] # the list of generated subexpression
        for j in sorted([random.randrange(k) for l in range(op.arity-1)]):
            args.append(generate(j - i))
            i = j
        args.append(generate(k - 1 - i))
        return op(*args)

class Art():
    """A simple graphical user interface for random art. It displays the image,
       and the 'Again!' button."""

    def __init__(self, master, size=256, draw_style=CANVAS, hash_string=None):
        self.root = master
        self.root.title('Random art')
        if hash_string:
            hex_string = hashlib.md5(hash_string.encode('utf-8'))
            hexdigest = hex_string.hexdigest()
            random.seed(int(hexdigest, 16))
        else:
            random.seed(datetime.now())
        self.draw_style = draw_style
        self.size = size
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
        self.start = time.time()
        if self.draw_alarm: 
            self.canvas.after_cancel(self.draw_alarm)
        self.canvas.delete(ALL)
        self.art = generate(random.randrange(20,150))
        print(self.art, '\n') #draw art tree
        self.d = 64   # current square size
        self.y = 0    # current row
        self.draw()
        if self.draw_style == IMAGE:
            self.photoImage = ImageTk.PhotoImage(image=self.img)
            self.img.save(self.filepath)
            self.canvas.create_image(0,0,image=self.photoImage,anchor="nw")

    def draw(self):
        if self.y >= self.size:
            self.y = 0
            self.d = self.d // 4
        if self.d >= 1:
            for x in range(0, self.size, self.d):
                #Convert coordinates to diapason [-1, 1]
                u = 2 * float(x + self.d/2)/self.size - 1.0
                v = 2 * float(self.y + self.d/2)/self.size - 1.0
                (r,g,b) = self.art.eval(u, v)
                if self.draw_style == IMAGE:
                    self.imageDraw.rectangle(
                        ((x, self.y), (x+self.d, self.y+self.d)), 
                        fill=rgb(r,g,b)
                    )
                else:
                    self.canvas.create_rectangle(
                        x, self.y, x+self.d, self.y+self.d,
                        width=0, fill=rgb(r,g,b)
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

# Main program
win = Tk()
arg = Art(win)
win.mainloop()
