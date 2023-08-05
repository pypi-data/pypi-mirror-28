#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('CHANGES.rst') as history_file:
    history = history_file.read()

requirements = [
    'pytest-play>=1.0.0',
    'RestrictedPython>=4.0.b2',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
    'mock',
    'pytest-cov'
]

setup(
    name='play_python',
    version='0.1.0',
    description="pytest-play plugin with python expressions and assertions",
    long_description=readme + '\n\n' + history,
    author="Davide Moro",
    author_email='davide.moro@gmail.com',
    url='https://github.com/tierratelematics/play_python',
    packages=find_packages(include=['play_python']),
    entry_points={
        'playcommands': [
            'python = play_python.providers:PythonProvider',
        ],
    },
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='play_python',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
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
    extras_require={
        'tests': test_requirements,
    },
)
