#!/usr/bin/env python

# MIT License
#
# Copyright (c) 2017 Paul Stevens
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import codecs
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import lemming


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--verbose',
            './lemming', './tests'
        ]
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))

tests_require = [
    'pytest',
    'mock'
]

install_requires = [
    'Jinja2>=2.10',
    'ruamel.yaml>=0.15.35',
]

# sdist
if 'bdist_wheel' not in sys.argv:
    try:
        import argparse
    except ImportError:
        install_requires.append('argparse>=1.2.1')

# bdist
extras_require = {}

def long_description():
    with codecs.open('README.rst', encoding='utf-8') as f:
        return f.read()

setup(
    name='lemming',
    version=lemming.__version__,
    description='Python3 project layout generator',
    long_description=long_description(),
    author=lemming.__author__,
    author_email='ps@xnode.co.za',
    url='https://lemming.xnode.co.za',
    packages=find_packages(),
    include_package_data=True,
    extras_require=extras_require,
    install_requires=install_requires,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': [
            'lemming = lemming.cli:main'
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development',
        'Topic :: Terminals',
        'Topic :: Utilities',
    ],
)
