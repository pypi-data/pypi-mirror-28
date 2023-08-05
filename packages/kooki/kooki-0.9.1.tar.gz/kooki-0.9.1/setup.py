#!/usr/bin/env python
import os, atexit
from setuptools import setup, find_packages
from setuptools.command.install import install
from subprocess import check_call

__version__ = '0.9.1'

setup(
    name='kooki',
    version=__version__,
    description='The ultimate document generator.',
    author='Noel Martignoni',
    include_package_data=True,
    package_data={'kooki.config': ['format.yaml']},
    author_email='noel@martignoni.fr',
    url='https://gitlab.com/kooki/kooki',
    scripts=['scripts/kooki', 'scripts/kooki-recipe', 'scripts/kooki-jar'],
    install_requires=['empy', 'pyyaml', 'toml', 'requests', 'termcolor', 'mistune', 'karamel', 'munch'],
    packages=find_packages(exclude=['tests*']),
    test_suite='tests',
)
