#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import pychievements


def publish():
    """Publish to PyPi"""
    os.system("python setup.py sdist upload")

if sys.argv[-1] == "publish":
    publish()
    sys.exit()

setup(
    name='pychievements',
    version=pychievements.__version__,
    description='Python Achievements Framework',
    long_description=open('README.rst').read() + '\n\n' + open('HISTORY.rst').read(),
    author='Brian Knobbs',
    author_email='brian@packetperception.org',
    url='https://github.com/PacketPerception/pychievements',
    packages=[
        'pychievements',
    ],
    extras_require={
        'cli': ["clint"]
    },
    license='MIT',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ),
)
