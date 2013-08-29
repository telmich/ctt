#!/usr/bin/env python3
"""
script to install ctt
"""
import sys
from setuptools import setup
sys.path.insert(0, 'lib/')
import ctt

setup(name='ctt',
      version=ctt.VERSION,
      # description=pwman.description,
      author=ctt.AUTHOR,
      author_email=ctt.WWW,
      url=ctt.WWW,
      license="GNU GPL",
      packages=['lib/ctt',
                ],
      scripts=['bin/ctt'],
      zip_safe=True,
      # install_requires=['pycrypto>=2.6',
      #          'colorama>=0.2.4'],
      classifiers=[
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: GPL version 3',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Requires-Python:: 3.x']
      )
