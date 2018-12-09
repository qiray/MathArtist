#version 130

#ifdef GL_FRAGMENT_PRECISION_HIGH
    precision highp float;
#endif

uniform ivec2 u_resolution; //pass widget resolution from main program

#define M_PI 3.1415926535897932384626433832795

#define AND 1
#define OR 2
#define XOR 3

//We made them globals for Chess function
vec3 x = vec3(0.0);
vec3 y = vec3(0.0);

//////////////////////////////// Coords: ////////////////////////////////

vec2 polar_shift = vec2(1.0, 0.0);

// gl_FragCoord - current coordinates
// u_resolution - widget size
//hack for flipping y axis:
vec2 current_coord = vec2(gl_FragCoord.x, u_resolution.y - gl_FragCoord.y);

vec2 linear_coord() {
    return 2.0*current_coord.xy / u_resolution - 1.0; //linear coord conversion: [-1; 1]
}

vec2 tent_coord() {
    return 1 - 2 * abs(current_coord.xy / u_resolution);
}

vec2 sin_coord() {
    return sin(2*M_PI*current_coord.xy / u_resolution);
}

vec2 rotate_coord() {
    float d = abs(current_coord.x - current_coord.y)/sqrt(2);
    float u = sqrt(8)*d/u_resolution.x - 1.0;
    float v = sqrt(2*(pow(current_coord.x, 2) + pow(current_coord.y, 2) - d*d))/u_resolution.x - 1.0;
    return vec2(u, 1.0 - v);
}

vec2 curved_rotate_coord() {
    float u = (current_coord.x - current_coord.y)/u_resolution.x;
    float v = sqrt(2*(pow(current_coord.x, 2) + pow(current_coord.y, 2) - u*u))/u_resolution.x - 1.0;
    return vec2(u, v);
}

vec2 polar() {
    float x = current_coord.x - polar_shift.x*u_resolution.x;
    float y = current_coord.y - polar_shift.y*u_resolution.y;
    float u = sqrt(x*x + y*y)/u_resolution.x;
    float v = x == 0 ? 0 : atan(y/x)*2/M_PI;
    return vec2(u, v);
}

vec2 center() {
    int halfsize = (u_resolution.x)/2;
    float x = current_coord.x;
    float y = current_coord.y;
    if (x >= halfsize)
        x = u_resolution.x - x;
    if (y >= halfsize)
        y = u_resolution.y - y;
    float u = 2 * x/halfsize - 1.0;
    float v = 2 * y/halfsize - 1.0;
    return vec2(u, v);
}

//////////////////////////////// Common: ////////////////////////////////

float wellf(float x) {
    float result = 1.0 - (2.0 / pow(1.0 + x*x, 8.0));
    return result < -1.0 ? 1.0 : result;
}

float tentf(float x) {
    return 1.0 - 2.0 * abs(x);
}

float sin_curve(float x) {
    float val = x != 0 ? x : 1;
    return sin(1.0/val);
}

float abs_sin(float x) {
    return sin(abs(x));
}

float wave(float x, float y) {
    return sin(sqrt(x*x + y*y));
}

//Colors:

int float_color_to_int(float c) {
    return max(0, min(255, int(128 * (c + 1))));
}

vec3 average_weighted(vec3 c1, vec3 c2, float w) {
    //Compute the weighted average of two colors. With w = 0.5 we get the average.
    return w * c1 + (1.0 - w)*c2;
}

vec3 average(vec3 c1, vec3 c2) {
    return 0.5 * c1 + 0.5*c2;
}

vec3 color_binary(vec3 c1, vec3 c2, int operator) {
    ivec3 color1 = ivec3(float_color_to_int(c1.r), float_color_to_int(c1.g), float_color_to_int(c1.b));
    ivec3 color2 = ivec3(float_color_to_int(c2.r), float_color_to_int(c2.g), float_color_to_int(c2.b));
    switch(operator) {
        case AND:
            return 2.0*(color1 & color2)/255.0 - 1.0;
        case OR:
            return 2.0*(color1 | color2)/255.0 - 1.0;
        case XOR:
            return 2.0*(color1 ^ color2)/255.0 - 1.0;
    }
    return vec3(0.0);
}

//////////////////////////////// Operators: ////////////////////////////////

// Terminals:

