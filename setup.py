#!/usr/bin/env python

from distutils.core import setup
import sys
setup(name='Digenpy',
      version='1.0',
      description='Python default wireless dictionary generators',
      author='David Francos Cuartero (XayOn)',
      author_email='xayon@davidfrancos.net',
      url='http://github.com/XayOn/Digenpy',
      packages=['Digenpy_'],
      scripts=['digenpy', 'digenpy-gtk'],
      data_files=[(sys.prefix + '/share', ['digenpy.ui'])],
     )
