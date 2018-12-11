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
import time
import webbrowser

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QIcon, QOpenGLContext
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication,
    QLabel, QFileDialog, QMessageBox, QTextEdit, QOpenGLWidget)
from PyQt5.QtCore import QThread, pyqtSignal

import OpenGL.GL as gl

from art import Art, APP_NAME, VERSION_MAJOR, VERSION_MINOR, VERSION_BUILD
from common import SIZE

#TODO: draw OpenGL without GUI
#TODO: draw in another thread

class DrawThread(QThread):
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        pass

    def stop(self):
        self.wait()

class GUI(QWidget):
    init_trigger = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.draw_thread = DrawThread()
        self.glWidget = GLWidget(self.init_trigger)
        # self.context = self.glWidget.context()
        # print(self.context)
        # self.context.moveToThread(self.draw_thread)
        self.art = Art(use_checker=True)

        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self.glWidget, 0, 0, 1, 2)

        new_button = QPushButton('Random image')
        new_button.clicked.connect(self.new_image)
        grid.addWidget(new_button, 2, 0)
        new_button2 = QPushButton('Generate image')
        new_button2.clicked.connect(self.save_image)
        grid.addWidget(new_button2, 2, 1)
        save_button = QPushButton('Save image')
        save_button.clicked.connect(self.save_image)
        grid.addWidget(save_button, 3, 0)
        load_button = QPushButton('Load image')
        load_button.clicked.connect(self.save_image)
        grid.addWidget(load_button, 3, 1)
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignCenter)
        grid.addWidget(self.status_label, 4, 0, 1, 2)

        self.name_label = QTextEdit('')
        self.name_label.setMaximumHeight(self.status_label.sizeHint().height()*3)
        grid.addWidget(self.name_label, 1, 0, 1, 2)

        self.setWindowTitle('Math Artist')
        self.setWindowIcon(QIcon('icon.ico'))
        self.init_trigger.connect(self.new_image) #connect signal and slot

    def new_image(self):
        start = time.time()
        self.art.prepare()
        self.art.print_art()
        self.status_label.setText("Generation finished in %g s" %(time.time() - start))
        self.name_label.setText(self.art.name)
        self.glWidget.initGL(self.art.get_art_as_object())
        self.glWidget.paintGL()
        self.status_label.setText("Drawing finished in %g s" %(time.time() - start))

    def save_image(self):
        image = self.glWidget.grabFramebuffer()
        image.save("output/1.png")

    def keyPressEvent(self, event): #Handle keys
        key = event.key()
        # modifiers = QApplication.keyboardModifiers() #modifiers == QtCore.Qt.ControlModifier
        if key == Qt.Key_Escape:
            print("Closing...")
            self.close()
        elif key == Qt.Key_N or key == Qt.Key_R:
            self.new_image()
        elif key == Qt.Key_G:
            self.new_image_name_thread()
        elif key == Qt.Key_O:
            self.load_file()
        elif key == Qt.Key_S:
            self.save_image()
        elif key == Qt.Key_A:
            self.show_about_message()
        elif key == Qt.Key_F1:
            self.show_online_help()
        event.accept()

    def show_about_message(self):
        QMessageBox.about(self, 'About', get_about_info())

    def show_online_help(self):
        webbrowser.open('http://google.com') #TODO: open github readme

