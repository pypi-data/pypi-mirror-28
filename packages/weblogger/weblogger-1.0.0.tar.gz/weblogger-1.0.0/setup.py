#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# The MIT License (MIT)
# 
# Copyright (c) 2016 Ivo Tzvetkov
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__version__ = '1.0.0'

setup(
    name='weblogger',
    version=__version__,
    description='A service for logging messages sent over HTTP to various backends',
    long_description='A service for logging messages sent over HTTP to various backends',
    author='Ivo Tzvetkov',
    author_email='ivotkv@gmail.com',
    license='MIT',
    url='http://github.com/ivotkv/weblogger',
    download_url='https://github.com/ivotkv/weblogger/tarball/v' + __version__,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ],
    keywords=[
        "web", "logger", "logging", "log"
    ],
    packages=[
        'weblogger'
    ],
    entry_points = {
        'console_scripts': [
            'weblogger=weblogger.server:main'
        ]
    },
    install_requires=[
        'PyYAML',
        'tornado',
        'httpagentparser'
    ]
)
