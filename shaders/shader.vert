
#ifdef GL_FRAGMENT_PRECISION_HIGH
    precision highp float;
#endif

attribute vec2 position;

varying vec4 vertex_color;

void main() {
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    vertex_color = gl_Color;
}
