
#ifdef GL_FRAGMENT_PRECISION_HIGH
    precision highp float;
#endif

uniform vec2 u_resolution; //pass widget resolution from main program

void main() {
    vec2 coord = gl_FragCoord.xy / u_resolution; //calc coords [0; 1]
    gl_FragColor = vec4(coord.xy, 0.0, 1.0); //result - color for vertex
}
