#!/usr/bin/env python3
#coding=utf-8

from setuptools import setup, find_packages
setup(
name = "tltest",
version = "0.2",
packages = find_packages(),
# scripts = [''],

# Project uses reStructuredText, so ensure that the docutils get
# installed or upgraded on the target machine
install_requires = [''],

package_data = {},

# metadata for upload to PyPI
author = "admin",
author_email = "admin@yjadd.com",
description = "test",
license = "Apache2",
keywords = "tltest",
url = "http://www.yjadd.com/",
)