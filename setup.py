#! /usr/bin/env python

'''Setup file for dyntopo Namespace Package

See:
    https://packaging.python.org/en/latest/distributing.html
'''

import os
import re
import sys
import shlex
import unittest
import subprocess

from setuptools import setup, find_packages, Command
from setuptools.command.test import test

pkg_name = 'dyntopo'

class CleanCommand(Command):
    '''Custom clean command

    cleanup current directory:
        - removes build/
        - removes src/*.egg-info
        - removes *.pyc and __pycache__ recursively

    Example
    -------
        python setup.py clean

    '''

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf src/*.egg-info')
        os.system('rm -vrf */src/*.egg-info')
        os.system('find . -type d -name "build" | xargs rm -vrf')
        os.system('find . -type d -name "__build__" | xargs rm -vrf')
        os.system('find . -type d -name "*documentation" -exec rm -vrf {} \;')
        os.system('find . -type f -name "*.pyc" -exec rm -vrf {} \;')
        os.system('find . -type d -name "__pycache__" | xargs rm -vrf')

class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # do nothing
        # do not need to run any tests for namespace pkg
        pass


class BuildAndPreviewDocsCommand(Command):
    user_options = []
    description = 'CISCO SHARED : Build and privately distribute ' \
        'Sphinx documentation for this package'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        sphinx_build_cmd = "sphinx-build -b html -c docs " \
            "-d ./__build__/documentation/doctrees docs/ ./__build__/documentation/html"
        try:
            ret_code = subprocess.call(shlex.split(sphinx_build_cmd))
            if not ret_code:
                sys.exit(0)
            else:
                sys.exit(1)
        except Exception:
            sys.exit(1)



def read(*paths):
    '''read and return txt content of file'''
    with open(os.path.join(os.path.dirname(__file__), *paths)) as fp:
        return fp.read()


def find_version(*paths):
    '''reads a file and returns the defined __version__ value'''
    version_match = re.search(r"^__version__ ?= ?['\"]([^'\"]*)['\"]",
                              read(*paths), re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

# compute version range
# For example, range >= 3.0.0 < 3.1.0
#
version = find_version('src', pkg_name, '__init__.py')
req_ver = version.split('.')
version_range = '>= %s.%s.0, < %s.%s.0' % \
    (req_ver[0], req_ver[1], req_ver[0], int(req_ver[1])+1)

# launch setup
setup(
    name = pkg_name,
    version = version,

    # descriptions
    description = 'pyATS: pyATS Overall Module',
    long_description = read('DESCRIPTION.rst'),

    # the project's main homepage.
    url = 'http://wwwin-pyats.cisco.com/cisco-shared/{}/latest/'.\
        format(pkg_name),

    # author details
    author = 'ASG Teams',
    author_email = 'pyats_support@cisco.com',

    # project licensing
    license = 'Cisco Systems, Inc. Cisco Confidential',

    # see https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry'
        'License :: Other/Proprietary License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Testing',
    ],

    # project keywords
    keywords = 'dyntopo dynamic topology orchestrator xrut laas vxr local',

    # uses namespace package
    namespace_packages = [pkg_name],

    # project packages
    packages = find_packages(where = 'src'),

    # project directory
    package_dir = {
        '': 'src',
    },

    # additional package data files that goes into the package itself
    package_data = {
    },

    # console entry point
    entry_points = {
    },

    # package dependencies
    install_requires =  ['dyntopo.laas %s' % version_range,
                         'dyntopo.xrut %s' % version_range,
                         'dyntopo.vxr %s' % version_range,
                         'dyntopo.local %s' % version_range,
                        ],

    # any additional groups of dependencies.
    # install using: $ pip install -e .[dev]
    extras_require = {
        'dev': ['coverage',
                'restview',
                'Sphinx',
                'sphinxcontrib-mockautodoc',
                'sphinx-rtd-theme'],
    },

    # any data files placed outside this package.
    # See: http://docs.python.org/3.4/distutils/setupscript.html
    # format:
    #   [('target', ['list', 'of', 'files'])]
    # where target is sys.prefix/<target>
    data_files = [],

    # custom commands for setup.py
    cmdclass = {
        'clean': CleanCommand,
        'test': TestCommand,
        'docs': BuildAndPreviewDocsCommand,
    },

    # non zip-safe (never tested it)
    zip_safe = False,
)
