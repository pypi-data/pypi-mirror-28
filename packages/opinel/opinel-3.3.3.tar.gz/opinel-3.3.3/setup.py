#!/usr/bin/env python

# distutils/setuptools install script for opinel
import os
from setuptools import setup, find_packages

# Package info
NAME = 'opinel'
ROOT = os.path.dirname(__file__)
VERSION = __import__(NAME).__version__

# Requirements
requirements = []
with open('requirements.txt') as f:
    for r in f.readlines():
        requirements.append(r.strip())

# Setup
setup(
    name=NAME,
    version=VERSION,
    description='Code shared between Scout2 and AWS-recipes.',
    long_description=open('README.rst').read(),
    author='l01cd3v',
    author_email='l01cd3v@gmail.com',
    url='https://github.com/nccgroup/opinel',
    packages=[
        'opinel', 'opinel.utils', 'opinel.services'
    ],
    package_data={
        'opinel': [
            'data/*.json',
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license='GNU General Public License v2 (GPLv2)',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
)
