# LeagueUtils

[![Version](https://img.shields.io/pypi/v/league-utils.svg?style=flat-square)](https://pypi.python.org/pypi/league-utils)
[![Downloads](https://img.shields.io/pypi/dm/league-utils.svg?style=flat-square)](https://pypi.python.org/pypi/league-utils)
[![Build Status](https://img.shields.io/circleci/project/TheKevJames/league.svg?style=flat-square)](https://circleci.com/gh/TheKevJames/league)
[![Coverage Status](https://img.shields.io/coveralls/TheKevJames/league/master.svg?style=flat-square)](https://coveralls.io/github/TheKevJames/league?branch=master)
[![Code Quality](https://img.shields.io/codacy/a8f370e55fc94d72b92b2b6615ce165b.svg?style=flat-square)](https://www.codacy.com/app/KevinJames/league)
[![Code Health](https://landscape.io/github/TheKevJames/league/master/landscape.svg?style=flat-square)](https://landscape.io/github/TheKevJames/league/master)
[![Requirements](https://img.shields.io/requires/github/TheKevJames/league.svg?style=flat-square)](https://requires.io/github/TheKevJames/league/requirements)

LeagueUtils is a set of utilities for interacting with League of Legends data.
Currently, it contains the League ISG (Item Set Generator).

## ISG

The Item Set Generator is designed to build recommended pages for every
champion in every viable role. It does this by pulling date from Riot's API and
from some third party sites, determining which build paths work best, and
updating your League config with the results.

### Usage

The most common use case is to run

    league-utils isg --write

to install the item sets for every champion. The item sets will be installed
beside the default Riot recommended pages, but if you have manually downloaded
item sets into your config directory before, these may be overwritten. Make
sure any such files have unique names before running this script! (eg. anything
other than `${CHAMPION}_${ROLE}.json`).

You can also run something like

    league-utils isg --champ Rumble --no-write

to dump info on that champion to your terminal.

## Setup

### Install from PyPI

Simply run

    pip install --pre league-utils

### Install from Source

After cloning this repo or downloading and un{zip,tar}ing the most recent
[zipfile or tarball](https://github.com/thekevjames/league/releases/latest),
run

    python setup.py install

### Run without installing

This project can also be run without installation. After cloning this repo or
downloading and un{zip,tar}ing the most recent
[zipfile or tarball](https://github.com/thekevjames/league/releases/latest),
run

    pip install -r requirements.txt

and use the `league-utils.py` script in the root of this folder. Working in a
[virtualenv](virtualenvwrapper.readthedocs.org) is recommended!

### From a binary

Pre-compiled binaries are provided for some Operating Systems. If yours is
supported, you can grab the binary for
[the latest release](https://github.com/thekevjames/league/releases/latest) and
just run that without installing anything. Note that using this method does not
allow you to easily update.

# FAQ

## I'm getting a `No LEAGUE_TOKEN found` error. What gives?

Distributing secrets is hard; until I come up with a good way to do so, you'll
need to get a developer token from Riot Games to use this app. Simply set

    export LEAGUE_TOKEN=xxxxxxxxx

with your token before running this app.

# Disclaimer

This project probably won't make your computer explode, make your girlfriend
leave you, or get you fired from your job, but I make no guarantees that
blindly following its advice won't drop your ELO. You've been warned.
