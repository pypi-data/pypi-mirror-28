#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='coltab',
    version='1.0.1',
    description='colorful tables for the terminal',
    long_description=readme,
    author="Richard Bann",
    author_email='richardbann@gmail.com',
    url='https://github.com/richardbann/coltab',
    packages=['coltab'],
    install_requires=['ansicolors>=1.1.8'],
    license="MIT license",
    zip_safe=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)
