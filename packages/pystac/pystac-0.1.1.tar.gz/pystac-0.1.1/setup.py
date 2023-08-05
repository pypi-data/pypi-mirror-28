#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from glob import glob

from os.path import (
    basename,
    splitext
)

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'python-dateutil==2.6.1',
    'rasterio==1.0a12',
    'Click>=6.0',
    'geojson==2.3.0',
    'requests==2.18.0',
    'typing==3.6.2;python_version<"3.5"'
]

setup_requirements = [
    # NOQA TODO(notthatbreezy): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # NOQA TODO: put package test requirements here
]

setup(
    name='pystac',
    version='0.1.1',
    description=("Python command line utilities for interacting with and"
                 "creating STAC compliant files."),
    long_description=readme + '\n\n' + history,
    author="Raster Foundry",
    author_email='info@rasterfoundry.com',
    url='https://github.com/rasterfoundry/pystac',
    packages=find_packages(),
    py_modules=[splitext(basename(path))[0] for path in glob('pystac/*.py')],
    entry_points={
        'console_scripts': [
            'pystac=pystac.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='pystac',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
