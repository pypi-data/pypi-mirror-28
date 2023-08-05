#!/usr/bin/env python

import os, glob
from setuptools import setup, find_packages, Extension
from codecs import open


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

try:
    import __pypy__, sys
    version = sys.pypy_version_info
    if version[0] == 5 and version[1] <= 9:
        requirements = ['cppyy-backend<0.3']
        add_pkg = ['cppyy', 'cppyy_compat']
    else:
        requirements = ['cppyy-backend']
        add_pkg = ['cppyy']
except ImportError:
    # CPython
    requirements = ['CPyCppyy']
    add_pkg = ['cppyy']

setup(
    name='cppyy',
    version='0.8.7',
    description='Cling-based Python-C++ bindings',
    long_description=long_description,

    url='http://cppyy.readthedocs.org',

    # Author details
    author='Wim Lavrijsen',
    author_email='WLavrijsen@lbl.gov',

    license='LBNL BSD',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'Topic :: Software Development',
        'Topic :: Software Development :: Interpreters',

        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: C',
        'Programming Language :: C++',

        'Natural Language :: English'
    ],

    install_requires=requirements,

    keywords='C++ bindings',

    package_dir={'': 'python'},
    packages=find_packages('python', include=add_pkg),
)
