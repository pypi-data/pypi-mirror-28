import os
from setuptools import find_packages, setup, Extension
from setuptools.command.build_ext import build_ext

version = '0.1.4'
README = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = open(README).read() + '\n'


class cythonize_build_ext(build_ext):
    """
    Custom extension building class which applies `cythonize()` do Cython
    extensions after dependencies from `setup_requires` are installed. This
    allows installing morpy in environments where numpy and Cython are not
    already installed.

    Inspired from https://stackoverflow.com/a/21621689/1819351
    """
    def finalize_options(self):
        from Cython.Build import cythonize
        import numpy
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        build_ext.finalize_options(self)
        self.include_dirs.append(numpy.get_include())
        self.extensions = cythonize(self.extensions)

        # Some combinations of Cython & setuptools version require this
        for ext in self.extensions:
            ext._needs_stub = False


cmdclass = { 'build_ext': cythonize_build_ext }
ext_modules = [
    Extension("morpy.cmorton",
              sources=["morpy/cmorton.pyx"],
              extra_compile_args=["-std=c99"],
              )
]
install_requires = [
    'numpy>=1.9.0',
]
setup_requires = install_requires + [
    'Cython>=0.22',
]

setup(name='morpy',
      version=version,
      description=("Morton Curve Library"),
      long_description=long_description,
      cmdclass = cmdclass,
      ext_modules=ext_modules,
      setup_requires=setup_requires,
      install_requires=install_requires,
      classifiers=[
          "Programming Language :: Python",
          ("Topic :: Software Development :: Libraries :: Python Modules"),
      ],
      keywords=['space filling curve','morton'],
      author='Samuel Skillman <samskillman@gmail.com>',
      license='MIT',
      packages=find_packages(),
      )
