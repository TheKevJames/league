import os

from riotwatcher import RiotWatcher


token = os.environ['LEAGUE_TOKEN']
api = RiotWatcher(token)
