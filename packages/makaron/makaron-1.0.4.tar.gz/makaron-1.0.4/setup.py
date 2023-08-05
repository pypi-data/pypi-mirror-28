#!/usr/bin/env python

from setuptools import setup, find_packages

__version__ = '1.0.4'

setup(
    name='makaron',
    version=__version__,
    description='Version handler',
    author='Noel Martignoni',
    author_email='noel@martignoni.fr',
    url='https://gitlab.com/makaron/makaron',
    scripts=['scripts/makaron'],
    install_requires=['future', 'pyyaml'],
    packages=find_packages(exclude=['tests*']),
)
