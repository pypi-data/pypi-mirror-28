import numpy
from setuptools import setup, Extension
import os
from Cython.Build import cythonize

_ROOT = os.path.abspath(os.path.join(__file__, os.pardir))


def _get_readme():
    path = os.path.join(_ROOT, 'README.rst')
    with open(path, 'r') as f:
        return f.read()


setup(
    name='fracpy',
    author='Borodin Gregory',
    author_email='grihabor@mail.ru',
    license='MIT',
    install_requires=[
        'numpy',
        'scikit-image',
    ],
    setup_requires=[
        'pytest-runner',        
    ],         
    tests_require=[             
        'pytest',        
        'pytest-cov',         
    ],
    ext_modules=cythonize([
        Extension('fracpy.fracpy', ['fracpy/fracpy.pyx']),
        Extension('fracpy.fractals', ['fracpy/fractals.pyx']),
        Extension('fracpy.point', ['fracpy/point.pyx']),
    ]),
    packages=["fracpy"],
    version='0.0.1',
    description='Fractal library',
    long_description=_get_readme(),
)
