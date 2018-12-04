
#ifdef GL_FRAGMENT_PRECISION_HIGH
    precision highp float;
#endif

uniform vec2 u_resolution;

void main() {
    vec2 coord = gl_FragCoord.xy/u_resolution.xy;
    gl_FragColor = vec4(coord.xy, 0.0, 1.0); //this is result - color for vertex
}
