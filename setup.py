#!/usr/bin/env python
# For some reason, building exes with py2exe doesnt work right now.
from setuptools import setup
from distutils.command.install import INSTALL_SCHEMES
import os

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

data_files = []

for dirpath, dirnames, filenames in os.walk('digenpyweb'):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

setup(name='DigenpyWeb',
      version='0.0.1',
      description='Digenpy Web interface',
      url='http://www.digenpy.com/',
      download_url='http://www.digenpy.com',
      license='GPL2',
      requires=['Digenpy' ],
      classifiers=[
          'Development Status :: 4 - Beta',
      ],
      long_description="Digenpy dictionary generator suite web interface",
      packages=['digenpyweb'],
      data_files=data_files,
      package_data={
        'digenpyweb' : [
            'static/'
            'templates/'
            ]
      },
      entry_points="""
        [console_scripts]
        digenpyweb = digenpyweb:server
      """
     )
