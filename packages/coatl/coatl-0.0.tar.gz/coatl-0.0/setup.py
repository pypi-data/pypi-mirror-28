# coding: utf-8

try:
    import setuptools
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setuptools.")

import os
long_description = 'This package provides you functions for data analysis, namely, data browsing and graph plotting. It can save the products made by these functions to a file.'

setup(
    name  = 'coatl',
    version = '0.0',
    description = 'For data analysis',
    long_description = long_description,
    license = 'MIT',
    author = 'Yuki Arai',
    author_email = 'threemeninaboat3247@gmail.com',
    url = 'https://github.com/threemeninaboat3247/coatl',
    keywords = 'data analysis',
    packages = find_packages(),
    install_requires = ['numpy','matplotlib','pandas'],
    classifiers = [
      'Programming Language :: Python',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: MIT License'
    ]
)
