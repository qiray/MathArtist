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
import time
from copy import copy
import webbrowser
from PIL import Image, ImageDraw, ImageQt

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication,
    QLabel, QFileDialog, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal

from art import Art, APP_NAME, VERSION_MAJOR, VERSION_MINOR, VERSION_BUILD
from common import SIZE

#pyinstaller --onefile --windowed main.py --hidden-import=palettes

#TODO: test on different OS
#TODO: add autoposting (twitter for example)

class DrawThread(QThread):
    def __init__(self, load_file=""):
        self.art = Art(use_checker=True)
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        self.art.redraw()

    def stop(self):
        self.art.stop_drawing() #send signal to art object
        self.wait()

    def get_image(self):
        return self.art.img

    def get_name(self):
        return self.art.name

    def save_image(self):
        self.art.save_image_text()

    def get_status(self):
        return self.art.status

    def set_trigger(self, trigger):
        self.art.set_trigger(trigger)

    def set_file(self, filepath):
        self.art.set_file(filepath)

class GUI(QWidget):

    trigger = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.draw_thread = None
        self.timer = 0
        self.initGUI()

    def keyPressEvent(self, event): #Handle keys
        key = event.key()
        # modifiers = QApplication.keyboardModifiers() #modifiers == QtCore.Qt.ControlModifier
        if key == QtCore.Qt.Key_Escape:
            print("Closing...")
            self.close()
        elif key == QtCore.Qt.Key_N:
            self.new_image_thread()
        elif key == QtCore.Qt.Key_O:
            self.load_file()
        elif key == QtCore.Qt.Key_S:
            self.save_image()
        elif key == QtCore.Qt.Key_A:
            self.show_about_message()
        elif key == QtCore.Qt.Key_F1:
            self.show_online_help()
        event.accept()

    def show_about_message(self):
        QMessageBox.about(self, 'About', get_about_info())

    def show_online_help(self):
        webbrowser.open('http://google.com') #TODO: open github readme

    def save_image(self):
        if self.draw_thread:
            self.draw_thread.save_image()

    def update_GUI(self):
        self.image = ImageQt.ImageQt(copy(self.draw_thread.get_image()))
        pixmap = QPixmap.fromImage(self.image)
        self.image_label.setPixmap(pixmap)
        self.name_label.setText(self.draw_thread.get_name())
        self.status_label.setText(self.draw_thread.get_status())

    def new_image_thread(self):
        if time.time() - self.timer < 1: #prevent from very often image updates
            return
        self.timer = time.time()
        if self.draw_thread: #if thread exists
            self.draw_thread.stop() #send signal to art object
        else: #init thread
            self.trigger.connect(self.update_GUI)
            self.draw_thread = DrawThread()
        self.draw_thread.set_trigger(self.trigger)
        self.draw_thread.start()

    def empty_image(self):
        size = SIZE
        image = Image.new('RGBA', (size, size))
        image_draw = ImageDraw.Draw(image)
        image_draw.rectangle(((0, 0,), (size, size)), fill="#FFFFFF")
        return ImageQt.ImageQt(image)

    def initGUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        #IMPORTANT: this image must exist all application lifetime:
        self.image = self.empty_image()
        pixmap = QPixmap.fromImage(self.image)
        self.image_label = QLabel()
        self.image_label.setPixmap(pixmap)
        grid.addWidget(self.image_label, 0, 0, 1, 3)
        self.name_label = QLabel('')
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        grid.addWidget(self.name_label, 1, 0, 1, 3)

        new_button = QPushButton('New image')
        new_button.clicked.connect(self.new_image_thread)
        grid.addWidget(new_button, 2, 0)
        save_button = QPushButton('Save image')
        save_button.clicked.connect(self.save_image)
        grid.addWidget(save_button, 2, 1)
        load_button = QPushButton('Load image')
        load_button.clicked.connect(self.load_file)
        grid.addWidget(load_button, 2, 2)
        self.status_label = QLabel('')
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(self.status_label, 3, 0, 1, 3)

        self.setWindowTitle('Math Artist')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.show()
        self.new_image_thread()

    def load_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Text Files (*.txt)")
        if time.time() - self.timer < 1: #prevent from very often image updates
            time.sleep(0.5)
        self.timer = time.time()
        if not filepath:
            return
        if self.draw_thread:
            self.draw_thread.stop()
        self.draw_thread.set_trigger(self.trigger)
        self.draw_thread.set_file(filepath)
        self.draw_thread.start()

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
    parser.add_argument('--file', type=str, help='Load file')
    parser.add_argument('--generate_list', action='store_true', help='Generate operators\' list (developer option)')
    return parser.parse_args()

def get_new_list():
    from operator_lists import generate_lists
    terminals, nonterminals = generate_lists()
    fulllist = terminals + nonterminals
    result = str([x.__name__ for x in fulllist])
    result = result.replace("'", "")
    result = result.replace("[", "(")
    result = result.replace("]", ")")
    return result

def get_version():
    return "%d.%d.%d" % (VERSION_MAJOR, VERSION_MINOR, VERSION_BUILD)

def get_about_info():
    return ("\n" + APP_NAME + " " + get_version() + " Copyright (C) 2018 Yaroslav Zotov.\n" +
        "Based on \"randomart\" Copyright (C) 2010, Andrej Bauer.\n"
        "This program comes with ABSOLUTELY NO WARRANTY.\n" +
        "This is free software under GNU GPL3; see the source for copying conditions\n")

if __name__ == '__main__':

    signal.signal(signal.SIGINT, sigint_handler)
    args = parse_args() #parse command line arguments
    if args.about:
        print(get_about_info())
        exit(0)
    if args.console:
        if args.generate_list:
            print(get_new_list())
            exit(0)
        art = Art(use_checker=args.checker, console=True, load_file=args.file)
    else:
        app = QApplication(sys.argv)
        window = GUI()
        sys.exit(app.exec_())