class GLWidget(QOpenGLWidget):

    def __init__(self, init_trigger=None, parent=None):
        super().__init__()
        super(GLWidget, self).__init__(parent)
        self.init_trigger = init_trigger
        self.setMinimumSize(QSize(SIZE, SIZE))
        self.setMaximumSize(QSize(SIZE, SIZE))

    def getOpenglInfo(self):
        info = """
            Vendor: {0}
            Renderer: {1}
            OpenGL Version: {2}
            Shader Version: {3}
        """.format(
            gl.glGetString(gl.GL_VENDOR),
            gl.glGetString(gl.GL_RENDERER),
            gl.glGetString(gl.GL_VERSION),
            gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION)
        )

        return info

    def initializeGL(self):
        print(self.getOpenglInfo())
        self.setClearColor(QColor.fromRgb(255, 255, 255)) #set background
        # Verticles array:
        self.pointdata = [[-1.0, -1.0], [-1.0, 1.0], [1.0, 1.0], [1.0, -1.0]]
        self.program = 0
        self.vertex = 0
        self.fragment = 0
        self.initGL()
        if self.init_trigger:
            self.init_trigger.emit() #emit signal

    def initGL(self, art_object=None):
        start = time.time()
        with open('shaders/shader.frag', 'r') as shader_file:
            frag_source = shader_file.read()
        if art_object:
            self.makeCurrent() #IMPORTANT: set focus to change widget
            gl.glDeleteProgram(self.program)
            gl.glDeleteShader(self.vertex)
            gl.glDeleteShader(self.fragment)
            frag_source = frag_source.replace("$POLAR_SHIFT$", art_object['shift']).replace("$COORD$", art_object['coord']).replace("$FORMULA$", art_object['formula'])
        else:
            frag_source = frag_source.replace("$POLAR_SHIFT$", "(0, 0)").replace("$COORD$", "linear_coord").replace("$FORMULA$", "White(1, 1, 1)")
        self.vertex = create_shader_from_file(gl.GL_VERTEX_SHADER, 'shaders/shader.vert') #create vertex shader
        self.fragment = create_shader_from_source(gl.GL_FRAGMENT_SHADER, frag_source) #create fragment shader
        self.program = gl.glCreateProgram() #Create empty GL program
        gl.glAttachShader(self.program, self.vertex) #attach vertex shader to program
        gl.glAttachShader(self.program, self.fragment) #attach fragment shader to program
        gl.glLinkProgram(self.program) #Link shader program
        #check errors:
        if gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS) == gl.GL_FALSE:
            print(gl.glGetProgramInfoLog(self.program))
            #TODO: save log with art object
            exit(1)
        try: #It can fail on some OpenGL versions
            gl.glUseProgram(self.program) #Use this program
        except:
            pass
        resolution = gl.glGetUniformLocation(self.program, 'u_resolution') #register uniform
        gl.glUniform2i(resolution, SIZE, SIZE) #pass resolution value to shaders
        print("Time for compiling:", time.time() - start)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)                    # Clear screen
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)            # Enable using vertex array
        #2 coords per vertex, use float type, 0 stride, use self.pointdata as data array:
        gl.glVertexPointer(2, gl.GL_FLOAT, 0, self.pointdata)
        gl.glDrawArrays(gl.GL_QUADS, 0, 4)
        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

    def setClearColor(self, c):
        gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

def create_shader_from_source(shader_type, source):
    '''Create shader from source code. 
    shader_type should be gl.GL_VERTEX_SHADER or gl.GL_FRAGMENT_SHADER
    '''
    shader = gl.glCreateShader(shader_type) #create empty shader
    gl.glShaderSource(shader, source) # Get source and pass it to shader
    gl.glCompileShader(shader) #compile shader
    return shader #return compiled result

def create_shader_from_file(shader_type, path):
    '''Create shader from source file'''
    with open(path, 'r') as shader_file:
        source = shader_file.read()
    return create_shader_from_source(shader_type, source)

def get_version():
    return "%d.%d.%d" % (VERSION_MAJOR, VERSION_MINOR, VERSION_BUILD)

def get_about_info():
    return ("\n" + APP_NAME + " " + get_version() + " Copyright (C) 2018 Yaroslav Zotov.\n" +
        "Based on \"randomart\" Copyright (C) 2010, Andrej Bauer.\n"
        "This program comes with ABSOLUTELY NO WARRANTY.\n" +
        "This is free software under GNU GPL3; see the source for copying conditions\n")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())
