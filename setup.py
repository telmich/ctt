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
      author=ctt.AUTHOR,
      author_email=ctt.WWW,
      url=ctt.WWW,
      license="GNU GPLv3",
      packages=['lib/ctt',
                ],
      scripts=['scripts/ctt'],
      data_files=[
            ('/etc/bash_completion.d/', ['extras/completion/ctt']),
      ],
      zip_safe=True,
      classifiers=[
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Requires-Python:: 3.x']
      )
