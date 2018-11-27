
# Formula: Mix(Well(Mix(Well(Mix(Mix(y, y, y), Well(y), Mix(y, y, x))), Well(Well(Mix(x, y, y))), Well(Mix(Well(x), Well(x), Well(x))))), Well(Mix(Well(Mix(Mix(y, x, y), Mix(x, y, y), Well(x))), Mix(Well(Mix(x, x, y)), Mix(Well(y), Mix(x, y, y), Mix(x, y, x)), Well(Mix(y, x, y))), Well(Well(Well(x))))), Well(Mix(Mix(Mix(Well(x), Mix(y, x, x), Mix(x, x, x)), Mix(Well(x), Mix(y, y, y), Well(x)), Mix(Mix(y, y, y), Well(x), Well(x))), Well(Mix(Well(x), Well(y), Mix(y, x, x))), Well(Mix(Mix(x, x, y), Well(x), Mix(x, y, y))))))

cimport libc.math as cmath
import time

ctypedef (double, double, double) color

cpdef double well(double x):
    '''A function which looks a bit like a well.'''
    cdef double result = 1 - 2 / cmath.pow(1 + x*x, 8)
    result = 1 if result < -1 else result
    return result

cpdef color average(color c1, color c2, double w=0.5):
    '''Compute the weighted average of two colors. With w = 0.5 we get the average.'''
    (r1, g1, b1) = c1
    (r2, g2, b2) = c2
    cdef double r3 = w * r1 + (1 - w) * r2
    cdef double g3 = w * g1 + (1 - w) * g2
    cdef double b3 = w * b1 + (1 - w) * b2
    return (r3, g3, b3)

cpdef polar(double x, double y, int size):
    cdef double u = cmath.sqrt(x*x + y*y)/size
    cdef double v = 0 if x == 0 else cmath.atan(y/x)*2/cmath.pi
    return u, v

# class VariableX():
#     arity = 0
#     mindepth = 4
#     def __init__(self):
#         pass
#     def __repr__(self):
#         return "x"
#     def eval(self, x, y):
#         return (x, x, x)

# class VariableY():
#     arity = 0
#     mindepth = 4
#     def __init__(self):
#         pass
#     def __repr__(self):
#         return "y"
#     def eval(self, x, y):
#         return (y, y, y)

# class Well():
#     arity = 1
#     mindepth = 3
#     def __init__(self, e):
#         self.e = e
#     def __repr__(self):
#         return 'Well(%s)' % self.e
#     def eval(self, x, y):
#         (r, g, b) = self.e.eval(x, y)
#         return (well(r), well(g), well(b))

# class Mix():
#     arity = 3
#     mindepth = 0
#     def __init__(self, w, e1, e2):
#         self.w = w
#         self.e1 = e1
#         self.e2 = e2
#     def __repr__(self):
#         return 'Mix(%s, %s, %s)' % (self.w, self.e1, self.e2)
#     def eval(self, x, y):
#         w = 0.5 * (self.w.eval(x, y)[0] + 1.0)
#         c1 = self.e1.eval(x, y)
#         c2 = self.e2.eval(x, y)
#         return average(c1, c2, w)

cdef class VariableX():
    cdef int iarity
    cdef int mindepth
    def __cinit__(self):
        iarity = 0
        mindepth = 4
    def __repr__(self):
        return "x"
    def eval(self, x, y):
        return (x, x, x)

cdef class VariableY():
    cdef int iarity
    cdef int mindepth
    def __cinit__(self):
        arity = 0
        mindepth = 4
    def __repr__(self):
        return "y"
    def eval(self, x, y):
        return (y, y, y)

cdef class Well():
    cdef int iarity
    cdef int mindepth
    cdef object e
    def __cinit__(self, e):
        arity = 1
        mindepth = 3
        self.e = e
    def __repr__(self):
        return 'Well(%s)' % self.e
    def eval(self, x, y):
        (r, g, b) = self.e.eval(x, y)
        return (well(r), well(g), well(b))

cdef class Mix():
    cdef int iarity
    cdef int mindepth
    cdef object w, e1, e2
    def __cinit__(self, w, e1, e2):
        arity = 3
        mindepth = 0
        self.w = w
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return 'Mix(%s, %s, %s)' % (self.w, self.e1, self.e2)
    def eval(self, x, y):
        cdef double weight = 0.5 * (self.w.eval(x, y)[0] + 1.0)
        cdef color c1 = self.e1.eval(x, y)
        cdef color c2 = self.e2.eval(x, y)
        return average(c1, c2, weight)

art = Mix(Well(Mix(Well(Mix(Mix(VariableY(), VariableY(), VariableY()), Well(VariableY()), Mix(VariableY(), VariableY(), VariableX()))), Well(Well(Mix(VariableX(), VariableY(), VariableY()))), Well(Mix(Well(VariableX()), Well(VariableX()), Well(VariableX()))))), Well(Mix(Well(Mix(Mix(VariableY(), VariableX(), VariableY()), Mix(VariableX(), VariableY(), VariableY()), Well(VariableX()))), Mix(Well(Mix(VariableX(), VariableX(), VariableY())), Mix(Well(VariableY()), Mix(VariableX(), VariableY(), VariableY()), Mix(VariableX(), VariableY(), VariableX())), Well(Mix(VariableY(), VariableX(), VariableY()))), Well(Well(Well(VariableX()))))), Well(Mix(Mix(Mix(Well(VariableX()), Mix(VariableY(), VariableX(), VariableX()), Mix(VariableX(), VariableX(), VariableX())), Mix(Well(VariableX()), Mix(VariableY(), VariableY(), VariableY()), Well(VariableX())), Mix(Mix(VariableY(), VariableY(), VariableY()), Well(VariableX()), Well(VariableX()))), Well(Mix(Well(VariableX()), Well(VariableY()), Mix(VariableY(), VariableX(), VariableX()))), Well(Mix(Mix(VariableX(), VariableX(), VariableY()), Well(VariableX()), Mix(VariableX(), VariableY(), VariableY()))))))

print (art)

size = 512
start = time.time()
for x in range(size):
    for y in range(size):
        u, v = polar(x, y, size)
        result = art.eval(u, v)
print(time.time() - start)
