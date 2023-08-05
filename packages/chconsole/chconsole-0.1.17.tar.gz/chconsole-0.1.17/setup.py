#!/usr/bin/env python
# coding: utf-8

# Copyright 2017 (C) Manfred Minimair
# Distributed under the terms of the Modified BSD License.
# Based on setup.py from qtconsole
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# the name of the package
name = 'chconsole'

#-----------------------------------------------------------------------------
# Minimal Python version sanity check
#-----------------------------------------------------------------------------

import sys

v = sys.version_info
if v[0] < 3 or (v[0] >= 3 and v[:2] < (3,3)):
    error = "ERROR: {} requires Python version 3.3 or above.".format(name)
    print(error, file=sys.stderr)
    sys.exit(1)

PY3 = (sys.version_info[0] >= 3)

#-----------------------------------------------------------------------------
# get on with it
#-----------------------------------------------------------------------------

import os
from glob import glob

from distutils.core import setup

pjoin = os.path.join
here = os.path.abspath(os.path.dirname(__file__))
pkg_root = pjoin(here, name)

packages = []
for d, _, _ in os.walk(pjoin(here, name)):
    if os.path.exists(pjoin(d, '__init__.py')):
        packages.append(d[len(here)+1:].replace(os.path.sep, '.'))

package_data = {
    'chconsole' : ['main/resources/icon/*.svg'],
}

version_ns = {}
with open(pjoin(here, name, '_version.py')) as f:
    exec(f.read(), {}, version_ns)


setup_args = dict(
    name            = name,
    version         = version_ns['__version__'],
    scripts         = glob(pjoin('scripts', '*')),
    packages        = packages,
    package_data    = package_data,
    description     = "Jupyter/Qt-based Chat Console",
    long_description= "Jupyter/Qt-based console with support for chat and rich media output",
    author          = 'Manfred Minimair',
    author_email    = 'chconsole@gmail.com',
    url             = 'https://github.com/mincode/chconsole',
    license         = 'BSD',
    platforms       = "Linux, Mac OS X, Windows",
    keywords        = ['Interactive', 'Interpreter', 'Shell'],
    classifiers     = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)

if 'develop' in sys.argv or any(a.startswith('bdist') for a in sys.argv):
    import setuptools

setuptools_args = {}
install_requires = setuptools_args['install_requires'] = [
    'traitlets',
    'jupyter_core',
    'jupyter_client>=4.1',
    'qtconsole>=4.1'
    'pygments',
    'paramiko',
    'ipykernel>=4.1', # not a real dependency, but require the reference kernel
]

extras_require = setuptools_args['extras_require'] = {
    'test:python_version=="2.7"': ['mock'],
    'test:sys_platform != "win32"': ['pexpect'],
    'doc': 'Sphinx>=1.3'
}

if 'setuptools' in sys.modules:
    setup_args['entry_points'] = {
        # gui_scripts eats help output in the command shell
        'console_scripts': [
            'jupyter-chconsole = chconsole.main.launch_app:main',
            'chconsole = chconsole.main.launch_app:main',
            'jupyter-chrun = chconsole.run_kernel.run_remote:start_remote',
            'chrun = chconsole.run_kernel.run_remote:start_remote',
        ],
        'gui_scripts': [
            'chc-python = chconsole.run_kernel.chc_python:start_local',
            'jupyter-chjoin = chconsole.launch.join:main',
            'chjoin = chconsole.launch.join:main',
        ]
    }
    setup_args.pop('scripts')
    setup_args.update(setuptools_args)

if __name__ == '__main__':
    setup(**setup_args)
