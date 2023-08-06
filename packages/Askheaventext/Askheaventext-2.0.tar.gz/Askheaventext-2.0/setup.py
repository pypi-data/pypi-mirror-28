#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

PACKAGE = "AskheavenTools"
NAME = "Askheaventext"
DESCRIPTION = "测试"
AUTHOR = "Askheaven"
AUTHOR_EMAIL = "278842015@qq.com"
URL = "https://github.com"
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open('README.rst').read(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages=find_packages(exclude=["tests.*", "tests"]),
    # package_data=find_package_data(
    #     PACKAGE,
    #     only_in_packages=False
    # ),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    zip_safe=False,
)