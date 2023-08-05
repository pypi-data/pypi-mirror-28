#!/usr/bin/env python
# coding=utf-8
from setuptools import setup, find_packages
import codecs
import os
import sys

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

NAME = "Frcwp"
PACKAGES = ["Frcwp"]
DESCRIPTION = "recognize the outliers of the data set"
LONG_DESCRIPTION = read("README.rst")
KEYWORDS = "algorithm"
AUTHOR = "sladesal"
AUTHOR_EMAIL = "stw386@sina.com"
URL = "https://github.com/sladesha/Frcwp"
VERSION = "0.0.7"
LICENSE = "MIT"

setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    packages = PACKAGES,
    include_package_data=True,
    zip_safe=True,
)
