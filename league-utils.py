#!/usr/bin/env python3
"""league-utils

Usage:
  league-utils api
  league-utils isg [options]

Options:
  --champ=<champ>     Get info for only this champion (by name or id).
  --path=<path>       Override the path to your LoL installation.
                      By default, this is:
                      "C:\\Program Files\\Riot Games\\League of Legends"
"""
import sys

import docopt

import league_utils.entrypoint


if __name__ == '__main__':
    args = docopt.docopt(__doc__, version='1.0.5', argv=sys.argv[1:])

    if args['api']:
        del sys.argv[1]
        league_utils.entrypoint.api()
    elif args['isg']:
        del sys.argv[1]
        league_utils.entrypoint.isg()
