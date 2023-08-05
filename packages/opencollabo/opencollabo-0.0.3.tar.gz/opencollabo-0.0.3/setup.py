#!/usr/bin/env python3

from setuptools import setup

setup(
    name='opencollabo',
    version='0.0.3',
    packages=['opencollabo'],
    package_dir={'opencollabo': 'opencollabo'},
    install_requires=[
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'opencollabo = opencollabo.main:run'
        ]
    }
)