#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
    'asyncpg',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='asyncpg_simpleorm',
    version='0.1.2',
    description="Simple orm for asyncpg",
    long_description=readme + '\n\n' + history,
    author="Michael Housh",
    author_email='mhoush@houshhomeenergy.com',
    url='https://github.com/m-housh/asyncpg_simpleorm',
    packages=find_packages(),
    package_dir={'asyncpg_simpleorm':
                 'asyncpg_simpleorm'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='asyncpg_simpleorm',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
