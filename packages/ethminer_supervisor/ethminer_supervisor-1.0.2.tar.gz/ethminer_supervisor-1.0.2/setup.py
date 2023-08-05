#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
]

test_requirements = [
    'coverage',
    'flake8',
    'mock',
    'tox',
]

setup(
    name='ethminer_supervisor',
    version='1.0.2',
    description="Supervise ethminer daemon and restart process or machine when appropriate",
    long_description=readme,
    author="Jon Robison",
    author_email='narfman0@gmail.com',
    url='https://github.com/narfman0/ethminer_supervisor',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=True,
    keywords='ethminer_supervisor ethereum',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': ['ethminer_supervisor=ethminer_supervisor.cli:main'],
    }
)
