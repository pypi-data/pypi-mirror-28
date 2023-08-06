#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = [
]

test_requirements = [
    "pytest",
    "virtualenv",
]

setup(
    name='kipoi',
    version='0.0.1',
    description="Kipoi package",
    author="Kipoi team",
    author_email='avsec@in.tum.de',
    url='https://github.com/kipoi/kipoi',
    long_description='Kipoi package',
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        "develop": ["bumpversion",
                    "wheel",
                    "jedi",
                    "epc",
                    "pytest",
                    "pytest-pep8",
                    "pytest-cov"],
    },
    license="MIT license",
    zip_safe=False,
    keywords=[],
    test_suite='tests',
    tests_require=test_requirements
)
