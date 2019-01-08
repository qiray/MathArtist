from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext

# python3 setup.py build_ext --inplace
 
setup(
    ext_modules = [
        Extension(
            'common',
            sources =["common.pyx"],
            extra_compile_args=['-O3'],
        ),
        Extension(
            'operators',
            sources =["operators.pyx"],
            extra_compile_args=['-O3'],
        )
    ],
    cmdclass = {'build_ext': build_ext}
)