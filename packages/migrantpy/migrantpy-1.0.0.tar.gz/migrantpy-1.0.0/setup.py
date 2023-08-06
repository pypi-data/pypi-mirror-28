#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2016 Sascha Peilicke
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import migrantpy

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name=migrantpy.__name__,
    version=migrantpy.__version__,
    license="Apache-2.0",
    description=migrantpy.__doc__,
    long_description=long_description,
    author=migrantpy.__author__.rsplit(' ', 1)[0],
    author_email=migrantpy.__author__.rsplit(' ', 1)[1][1:-1],
    url='http://github.com/saschpe/migrantpy',
    scripts=['migrantpy.py', 'scripts/migrantpy'],
    data_files=[('share/doc/migrantpy', ['LICENSE.txt', 'README.md'])],
    test_suite="nose.collector",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Pre-processors',
    ],
)
