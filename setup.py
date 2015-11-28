#!/usr/bin/env python
# For some reason, building exes with py2exe doesnt work right now.
from distutils.core import setup
import sys, os, shutil

setup(name='Digenpy',
      version='1.4.1',
      description='Python default wireless dictionary generators',
      author='David Francos Cuartero',
      author_email='me@davidfrancos.net',
      url='http://github.com/XayOn/Digenpy',
      download_url='http://github.com/XayOn/Digenpy',
      license='GPL2',
      requires=['pygtk','gettext'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
      ],
      mantainer='David Francos Cuartero (XayOn)',
      mantainer_email='xayon@xayon.net',
      long_description="Default password dictionary generator for multiple companys",
      packages=['digenpy'],
      package_data={
          'Digenpy_': ['Digenpy.ui'],
      },
      entry_points={
          'console_scripts': [
              'dgenpy = digenpy.main:cli',
          ],
          'gui_scripts': [
              'digenpy-gtk = digenpy.main:gui'
          ]
      }
)
