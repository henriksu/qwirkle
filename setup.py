#!/usr/bin/env python

from setuptools import setup

setup(name='Qwirkle',
      version='0.1',
      description='Python Implementation of the Board Game Qwirkle',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha'
          'Intended Audience :: Education'
          'Intended Audience :: End Users/Desktop'
          'Programming Language :: Python :: 3.6',
          'Topic :: Games/Entertainment :: Board Games'
          # 'Topic :: Scientific/Engineering :: Artificial Intelligence',
          # 'License :: OSI Approved', ?
          ],
      keywords='qwirkle',
      author='Jon-Henning Aasum, Henrik Sperre Sundklakk',
      author_email='henrik.sundklakk@gmail.com',
      packages=['qwirkle', 'qwirkle.AI', 'qwirkle.game_logic', 'qwirkle.gui', 'tests'],
      install_requires=['numpy', 'pygame'],
      test_suite="tests",
      tests_require=['unittest'], # TODO: pytest instad.
      include_package_data=True,
      zip_safe=False,
     )