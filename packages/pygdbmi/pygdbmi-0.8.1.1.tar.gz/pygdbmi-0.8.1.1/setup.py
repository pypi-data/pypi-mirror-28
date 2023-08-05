#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#  pip install twine

import io
import os
import sys
import re
from setuptools import find_packages, setup, Command
from codecs import open
from pygdbmi.tests import test_app

EXCLUDE_FROM_PACKAGES = []
CURDIR = os.path.abspath(os.path.dirname(__file__))
README = io.open('README.rst', 'r', encoding="utf-8").read()

with open('pygdbmi/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)


class TestCommand (Command):
    description = 'test task'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        num_failures = test_app.main()
        if num_failures == 0:
            sys.exit(0)
        else:
            sys.exit(1)


setup(
    name='pygdbmi',
    version=version,
    author='Chad Smith',
    author_email='grassfedcode@gmail.com',
    description='Parse gdb machine interface output with Python',
    long_description=README,
    url='https://github.com/cs01/pygdbmi',
    license='MIT',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    keywords=['gdb', 'python', 'machine-interface', 'parse', 'frontend'],
    scripts=[],
    entry_points={},
    extras_require={},
    zip_safe=False,
    cmdclass={
        'test': TestCommand,
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
