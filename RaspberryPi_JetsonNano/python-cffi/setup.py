#!/usr/bin/env python

import os
import sys

from setuptools import setup, find_packages

os.chdir(os.path.dirname(sys.argv[0]) or '.')

setup(
  name='waveshare-epaper-cffi',
  version='0.0.1',
  description="Python FFI bindings for Waveshare's C libraries",
  long_description=open('README.md', 'rt').read(),
  url='https://github.com/waveshare/e-paper',
  author='Jochen Keil',
  author_email='jochen.keil@gmail.com',
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: BSD License',
  ],
  packages=find_packages(where='src'),
  install_requires=['cffi>=1.0.0'],
  setup_requires=['cffi>=1.0.0'],
  cffi_modules=[
    'src/DEV_Config_build.py:ffibuilder',
    'src/EPD_2in13_V2_build.py:ffibuilder'
  ],
  )
