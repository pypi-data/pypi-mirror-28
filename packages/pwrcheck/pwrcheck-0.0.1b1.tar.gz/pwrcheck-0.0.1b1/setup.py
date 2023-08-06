#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for the Python PWRCheck Reader.

Source:: https://github.com/ampledata/pwrcheck
"""

import os
import sys

import setuptools

__title__ = 'pwrcheck'
__version__ = '0.0.1b1'
__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__copyright__ = 'Copyright 2018 Greg Albrecht'
__license__ = 'Apache License, Version 2.0'


def publish():
    """Function for publishing package to pypi."""
    if sys.argv[-1] == 'publish':
        os.system('python setup.py sdist')
        os.system('twine upload dist/*')
        sys.exit()


publish()


setuptools.setup(
    name=__title__,
    version=__version__,
    description='Python PWRCheck Reader.',
    author='Greg Albrecht',
    author_email='oss@undef.net',
    packages=['pwrcheck'],
    package_data={'': ['LICENSE']},
    package_dir={'pwrcheck': 'pwrcheck'},
    license=open('LICENSE').read(),
    long_description=open('README.rst').read(),
    url='https://github.com/ampledata/pwrcheck',
    zip_safe=False,
    include_package_data=True,
    setup_requires=[
        'coverage >= 3.7.1',
        'httpretty >= 0.8.10',
        'nose >= 1.3.7'
    ],
    install_requires=[
        'pynmea2 >= 1.4.2',
        'pyserial >= 2.7',
    ],
    classifiers=[
        'Topic :: Communications :: Ham Radio',
        'Programming Language :: Python',
        'License :: OSI Approved :: Apache Software License'
    ],
    keywords=[
        'Ham Radio', 'APRS', 'GPS'
    ],
    entry_points={'console_scripts': ['pwrcheck = pwrcheck.cmd:cli']}
)
