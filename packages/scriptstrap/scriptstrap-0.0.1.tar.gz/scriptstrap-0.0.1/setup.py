#!/usr/bin/env python3
# encoding: utf-8

import os
from setuptools import setup, find_packages

# Read content of a file and return as a string
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='scriptstrap',
    version='0.0.1',
    license='MIT',
    url='https://github.com/postlund/scriptstrap',
    author='Pierre Ståhl',
    author_email='pierre.staahl@gmail.com',
    description='Simple bootstrapping of python scripts',
    long_description=read('README.rst'),
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
)
