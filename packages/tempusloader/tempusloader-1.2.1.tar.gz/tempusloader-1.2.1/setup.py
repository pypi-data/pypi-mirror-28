#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from distutils.spawn import find_executable

assert find_executable('psql'), 'psql executable not found!!'

setup(
    name='tempusloader',
    version='1.2.1',
    description="Tempus data loader",
    long_description="Tempus data loader",
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: System :: Software Distribution",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    keywords='',
    author='Tempus Team',
    author_email='infos@oslandia.com',
    maintainer='Oslandia',
    maintainer_email='infos@oslandia.com',

    license='LGPL',
    packages=['tempusloader', 'tempusloader/provider'],
    package_data={
        'tempusloader/provider': ['sql/*.sql'],
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=('gtfslib', 'pglite'),
    extras_require={
        "develop": ()
    },

    entry_points=dict(console_scripts=[
        'loadtempus=tempusloader.load_tempus:main',
    ]),
)
