#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication, QLabel)
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageDraw, ImageQt

class GUI(QWidget):

    def __init__(self):
        super().__init__()
        self.initGUI()

    def generate_image(self):
        #TODO: rewrite with normal image generating
        size = 512
        self.img = Image.new('RGB', (size, size))
        self.image_draw = ImageDraw.Draw(self.img)
        self.image_draw.rectangle(
            ((0, 0), (25, 40)),
            fill="#ff0000"
        )
        return ImageQt.ImageQt(self.img)

    def initGUI(self):
        #TODO: add 2 tabs: with canvas and generate/save buttons and with settings such as read file etc.
        grid = QGridLayout()
        self.setLayout(grid)

        self.image = self.generate_image() #IMPORTANT: this image must exist all application lifetime
        pixmap = QPixmap.fromImage(self.image)
        # pixmap = QPixmap("2018-11-06 00-17.png")
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        grid.addWidget(image_label, 0, 0, 1, 2)

        new_button = QPushButton('New image')
        grid.addWidget(new_button, 1, 0)
        save_button = QPushButton('Save image')
        grid.addWidget(save_button, 1, 1)

        self.setWindowTitle('Math Artist')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GUI()
    sys.exit(app.exec_())
