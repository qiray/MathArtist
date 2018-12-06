
#ifdef GL_FRAGMENT_PRECISION_HIGH
    precision highp float;
#endif

uniform ivec2 u_resolution; //pass widget resolution from main program

float wellf(float x) {
    float result = 1.0 - (2.0 / pow(1.0 + x*x, 8.0));
    return result < -1 ? 1 : result;
}

float tentf(float x) {
    return 1.0 - 2.0 * abs(x);
}

vec3 Well(vec3 color) {
    return vec3(wellf(color.r), wellf(color.g), wellf(color.b));
}

vec3 Tent(vec3 color) {
    return vec3(tentf(color.r), tentf(color.g), tentf(color.b));
}

void main() {
    vec2 coord = gl_FragCoord.xy / u_resolution; //calc coords [0; 1]
    vec2 pos = 2.0*coord.xy - 1.0; //linear coord conversion: [-1; 1]
    // vec3 result = $FORMULA$;
    vec3 result = Well(Tent(vec3(pos.x)));
    gl_FragColor = vec4(result.rgb, 1.0); //result - color for vertex
}
