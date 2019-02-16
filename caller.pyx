
# distutils: language = c++

#example for cpp code

cdef extern from "example.cpp":
    void awesomeFunc()
    
cpdef myf():
    awesomeFunc()
