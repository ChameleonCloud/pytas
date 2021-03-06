#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

from pytas import __version__

import os
import sys

class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--ignore', 'build']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()

requires = [r for r in open('requirements.txt').readlines()]

setup(
    name='pytas',
    version=__version__,
    description='Python package for TAS integration',
    long_description=readme,
    author='Matthew Hanlon',
    author_email='mrhanlon@tacc.utexas.edu',
    url='https://github.com/mrhanlon/pytas',
    packages=find_packages(),
    package_dir={'pytas':
                 'pytas'},
    include_package_data=True,
    install_requires=requires,
    license="MIT",
    zip_safe=False,
    keywords='pytas',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    cmdclass={'test': PyTest},
    tests_require=['pytest'],
    test_suite='tests',
)
