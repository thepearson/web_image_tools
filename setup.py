#!/usr/bin/env python
#
# $Id$
#
# Copyright (c) 2009, Jay Loden, Giampaolo Rodola'. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import sys
import os
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension


def get_version():
    INIT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'VERSION'))
    f = open(INIT, 'r')
    try:
        for line in f:
            if line.startswith('VERSION'):
                ret = eval(line.strip().split(' = ')[1])
                assert ret.count('.') == 2, ret
                for num in ret.split('.'):
                    assert num.isdigit(), ret
                return ret
        else:
            raise ValueError("couldn't find version string")
    finally:
        f.close()

def get_description():
    README = os.path.abspath(os.path.join(os.path.dirname(__file__), 'README.md'))
    f = open(README, 'r')
    try:
        return f.read()
    finally:
        f.close()

VERSION = get_version()

def main():
    setup_args = dict(
        name='wit',
        version=VERSION,
        download_url="https://github.com/thepearson/web_image_tools/zipball/master",
        description='A tool used to grab images from web pages and then do things to them',
        long_description=get_description(),
        provides = ['wit'],
        requires = ['python (>= 2.7)'],
        keywords=['library','images','qt','web',],
        author='Craig Pearson',
        author_email='thepearson@gmail.com',
        maintainer='Craig Pearson',
        maintainer_email='thepearson <at> gmail <dot> com',
        url='https://github.com/thepearson/web_image_tools',
        platforms='Platform Independent',
        license='License :: OSI Approved :: BSD License',
        packages=['wit'],
        scripts = ["scripts/wit", "scripts/wit-capture", "scripts/wit-capture-xvfb"],
        classifiers=[
              'Development Status :: 5 - Production/Stable',
              'Environment :: Console',
              'Operating System :: MacOS :: MacOS X',
              'Operating System :: Microsoft',
              'Operating System :: Microsoft :: Windows :: Windows NT/2000',
              'Operating System :: POSIX',
              'Operating System :: POSIX :: Linux',
              'Operating System :: POSIX :: BSD :: FreeBSD',
              'Operating System :: OS Independent',
              'Programming Language :: C',
              'Programming Language :: Python',
              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: 3',
              'Programming Language :: Python :: 3.0',
              'Programming Language :: Python :: 3.1',
              'Programming Language :: Python :: 3.2',
              'Topic :: System :: Monitoring',
              'Topic :: System :: Networking',
              'Topic :: System :: Networking :: Monitoring',
              'Topic :: System :: Benchmark',
              'Topic :: System :: Hardware',
              'Topic :: System :: Systems Administration',
              'Topic :: Utilities',
              'Topic :: Software Development :: Libraries',
              'Topic :: Software Development :: Libraries :: Python Modules',
              'Intended Audience :: Developers',
              'Intended Audience :: System Administrators',
              'License :: OSI Approved :: BSD License',
              ],
        )
    setup(**setup_args)

if __name__ == '__main__':
    main()
