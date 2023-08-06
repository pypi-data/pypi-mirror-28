#!/usr/bin/env python

# The author disclaims copyright to this source code. Please see the
# accompanying UNLICENSE file.

from __future__ import with_statement

from setuptools import setup, find_packages

with open("README") as readme:
    documentation = readme.read()

setup(
    name="tbucket",
    version="1.1.0",
    description="A sqlite-backed token bucket rate limiter implementation.",
    long_description=documentation,
    author="AllSeeingEyeTolledEweSew",
    author_email="allseeingeyetolledewesew@protonmail.com",
    url="http://github.com/AllSeeingEyeTolledEweSew/tbucket",
    license="Unlicense",
    py_modules=["tbucket"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Public Domain",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
        "Topic :: Database",
        "Operating System :: OS Independent",
        "License :: Public Domain",
    ],
)
