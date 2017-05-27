# TODO: global session
import asyncio
import logging
import os

import aiohttp

from ..utils import async_lru_cache


TOKEN = os.environ.get('CHAMPIONGG_TOKEN', '')

API_BASE = 'http://api.champion.gg/v2'
API_CHAMP_HASHES = API_BASE + '/champions/{}?champData=hashes&api_key=' + TOKEN

logger = logging.getLogger()


@async_lru_cache(maxsize=256)
async def get_itemsets_best(cid):
    assert TOKEN
    logger.debug('get_itemsets_best(%s)', cid)
    url = API_CHAMP_HASHES.format(cid)
    async with aiohttp.ClientSession() as client, client.get(url) as response:
        assert response.status == 200

        # TODO: py36 (async generator)
        isets = []
        for role in await response.json():
            itemsets = role['hashes']['finalitemshashfixed']
            winrate = itemsets['highestWinrate']['winrate']
            items = itemsets['highestWinrate']['hash'].split('-')[1:]
            isets.append({
                'role': role['role'],
                'winrate': winrate,
                'items': items})

        return isets


@async_lru_cache(maxsize=256)
async def get_itemsets_popular(cid):
    assert TOKEN
    logger.debug('get_itemsets_popular(%s)', cid)
    url = API_CHAMP_HASHES.format(cid)
    async with aiohttp.ClientSession() as client, client.get(url) as response:
        assert response.status == 200

        # TODO: py36 (async generator)
        isets = []
        for role in await response.json():
            itemsets = role['hashes']['finalitemshashfixed']
            winrate = itemsets['highestCount']['winrate']
            items = itemsets['highestCount']['hash'].split('-')[1:]
            isets.append({
                'role': role['role'],
                'winrate': winrate,
                'items': items})

        return isets


@async_lru_cache(maxsize=256)
async def get_itemstarts_best(cid):
    assert TOKEN
    logger.debug('get_itemstarts_best(%s)', cid)
    url = API_CHAMP_HASHES.format(cid)
    async with aiohttp.ClientSession() as client, client.get(url) as response:
        assert response.status == 200

        # TODO: py36 (async generator)
        isets = []
        for role in await response.json():
            itemsets = role['hashes']['firstitemshash']
            winrate = itemsets['highestWinrate']['winrate']
            items = itemsets['highestWinrate']['hash'].split('-')[1:]
            isets.append({
                'role': role['role'],
                'winrate': winrate,
                'items': items})

        return isets


@async_lru_cache(maxsize=256)
async def get_itemstarts_popular(cid):
    assert TOKEN
    logger.debug('get_itemstarts_popular(%s)', cid)
    url = API_CHAMP_HASHES.format(cid)
    async with aiohttp.ClientSession() as client, client.get(url) as response:
        assert response.status == 200

        # TODO: py36 (async generator)
        isets = []
        for role in await response.json():
            itemsets = role['hashes']['firstitemshash']
            winrate = itemsets['highestCount']['winrate']
            items = itemsets['highestCount']['hash'].split('-')[1:]
            isets.append({
                'role': role['role'],
                'winrate': winrate,
                'items': items})

        return isets


async def reset_cache():
    while True:
        get_itemsets_best.cache_clear()
        get_itemsets_popular.cache_clear()
        get_itemstarts_best.cache_clear()
        get_itemstarts_popular.cache_clear()

        await asyncio.sleep(60 * 60 * 24)
