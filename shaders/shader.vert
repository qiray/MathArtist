
#ifdef GL_FRAGMENT_PRECISION_HIGH
    precision highp float;
#endif

attribute vec2 position;

void main() {
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex; //Calc poistion
    // gl_Position = vec4(position, 0.0, 1.0); //Calc poistion
}
