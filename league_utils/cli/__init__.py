import asyncio
import itertools
import json
import os
import platform
import sys

import aiohttp
import tqdm

from ..error import CLIError


# LEAGUE_UTILS_API = 'http://127.0.0.1:28006'
LEAGUE_UTILS_API = 'https://league.thekev.in'


async def get_itemset(session, cid, ckey, role):
    url = '{}/champ/{}/itemset/{}'.format(LEAGUE_UTILS_API, cid, role)
    try:
        async with session.get(url, timeout=120) as response:
            if response.status != 200:
                return

            return (ckey, role, await response.json())
    except asyncio.TimeoutError:
        print('TIMEOUT getting itemset for {} ({}).'.format(ckey, role))
        return


async def get_itemsets(champs, roles):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for (cid, ckey), role in itertools.product(champs, roles):
            task = asyncio.ensure_future(get_itemset(session, cid, ckey, role))
            tasks.append(task)

        done = []
        for task in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            done.append(await task)
            # TODO: success/failures?

        return done


def save_itemset(ckey, role, itemset, output):
    itemset_file = os.path.join(
        output.itemset_path(ckey),
        '{}_{}.json'.format(ckey, role)
    )
    with open(itemset_file, 'w') as f:
        f.write(json.dumps(itemset))


async def parse_champs(champ):
    url = '{}/champ'.format(LEAGUE_UTILS_API)
    try:
        async with aiohttp.ClientSession() as c, c.get(url) as response:
            if response.status != 200:
                print('ERROR reading from league-utils API.')
                sys.exit(1)

            data = (await response.json())['data']
    except (aiohttp.ClientDisconnectedError, asyncio.CancelledError):
        print('Cancelling...')
        sys.exit(0)
    except aiohttp.ClientError:
        print('ERROR reading from league-utils API.')
        sys.exit(1)

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
    except Exception:  # pylint: disable=broad-except
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

    def ensure_paths(self, champs):
        for _, ckey in champs:
            try:
                os.makedirs(self.itemset_path(ckey))
            except FileExistsError:
                pass
