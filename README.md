# LeagueUtils

LeagueUtils is a set of utilities for interacting with League of Legends data.
Currently, it contains the League ISG (Item Set Generator).

## ISG

The Item Set Generator is designed to build recommended pages for every
champion in every viable role. It does this by pulling date from Riot's API and
from some third party sites, determining which build paths work best, and
updating your League config with the results.

### Usage

After running `pip install -r requirements.txt` (preferably in a
[virtualenv](virtualenvwrapper.readthedocs.org)), simply run

    ./league-utils.py isg --write

to write the data to your system. You can also run something like

    ./league-utils.py isg --champ Rumble --no-write

to dump info on that champion to your terminal.

# Disclaimer

This project probably won't make your computer explode, make your girlfriend
leave you, or get you fired from your job, but I make no guarantees that
blindly following its advice won't drop your ELO. You've been warned.
