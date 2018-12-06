#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2015 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################

import sys
import math

from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QOpenGLWidget, QSlider,
                             QWidget, QPushButton)

import OpenGL.GL as gl

SIZE = 512

#pip install PyOpenGL

#Some material from https://habr.com/post/247123/

#TODO: read https://thebookofshaders.com/02/

class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()

        self.glWidget = GLWidget()

        new_button = QPushButton('Save image')
        new_button.clicked.connect(self.save_image)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.glWidget)
        mainLayout.addWidget(new_button)
        self.setLayout(mainLayout)

        self.setWindowTitle("Hello GL")

    def save_image(self):
        image = self.glWidget.grabFramebuffer()
        image.save("1.png")

    def keyPressEvent(self, event): #Handle keys
        key = event.key()
        if key == Qt.Key_Escape:
            print("Closing...")
            self.close()
        event.accept()


class GLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.bgcolor = QColor.fromRgb(100, 100, 100)
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
        self.setClearColor(self.bgcolor)
        self.initGL()

    def paintGL(self):
        print("Redrawing")
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)                    # Clear screen
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)            # Включаем использование массива вершин
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)             # Включаем использование массива цветов
        # Указываем, где взять массив вершин:
        # Первый параметр - сколько используется координат на одну вершину
        # Второй параметр - определяем тип данных для каждой координаты вершины
        # Третий парметр - определяет смещение между вершинами в массиве
        # Если вершины идут одна за другой, то смещение 0
        # Четвертый параметр - указатель на первую координату первой вершины в массиве
        gl.glVertexPointer(3, gl.GL_FLOAT, 0, self.pointdata)
        # Указываем, где взять массив цветов:
        # Параметры аналогичны, но указывается массив цветов
        gl.glColorPointer(3, gl.GL_FLOAT, 0, self.pointcolor)
        # First param - data type, 2nd - start index, 3rd - verticles count
        gl.glDrawArrays(gl.GL_QUADS, 0, 4)
        gl.glDisableClientState(gl.GL_VERTEX_ARRAY) 
        gl.glDisableClientState(gl.GL_COLOR_ARRAY) 

    def initGL(self):
        vertex = create_shader_from_file(gl.GL_VERTEX_SHADER, 'shader.vert') #create vertex shader
        fragment = create_shader_from_file(gl.GL_FRAGMENT_SHADER, 'shader.frag') #create fragment shader
        # Создаем пустой объект шейдерной программы
        program = gl.glCreateProgram()
        # Приcоединяем вершинный шейдер к программе
        gl.glAttachShader(program, vertex)
        # Присоединяем фрагментный шейдер к программе
        gl.glAttachShader(program, fragment)
        # "Собираем" шейдерную программу
        gl.glLinkProgram(program)
        # Сообщаем OpenGL о необходимости использовать данную шейдерную программу при отрисовке объектов
        try: #It can fail on some OpenGL versionss
            gl.glUseProgram(program)
        except:
            pass

        resolution = gl.glGetUniformLocation(program, 'u_resolution') #register uniform
        gl.glUniform2i(resolution, SIZE, SIZE) #pass resolution value to shaders
        
        # Verticles array
        self.pointdata = [[-1.0, -1.0, 0], [-1.0, 1.0, 0], [1.0, 1.0, 0], [1.0, -1.0, 0]]
        # Colors array
        self.pointcolor = [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]

    def setClearColor(self, c):
        gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, c):
        gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())

def create_shader_from_source(shader_type, source):
    '''Create shader from source code'''
    # Создаем пустой объект шейдера
    shader = gl.glCreateShader(shader_type)
    # Привязываем текст шейдера к пустому объекту шейдера
    gl.glShaderSource(shader, source)
    # Компилируем шейдер
    gl.glCompileShader(shader)
    # Возвращаем созданный шейдер
    return shader

def create_shader_from_file(shader_type, path):
    '''Create shader from source file'''
    with open(path, 'r') as shader_file:
        source = shader_file.read()
    return create_shader_from_source(shader_type, source)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
