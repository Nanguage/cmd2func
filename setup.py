#!/usr/bin/env python

"""The setup script."""

import re
from setuptools import setup, find_packages


def get_long_description():
    return "See https://github.com/Nanguage/cmd2func"


def get_version():
    with open("cmd2func/__init__.py") as f:
        for line in f.readlines():
            m = re.match("__version__ = '([^']+)'", line)
            if m:
                return m.group(1)
        raise IOError("Version information can not found.")


def get_install_requirements():
    requirements = [
        "typing_extensions",
        "funcdesc",
        "pyYAML",
    ]
    return requirements


requires_test = ['pytest', 'pytest-cov', 'flake8', 'mypy']
packages_for_dev = ["pip", "setuptools", "wheel", "twine", "ipdb"]

requires_dev = packages_for_dev + requires_test

setup(
    author="Weize Xu",
    author_email='vet.xwz@gmail.com',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="Convert command to callable Python object.",
    install_requires=get_install_requirements(),
    license="MIT license",
    long_description=get_long_description(),
    include_package_data=True,
    keywords='cmd2func',
    name='cmd2func',
    packages=find_packages(include=['cmd2func', 'cmd2func.*']),
    url='https://github.com/Nanguage/cmd2func',
    version=get_version(),
    zip_safe=False,
    extras_require={
        'test': requires_test,
        'dev': requires_dev,
    }
)
