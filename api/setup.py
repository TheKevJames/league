#!/usr/bin/env python
import setuptools


setuptools.setup(
    name='league-utils-api',
    version='1.0.0',
    description='League of Legends utilities (API Server)',
    keywords='league of legends game utilities item set generator isg',
    author='Kevin James',
    author_email='KevinJames@thekev.in',
    url='https://github.com/TheKevJames/league.git',
    license='MIT License',
    packages=setuptools.find_packages(),
    install_requires=['aiohttp'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': [
            'league-utils-api = league_utils_api.entrypoint:run',
        ],
    },
)
