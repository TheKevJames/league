#!/usr/bin/env python
import setuptools


setuptools.setup(
    name='league-utils',
    version='1.0.4',
    description='League of Legends utilities, including an Item Set Generator',
    long_description=open('README.rst', 'r').read(),
    keywords='league legends game utilities item set generator efficiency isg',
    author='Kevin James',
    author_email='KevinJames@thekev.in',
    url='https://github.com/TheKevJames/league.git',
    license='MIT License',
    packages=setuptools.find_packages(),
    install_requires=['aiohttp', 'docopt', 'tqdm'],
    setup_requires=['pytest-runner'],
    tests_require=['hypothesis', 'pytest', 'pytest-cov', 'pytest-pep8'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'league-utils-api = league_utils.entrypoint:api',
            'league-utils-isg = league_utils.entrypoint:isg',
        ],
    },
)
