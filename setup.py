#!/usr/bin/env python

from distutils.core import setup

setup(name='python-graphviz',
    version='0.1',
    description='Python interface to the GraphViz graphing tool',
    author='Gregoire Lejeune',
    author_email='gregoire.lejeune@free.fr',
    url='https://github.com/glejeune/pyhton-graphviz',
    packages=['graphviz'],
    package_dir={'graphviz': 'src/graphviz'},
    )
