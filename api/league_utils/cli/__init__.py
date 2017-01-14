import asyncio
import itertools
import json
import os
import platform
import sys

import aiohttp
import tqdm

from ..error import CLIError


async def get_itemset(cid, role):
    url = 'https://league.thekev.in/champ/{}/itemset/{}'.format(cid, role)
    async with aiohttp.ClientSession() as client, client.get(url) as response:
        if response.status != 200:
            return

        return await response.json()


async def save_itemset(cid, ckey, role, output):
    itemset = await get_itemset(cid, role)
    if not itemset:
        return

    champion_dir = output.itemset_path(ckey)
    try:
        os.makedirs(champion_dir)
    except OSError:
        pass

    itemset_filename = '{}_{}.json'.format(ckey, role)
    with open(os.path.join(champion_dir, itemset_filename), 'w') as f:
        f.write(json.dumps(itemset))


async def save_itemsets(champs, roles, output):
    tasks = []
    for (cid, ckey), role in itertools.product(champs, roles):
        task = asyncio.ensure_future(save_itemset(cid, ckey, role, output))
        tasks.append(task)

    for task in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        await task


async def parse_champs(champ):
    url = 'https://league.thekev.in/champ'
    async with aiohttp.ClientSession() as c, c.get(url) as response:
        if response.status != 200:
            print('ERROR reading from league-utils API.')
            sys.exit(1)

        data = (await response.json())['data']

    try:
        cid = [int(champ)]
        ckey = [c['attributes']['key'] for c in data if c['id'] == cid[0]]
        return zip(cid, ckey)
    except TypeError:
        return [(int(c['id']), c['attributes']['key']) for c in data]
    except ValueError:
        champ = champ.lower()
        for c in data:
            ckey = c['attributes']['key']
            name = c['attributes']['name']
            if name.lower() == champ or ckey.lower() == champ:
                return [(int(c['id']), ckey)]
    except Exception:
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
