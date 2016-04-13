#!/usr/bin/env python
import setuptools

from league_utils.version import __version__


# For reasons why you shouldn't do this, see:
#   https://caremad.io/blog/setup-vs-requirement/
# For all the fucks I give see:
#   /dev/zero
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()


setuptools.setup(
    name='league-utils',
    version=__version__,
    description='League of Legends utilities, including an Item Set Generator',
    keywords='league of legends game utilities item set generator isg',
    author='Kevin James',
    author_email='KevinJames@thekev.in',
    url='https://github.com/TheKevJames/league.git',
    license='MIT License',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': [
            'league-utils = league_utils.entrypoint:run',
        ],
    },
)
