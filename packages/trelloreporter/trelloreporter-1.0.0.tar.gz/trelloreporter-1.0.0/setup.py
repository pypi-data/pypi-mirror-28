#!/usr/bin/env python

# Copyright 2017 Internet Solutions (Pty) Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import sys

from codecs import open

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
for p in sys.path:
    print(p)

local = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(local, 'trelloreporter', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

packages = ['trelloreporter', 'trelloreporter/cmd', 'trelloreporter/config', 'trelloreporter/rest',
    'trelloreporter/trelloreader', 'trelloreporter/writer']

requires = [
    'requests>=2.12.5',
    'openpyxl>=2.4.5',
    'ruamel.yaml>=0.13.10',
    'uvloop>=0.8.1',
    'aiohttp>=2.3.2',
    'elasticsearch>=6.0.0'
]

test_requirements = [
    'coverage==4.4.1',
    'pytest==3.2.1',
    'pytest-cov==2.5.1',
]

setup(
    name='trelloreporter',
    version=about['__version__'],
    description='Platform Engineering Northbound API',
    author='Paul Stevens',
    author_email='paul.stevens@is.co.za',
    url='https://platform.is',
    packages=packages,
    package_dir={'trelloreporter': 'trelloreporter'},
    data_files=[('/opt/trelloreporter/config', ['trelloreporter/config/trelloreporter.yml']), 
	('/opt/trelloreporter/data', ['trelloreporter/data/trelloreporter.db']),
	('/opt/trelloreporter/data/log',['trelloreporter/data/log/trelloreporter.log'])],
    include_package_data=True,
    install_requires=requires,
    python_requires='~=3.5',
    license='Apache 2.0',
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ),
    cmdclass={},
    entry_points={
        'console_scripts': [
            'trelloreporter=trelloreporter.cmd.trelloreport:main',
        ]
    },
    tests_require=test_requirements,
    extras_require={},
)
