#!/usr/bin/env python

import os
import re

from setuptools import setup, find_packages


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    with open(os.path.join(package, "__init__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)


def get_long_description():
    """
    Return the README.
    """
    with open("README.md", encoding="utf8") as f:
        return f.read()


setup(
    name="lsfiles",
    python_requires=">=3.7",
    version=get_version("lsfiles"),
    url="https://git.ars-virtualis.org/yul/lsfiles",
    license="BSD",
    description="find-like utility with functional API",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Aymeric Guth",
    author_email="aymeric.guth@protonmail.com",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: MacOS :: MacOS X",
        'Operating System :: POSIX',
    ],
    zip_safe=True,
)
