#!/usr/bin/env python

"""
setup.py file for GridDB python client
"""

from distutils.command.build import build

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

try:
    with open('README.rst') as f:
        readme = f.read()
except IOError:
    readme = ''

SOURCES = [
    'src/Resource.cpp',
    'src/AggregationResult.cpp',
    'src/ContainerInfo.cpp',
    'src/Container.cpp',
    'src/Store.cpp',
    'src/StoreFactory.cpp',
    'src/PartitionController.cpp',
    'src/Query.cpp',
    'src/Row.cpp',
    'src/RowKeyPredicate.cpp',
    'src/RowSet.cpp',
    'src/Timestamp.cpp',
    'src/griddb.i',
]

DEPENDENTS = [
    'src/Resource.h',
    'src/AggregationResult.h',
    'src/ContainerInfo.h',
    'src/Container.h',
    'src/Store.h',
    'src/StoreFactory.h',
    'src/PartitionController.h',
    'src/Query.h',
    'src/Row.h',
    'src/RowKeyPredicate.h',
    'src/RowSet.h',
    'src/Timestamp.h',
    'src/GSException.h',
    'src/gstype_python.i',
    'src/gstype.i',
    'include/gridstore.h',
]

INCLUDES = [
    'include',
    'src',
]

COMPILE_ARGS = [
    '-std=c++0x'
]

LIBRARIES = [
    'rt',
    'gridstore',
]

SWIG_OPTS = [
    '-DSWIGWORDSIZE64',
    '-c++',
    '-outdir',
    '.',
    '-Isrc'
]


class CustomBuild(build):
    sub_commands = [
        ('build_ext', build.has_ext_modules),
        ('build_py', build.has_pure_modules),
        ('build_clib', build.has_c_libraries),
        ('build_scripts', build.has_scripts),
    ]


griddb_module = Extension('_griddb_python_client',
                          sources=SOURCES,
                          include_dirs=INCLUDES,
                          libraries=LIBRARIES,
                          extra_compile_args=COMPILE_ARGS,
                          swig_opts=SWIG_OPTS,
                          depends=DEPENDENTS,
                          )

classifiers = [
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
]

setup(name='griddb_python_client',
      version='0.5.2',
      author='Katsuhiko Nonomura',
      author_email='contact@griddb.org',
      description='GridDB Python Client Library built using SWIG',
      ext_modules=[griddb_module],
      py_modules=['griddb_python_client'],
      url='https://github.com/griddb/griddb_client',
      cmdclass={'build': CustomBuild},
      license='Apache Software License',
      long_description=readme,
      classifiers=classifiers,
      )
