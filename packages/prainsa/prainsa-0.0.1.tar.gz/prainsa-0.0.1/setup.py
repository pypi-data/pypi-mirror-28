#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import versioning
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'numpy>=1.11.1',
    'scipy>=0.18.1',
    'plotly>=2.0.12',
    'h5py>=2.6.0'
]

setup_requirements = [
    # TODO(A-Althobaiti): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='prainsa',
    version=versioning.get_version(),
    description="A Python framework to analyze and visualize brain signals.",
    long_description=readme + '\n\n' + history,
    author="Abdulrahman A. Althobaiti",
    author_email='Abdulrahman.Althobaiti@kaust.edu.sa',
    url='https://github.com/A-Althobaiti/prainsa',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='prainsa',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
