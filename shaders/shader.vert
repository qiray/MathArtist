#version 120

#ifdef GL_FRAGMENT_PRECISION_HIGH
    precision highp float;
#endif

void main() {
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex; //Calc poistion
}
