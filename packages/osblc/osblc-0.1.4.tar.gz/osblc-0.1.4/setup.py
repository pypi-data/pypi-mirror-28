#!/usr/bin/env python

from setuptools import setup, find_packages

__version__ = '0.1.4'

setup(
    name='osblc',
    version=__version__,
    description='On s\'en bat les couilles !',
    author='Noel Martignoni',
    author_email='noel@martignoni.fr',
    url='https://gitlab.com/nmartignoni/osblc',
    scripts=['osblc'],
    install_requires=['pygame'],
    include_package_data=True,
    packages=find_packages(exclude=['tests*']),
)
