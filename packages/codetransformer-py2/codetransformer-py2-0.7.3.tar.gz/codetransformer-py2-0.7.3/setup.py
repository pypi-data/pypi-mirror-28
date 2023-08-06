#!/usr/bin/env python
from setuptools import setup, find_packages
import sys

import versioneer

long_description = ''

if 'upload' in sys.argv:
    with open('README.rst') as f:
        long_description = f.read()


setup(
    name='codetransformer-py2',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Python code object transformers',
    author='Joe Jevnik, Scott Sanderson, and Bryan Thornbury',
    author_email='joejev@gmail.com',
    packages=find_packages(),
    long_description=long_description,
    license='GPL-2',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Pre-processors',
    ],
    url='https://github.com/brthor/codetransformer-py2',
    install_requires=['six', 'enum34', 'singledispatch'],
    extras_require={
        'dev': [
            'flake8==3.3.0',
            'pytest==2.8.4',
            'pytest-cov==2.2.1',
        ],
    },
)
