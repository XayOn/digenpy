#!/usr/bin/env python
"""
    Digenpy
"""
from distutils.core import setup

setup(name='Digenpy',
      version='2.0.0',
      description='Python default wireless dictionary generators',
      author='David Francos Cuartero',
      author_email='me@davidfrancos.net',
      url='http://github.com/XayOn/Digenpy',
      download_url='http://github.com/XayOn/Digenpy',
      license='GPL2',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
      ],
      mantainer='David Francos Cuartero (XayOn)',
      mantainer_email='xayon@xayon.net',
      long_description=("Default wifi password dictionary generator"
                        " for multiple companys"),
      packages=['digenpy'],
      entry_points={
          'console_scripts': [
              'digenpy = digenpy:main',
          ],
      })
