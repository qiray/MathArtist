
# distutils: language = c++

#example for cpp code

cdef extern from "example.cpp":
    void cppFunc()

cpdef call_cpp():
    cppFunc()
