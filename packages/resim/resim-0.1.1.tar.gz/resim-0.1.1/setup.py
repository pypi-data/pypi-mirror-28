#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Based on https://github.com/pypa/sampleproject/blob/master/setup.py."""

from os import path
import sys
from codecs import open
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Shortcut for building/publishing to Pypi
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel upload')
    sys.exit()

def parse_reqs(req_path='./requirements.txt'):
    """Recursively parse requirements from nested pip files."""
    install_requires = []
    with open(req_path, 'r') as handle:
        # remove comments and empty lines
        lines = (line.strip() for line in handle
                 if line.strip() and not line.startswith('#'))

        for line in lines:
            # check for nested requirements files
            if line.startswith('-r'):
                # recursively call this function
                install_requires += parse_reqs(req_path=line[3:])
            else:
                # add the line as a new requirement
                install_requires.append(line)
    return install_requires

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='resim',
    version='0.1.1',
    description='chemoREsistance SIMulator',
    long_description=long_description,
    keywords='chemoresistance cancer outcome simulations modeling',
    url='http://github.com/zeochoy/resim',
    author='Zeo Choy',
    author_email='zeochoy@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=parse_reqs(),
    entry_points = {
        'console_scripts': ['resim-flask=resim.command_line:run_resim_flask'],
        #'console_scripts': ['resim-cui=resim.command_line:resim_cui'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Environment :: Console',
        ],
    )
