#!/usr/bin/env python
# -*- python -*-
# -*- coding: utf-8 -*-

#
# Copyright 2011-2018 Red Hat, Inc.
#   This copyrighted material is made available to anyone wishing to use,
#  modify, copy, or redistribute it subject to the terms and conditions of
#  the GNU General Public License v.2.
#
#   This application is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   General Public License for more details.
#
# Authors:
#   Guy Streeter <guy.streeter@gmail.com>
#

from __future__ import print_function
import sys
import os
import subprocess

from setuptools import Command, setup
from distutils.command.build import build
from distutils.extension import Extension
from Cython.Distutils import build_ext


if sys.version_info[0] == 3:
    _package_name = 'python3-hwloc'
    _pythonver = 'python2'
else:
    _package_name = 'python2-hwloc'
    _pythonver = 'python3'

__author = 'Guy Streeter <guy.streeter@gmail.com>'
__author_email = 'guy.streeter@gmail.com'
__license = 'GPLv2+'
__description = 'python bindings for hwloc'
__version = '2.3.6.0.1.11.5'
__URL = 'https://gitlab.com/guystreeter/python-hwloc'
__classifiers = [
    'Environment :: Other Environment',
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Topic :: System :: Systems Administration',
    ]

with open('README.rst') as rfile:
    __long_description = rfile.read()

datadir = os.environ.get('DATADIR', 'share')
docdir = os.path.join(datadir, 'doc', _package_name)
licdir = os.environ.get('LICENSEDIR',
                        os.path.join(datadir, 'doc', _package_name))

data_files = [
    (licdir, ['COPYING',
              'LICENSE',
              ]),
    (docdir, ['doc/hwloc-hello.py',
              'doc/guide.md',
              'doc/guide.html',
              ]),
]


class build_doc(Command):
    description = 'build guide.pdf and guide.html'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            subprocess.call(
                ['/usr/bin/pandoc', '-o', 'doc/guide.html', 'doc/guide.md'])
            subprocess.call(
                ['/usr/bin/pandoc', '-o', 'doc/guide.pdf', '--toc', '-V',
                 'fontfamily:utopia', 'doc/guide.md'])
        except:
            print(
                'pandoc and texlive are required to build documentation',
                file=sys.stderr)


class all_build(build):
    sub_commands = [
        ('build_ext', None),
        ] + build.sub_commands


setup(
    name=_package_name,
    version=__version,
    description=__description,
    author=__author,
    author_email=__author_email,
    license=__license,
    classifiers=__classifiers,
    long_description=__long_description,
    url=__URL,
    install_requires=[_pythonver+'-libnuma'],
    packages=['hwloc'],
    data_files=data_files,
    cmdclass={
        'build': all_build,
        'build_doc': build_doc,
        'build_ext': build_ext,
        },
    ext_modules=[
        Extension(
            'hwloc.chwloc',
                ['chwloc.pyx'],
            libraries=['hwloc']),
        Extension(
            'hwloc.linuxsched',
            ['linuxsched.pyx'])])
