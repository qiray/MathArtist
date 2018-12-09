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

// def linear_coord(x, y, d, size, polar_shift=None):
//     u = 2 * x/size - 1.0
//     v = 2 * y/size - 1.0
//     return u, v

// def tent_coord(x, y, d, size, polar_shift=None):
//     u = 1 - 2 * abs(x/size)
//     v = 1 - 2 * abs(y/size)
//     return u, v

// def sin_coord(x, y, d, size, polar_shift=None):
//     u = math.sin(2*math.pi*x/size)
//     v = math.sin(2*math.pi*y/size)
//     return u, v

// def rotate_coord(x, y, d, size, polar_shift=None):
//     d = abs(x - y)/math.sqrt(2)
//     u = math.sqrt(8)*d/size - 1
//     v = math.sqrt(2*(x*x + y*y - d*d))/size - 1
//     return u, v

// def curved_rotate_coord(x, y, d, size, polar_shift=None):
//     u = (x - y)/size
//     v = math.sqrt(2*(x*x + y*y - u*u))/size - 1
//     return u, v

// def polar(x, y, d, size, polar_shift):
//     x -= polar_shift[0]*size
//     y -= polar_shift[1]*size
//     u = math.sqrt(x*x + y*y)/size
//     v = 0 if x == 0 else math.atan(y/x)*2/math.pi
//     return u, v

// def center(x, y, d, size, polar_shift):
//     half = size/2
//     if x >= half:
//         x = size - x
//     if y >= half:
//         y = size - y
//     u = 2 * x/half - 1.0
//     v = 2 * y/half - 1.0
//     return u, v

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

vec3 Random(vec3 color) {
    return color;
}

vec3 Palette(vec3 color) {
    return color;
}

vec3 White(vec3 color) {
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
    vec3 result = phase + freq*color;
    return result;
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

// class Wave():
//     arity = 2
//     mindepth = 0
//     def __init__(self, e1, e2):
//         self.e1 = e1
//         self.e2 = e2
//     def __repr__(self):
//         return 'Wave(%s, %s)' % (self.e1, self.e2)
//     def eval(self, x, y):
//         (r1, g1, b1) = self.e1.eval(x, y)
//         (r2, g2, b2) = self.e2.eval(x, y)
//         return (wave(r1, r2), wave(g1, g2), wave(b1, b2))

// class Level():
//     arity = 3
//     mindepth = 0
//     def __init__(self, level, e1, e2, treshold = None):
//         self.treshold = treshold if treshold else random.uniform(-1.0, 1.0) #for parsing
//         self.level = level
//         self.e1 = e1
//         self.e2 = e2
//     def __repr__(self):
//         return 'Level(%s, %s, %s, %g)' % (self.level, self.e1, self.e2, self.treshold)
//     def eval(self, x, y):
//         (r1, g1, b1) = self.level.eval(x, y)
//         (r2, g2, b2) = self.e1.eval(x, y)
//         (r3, g3, b3) = self.e2.eval(x, y)
//         r4 = r2 if r1 < self.treshold else r3
//         g4 = g2 if g1 < self.treshold else g3
//         b4 = b2 if b1 < self.treshold else b3
//         return (r4, g4, b4)

// class Mix():
//     arity = 3
//     mindepth = 0
//     def __init__(self, w, e1, e2):
//         self.w = w
//         self.e1 = e1
//         self.e2 = e2
//     def __repr__(self):
//         return 'Mix(%s, %s, %s)' % (self.w, self.e1, self.e2)
//     def eval(self, x, y):
//         w = 0.5 * (self.w.eval(x, y)[0] + 1.0)
//         c1 = self.e1.eval(x, y)
//         c2 = self.e2.eval(x, y)
//         return average(c1, c2, w)

// class RGB():
//     arity = 3
//     mindepth = 4
//     def __init__(self, e1, e2, e3):
//         self.e1 = e1
//         self.e2 = e2
//         self.e3 = e3
//     def __repr__(self):
//         return 'RGB(%s, %s, %s)' % (self.e1, self.e2, self.e3)
//     def eval(self, x, y):
//         (r, _, _) = self.e1.eval(x, y)
//         (_, g, _) = self.e2.eval(x, y)
//         (_, _, b) = self.e3.eval(x, y)
//         return (r, g, b)

// class Closest():
//     arity = 3
//     mindepth = 3
//     def __init__(self, target, e1, e2):
//         self.target = target
//         self.e1 = e1
//         self.e2 = e2
//     def __repr__(self):
//         return 'Closest(%s, %s, %s)' % (self.target, self.e1, self.e2)
//     def eval(self, x, y):
//         (r1, g1, b1) = self.target.eval(x, y)
//         (r2, g2, b2) = self.e1.eval(x, y)
//         (r3, g3, b3) = self.e2.eval(x, y)
//         #distances between colors:
//         d1 = math.sqrt((r2-r1)**2+(g2-g1)**2+(b2-b1)**2)
//         d2 = math.sqrt((r3-r1)**2+(g3-g1)**2+(b3-b1)**2)

//         return (r2, g2, b2) if d1 < d2 else (r3, g3, b3)

// class Far():
//     arity = 3
//     mindepth = 3
//     def __init__(self, target, e1, e2):
//         self.target = target
//         self.e1 = e1
//         self.e2 = e2
//     def __repr__(self):
//         return 'Far(%s, %s, %s)' % (self.target, self.e1, self.e2)
//     def eval(self, x, y):
//         (r1, g1, b1) = self.target.eval(x, y)
//         (r2, g2, b2) = self.e1.eval(x, y)
//         (r3, g3, b3) = self.e2.eval(x, y)
//         #distances between colors:
//         d1 = math.sqrt((r2-r1)**2+(g2-g1)**2+(b2-b1)**2)
//         d2 = math.sqrt((r3-r1)**2+(g3-g1)**2+(b3-b1)**2)

//         return (r2, g2, b2) if d1 > d2 else (r3, g3, b3)

void main() {
    vec2 coord = gl_FragCoord.xy / u_resolution; //calc coords [0; 1]
    vec2 pos = 2.0*coord.xy - 1.0; //linear coord conversion: [-1; 1]
    x = vec3(pos.x); //use global x, y
    y = vec3(pos.y);
    //TODO: replace formula, coord_system 
    // vec3 result = $FORMULA$;
    vec3 result = Well(Tent(x));
    vec3 color = 0.5*result + 0.5; //[-1; 1] -> [1,1]
    gl_FragColor = vec4(color, 1); //color for vertex
}
