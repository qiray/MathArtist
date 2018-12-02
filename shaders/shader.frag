
#ifdef GL_FRAGMENT_PRECISION_HIGH
    precision highp float;
#endif

varying vec4 vertex_color; //this variable is shared between vert and frag

void main() {
    gl_FragColor = vertex_color; //this is result - color for vertex
}