vec3 Random(float r, float g, float b) {
    return vec3(r, g, b);
}

vec3 Palette(float r, float g, float b) {
    return vec3(r, g, b);
}

vec3 White(float r, float g, float b) {
    return vec3(1.0, 1.0, 1.0);
}

vec3 Chess(float wX, float wY) {
    int isOdd = 0;
    isOdd ^= int(floor(x/wX)) & 1;
    isOdd ^= int(floor(y/wY)) & 1;
    return isOdd != 0 ? vec3(-1.0) : vec3(1.0);
}

// Nonterminals:

vec3 Well(vec3 color) {
    return vec3(wellf(color.r), wellf(color.g), wellf(color.b));
}

vec3 Tent(vec3 color) {
    return vec3(tentf(color.r), tentf(color.g), tentf(color.b));
}

vec3 Sin(vec3 color, float phase, float freq) {
    return sin(phase + freq*color);
}

vec3 Not(vec3 color) {
    return -color;
}

vec3 SinCurve(vec3 color) {
    return vec3(sin_curve(color.r), sin_curve(color.g), sin_curve(color.b));
}

vec3 AbsSin(vec3 color) {
    return vec3(abs_sin(color.r), abs_sin(color.g), abs_sin(color.b));
}

vec3 Atan(vec3 color) {
    return vec3(atan(color.r)*2/M_PI, atan(color.g)*2/M_PI, atan(color.b)*2/M_PI);
}

vec3 Sum(vec3 color1, vec3 color2) {
    return average(color1, color2);
}

vec3 Product(vec3 color1, vec3 color2) {
    return color1*color2;
}

vec3 Mod(vec3 color1, vec3 color2) {
    if ((color2 == vec3(0.0)))
        return vec3(0.0);
    return mod(color1, color2);
}

vec3 And(vec3 color1, vec3 color2) {
    return color_binary(color1, color2, AND);
}

vec3 Or(vec3 color1, vec3 color2) {
    return color_binary(color1, color2, OR);
}

vec3 Xor(vec3 color1, vec3 color2) {
    return color_binary(color1, color2, XOR);
}

vec3 Wave(vec3 c1, vec3 c2) {
    return vec3(wave(c1.r, c2.r), wave(c1.g, c2.g), wave(c1.b, c2.b));
}

vec3 Level(vec3 level, vec3 c1, vec3 c2, float treshold) {
    float r = level.r < treshold ? c1.r : c2.r;
    float g = level.g < treshold ? c1.g : c2.g;
    float b = level.b < treshold ? c1.b : c2.b;
    return vec3(r, g, b);
}

vec3 Mix(vec3 w, vec3 color1, vec3 color2) {
    float weight = 0.5 * (w[0] + 1.0);
    return average_weighted(color1, color2, weight);
}

vec3 RGB(vec3 c1, vec3 c2, vec3 c3) {
    return vec3(c1.r, c2.g, c3.b);
}

vec3 Closest(vec3 target, vec3 c1, vec3 c2) {
    float d1 = sqrt(pow(c1.r - target.r, 2) + pow(c1.g - target.g, 2) + pow(c1.b - target.b, 2));
    float d2 = sqrt(pow(c2.r - target.r, 2) + pow(c2.g - target.g, 2) + pow(c2.b - target.b, 2));
    return d1 < d2 ? c1 : c2;
}

vec3 Far(vec3 target, vec3 c1, vec3 c2) {
    float d1 = sqrt(pow(c1.r - target.r, 2) + pow(c1.g - target.g, 2) + pow(c1.b - target.b, 2));
    float d2 = sqrt(pow(c2.r - target.r, 2) + pow(c2.g - target.g, 2) + pow(c2.b - target.b, 2));
    return d1 > d2 ? c1 : c2;
}

//////////////////////////////// Main: ////////////////////////////////

void main() {
    vec2 coord = linear_coord();
    x = vec3(coord.x); //use global x, y
    y = vec3(coord.y);
    //TODO: replace formula, coord_system, polar_shift
    // vec3 result = $FORMULA$;
    vec3 result = Chess(0.5, 0.1); //TODO: fix Chess function
    vec3 color = 0.5*result + 0.5; //[-1; 1] -> [1,1]
    gl_FragColor = vec4(color, 1); //Result - color for vertex
}
