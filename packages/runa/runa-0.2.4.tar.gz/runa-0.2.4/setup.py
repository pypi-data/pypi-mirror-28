#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import sys

from setuptools import setup, find_packages

VERSION_REQUIRED = (3, 5)

if sys.version_info < VERSION_REQUIRED:
    sys.exit('Python %s.%s is required' % VERSION_REQUIRED)

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'suds2==0.7.1'
]

setup_requirements = [
    # TODO(ovnicraft): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='runa',
    version='0.2.4',
    python_requires='>=3.2',
    description="Librería para uso de WS del Bus Gubernamental de Ecuador",
    long_description=readme + '\n\n' + history,
    author="Cristian Salamea",
    author_email='cristian.salamea@gmail.com',
    url='https://github.com/ovnicraft/runa',
    packages=find_packages(include=['runa']),
    entry_points={
        'console_scripts': [
            'runa=runa.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='runa',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
