import os
import platform
import sys

import aiohttp

from ..error import CLIError


async def get_itemset(cid, role):
    url = 'https://league.thekev.in/champ/{}/itemset/{}'.format(cid, role)
    async with aiohttp.ClientSession() as client, client.get(url) as response:
        if response.status != 200:
            return

        return await response.json()


def save_itemset(ckey, role, itemset, output):
    champion_dir = output.itemset_path(ckey)
    try:
        os.makedirs(champion_dir)
    except OSError:
        pass

    itemset_filename = '{}_{}.json'.format(ckey, role)
    with open(os.path.join(champion_dir, itemset_filename), 'w') as f:
        f.write(itemset)


async def parse_champs(champ):
    url = 'https://league.thekev.in/champ'
    async with aiohttp.ClientSession() as c, c.get(url) as response:
        if response.status != 200:
            print('ERROR reading from league-utils API.')
            sys.exit(1)

        data = (await response.json())['data']

    if not champ:
        return [(int(c['id']), c['attributes']['key']) for c in data]

    try:
        cid = [int(champ)]
        ckey = [c['attributes']['key'] for c in data if c['id'] == champ]
        return zip(cid, ckey)
    except TypeError:
        pass

    for c in data:
        if c['attributes']['name'] == champ or c['attributes']['key'] == champ:
            return [(int(c['id']), c['attributes']['key'])]

    print('Could not find champion {}.'.format(champ))
    sys.exit(1)


class Output:
    def __init__(self, path=None):
        self.path = path
        if not path:
            self.path = self.get_default_path()

    @staticmethod
    def get_default_path():
        system = platform.system()

        if system == 'Windows':
            return os.path.join('C:', 'Riot Games', 'League of Legends')

        if system.startswith('CYGWIN_NT'):
            return os.path.join(
                os.sep, 'cygdrive', 'c', 'Riot Games', 'League of Legends')

        if system == 'Linux':
            return os.path.join(
                os.path.expanduser('~'), '.PlayOnLinux', 'wineprefix',
                'LeagueOfLegends', 'drive_c', 'Riot Games',
                'League of Legends')

        if system == 'Darwin':
            return os.path.join(
                os.sep, 'Applications', 'League of Legends.app', 'Contents',
                'LOL')

        raise CLIError('Platform {} not supported.'.format(system))

    @property
    def champ_path(self):
        return os.path.join(self.path, 'Config', 'Champions')

    def itemset_path(self, ckey):
        return os.path.join(self.champ_path, ckey, 'Recommended')
