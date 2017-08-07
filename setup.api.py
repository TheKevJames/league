#!/usr/bin/env python
import setuptools


setuptools.setup(
    name='league-utils',
    version='1.0.5',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'league-utils-api = league_utils.entrypoint:api',
            'league-utils-isg = league_utils.entrypoint:isg',
        ],
    },
)
