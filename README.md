# LeagueUtils

LeagueUtils is a set of utilities for interacting with League of Legends data.
Currently, it contains the League ISG (Item Set Generator).

## Setup

### Install from PyPI

Simply run

    pip install --pre league-utils

### Install from Source

After cloning this repo, run

    python setup.py install

### Run without installing

This project can also be run without installation. After cloning this repo, run

    pip install -r requirements.txt

and use the `league-utils.py` script in the root of this folder. Working in a
[virtualenv](virtualenvwrapper.readthedocs.org) is recommended!

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

to dump info on that champion to your terminal. Currently, this isn't overly
readable, as it is in Riot's item set format. This will change at some point.

# Disclaimer

This project probably won't make your computer explode, make your girlfriend
leave you, or get you fired from your job, but I make no guarantees that
blindly following its advice won't drop your ELO. You've been warned.
