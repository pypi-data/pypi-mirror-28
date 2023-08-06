#!/usr/bin/env python
"""Build/distribute via setuptools."""

import setuptools

setuptools.setup(
    name='simplecmd',
    version='1.0.0',
    packages=['simplecmd'],

    # metadata for upload to PyPI
    author='Nicholas Bishop',
    author_email='nicholasbishop@gmail.com',
    description='Simple wrapper around subprocess',
    license='Apache-2.0',
    url='https://github.com/nicholasbishop/simplecmd',
)
