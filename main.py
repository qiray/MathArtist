#!/usr/bin/python3
# -*- coding: utf-8 -*-

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

import sys
import signal
import argparse
from PIL import Image, ImageDraw, ImageQt

from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication, QLabel)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal

from art import Art, APP_NAME, VERSION_MAJOR, VERSION_MINOR, VERSION_BUILD

#pyinstaller --onefile --windowed main.py

#TODO: readme
#TODO: add icon
#TODO: test on different OS
#TODO: enable checker in GUI

class DrawThread(QThread):
    def __init__(self, func):
        self.func = func
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        self.func()

class GUI(QWidget):

    trigger = pyqtSignal()

    def __init__(self, art):
        super().__init__()
        self.art = art
        self.draw_thread = None
        self.initGUI()

    def keyPressEvent(self, event): #Handle keys
        if event.key() == QtCore.Qt.Key_Escape:
            print("Closing...")
            self.close()
        event.accept()
    
    def save_image(self):
        self.art.save_image_text()

    def new_image(self):
        self.image = self.generate_image()
        self.trigger.emit()

    def update_GUI(self):
        self.image = ImageQt.ImageQt(self.art.img)
        pixmap = QPixmap.fromImage(self.image)
        self.image_label.setPixmap(pixmap)
        self.name_label.setText(self.art.name)
        self.status_label.setText(self.get_status())

    def new_image_thread(self):
        if self.draw_thread:
            self.art.stop_drawing() #send signal to art object
        else:
            self.trigger.connect(self.update_GUI)
            self.art.trigger = self.trigger
        self.draw_thread = DrawThread(self.new_image)
        self.draw_thread.start()

    def generate_image(self):
        self.art.redraw()
        image = self.art.img
        return ImageQt.ImageQt(image)

    def empty_image(self):
        size = 512
        image = Image.new('RGB', (size, size))
        image_draw = ImageDraw.Draw(image)
        image_draw.rectangle(((0, 0,), (size, size)), fill="#FFFFFF")
        return ImageQt.ImageQt(image)

    def get_status(self):
        return self.art.status

    def initGUI(self):
        #TODO: make some design
        #TODO: add 2 tabs: with canvas and generate/save buttons and with settings such as read file etc.
        #TODO: load image button
        #TODO: generate lists button (developer only)
        grid = QGridLayout()
        self.setLayout(grid)
        #IMPORTANT: this image must exist all application lifetime:
        self.image = self.empty_image()
        pixmap = QPixmap.fromImage(self.image)
        self.image_label = QLabel()
        self.image_label.setPixmap(pixmap)
        grid.addWidget(self.image_label, 0, 0, 1, 2)
        self.name_label = QLabel(self.art.name)
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        grid.addWidget(self.name_label, 1, 0, 1, 2)

        new_button = QPushButton('New image')
        new_button.clicked.connect(self.new_image_thread)
        grid.addWidget(new_button, 2, 0)
        save_button = QPushButton('Save image')
        save_button.clicked.connect(self.save_image)
        grid.addWidget(save_button, 2, 1)
        self.status_label = QLabel(self.get_status())
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(self.status_label, 3, 0, 1, 2)

        self.setWindowTitle('Math Artist')
        self.show()
        self.new_image_thread()

def sigint_handler(sig, frame):
    print("Closing...")
    sys.exit(0)

def parse_args():
    """argparse settings"""
    parser = argparse.ArgumentParser(prog=APP_NAME, 
        description='Tool for generating pictures using mathematical formulas.')
    parser.add_argument('--console', action='store_true', help='Run in console mode (no window)')
    parser.add_argument('--about', action='store_true', help='Show about info')
    parser.add_argument('--checker', action='store_true', help='Enable checker')
    parser.add_argument('--file', type=str, help='Load file (console mode only)')
    return parser.parse_args()

if __name__ == '__main__':

    signal.signal(signal.SIGINT, sigint_handler)
    args = parse_args() #parse command line arguments
    if args.about:
        print("\n" + APP_NAME + " Copyright (C) 2018 Yaroslav Zotov.\n" +
            "Based on \"randomart\" Copyright (C) 2010, Andrej Bauer.\n"
            "This program comes with ABSOLUTELY NO WARRANTY.\n" +
            "This is free software; see the source for copying conditions\n")
        exit(0)
    if args.console:
        art = Art(use_checker=args.checker, console=True, load_file=args.file)
    else:
        app = QApplication(sys.argv)
        window = GUI(Art())
        sys.exit(app.exec_())
