#version 130

#ifdef GL_FRAGMENT_PRECISION_HIGH
    precision highp float;
#endif

void main() {
    // gl_Position = vec4(-1, -1, -1, 1)*gl_ModelViewProjectionMatrix * gl_Vertex; //Calc poistion
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex * vec4 (1.0, -1.0, 1.0, 1.0); //Calc poistion
}
