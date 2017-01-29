# TODO: global session
import asyncio
import logging
import os

import aiohttp

from ..utils import async_lru_cache


TOKEN = os.environ.get('CHAMPIONGG_TOKEN', '')

API_BASE = 'http://api.champion.gg'
API_ITEMS_DONE = API_BASE + '/champion/{}/items/finished'
API_ITEMS_DONE_POPULAR = API_ITEMS_DONE + '/mostPopular?api_key=' + TOKEN
API_ITEMS_DONE_BEST = API_ITEMS_DONE + '/mostWins?api_key=' + TOKEN
API_ITEMS_START = API_BASE + '/champion/{}/items/starters'
API_ITEMS_START_POPULAR = API_ITEMS_START + '/mostPopular?api_key=' + TOKEN
API_ITEMS_START_BEST = API_ITEMS_START + '/mostWins?api_key=' + TOKEN

logger = logging.getLogger()


@async_lru_cache(maxsize=256)
async def get_itemsets_best(ckey):
    assert TOKEN
    logger.debug('get_itemsets_best(%s)', ckey)
    url = API_ITEMS_DONE_BEST.format(ckey)
    async with aiohttp.ClientSession() as client, client.get(url) as response:
        assert response.status == 200
        return await response.json()


@async_lru_cache(maxsize=256)
async def get_itemsets_popular(ckey):
    assert TOKEN
    logger.debug('get_itemsets_popular(%s)', ckey)
    url = API_ITEMS_DONE_POPULAR.format(ckey)
    async with aiohttp.ClientSession() as client, client.get(url) as response:
        assert response.status == 200
        return await response.json()


@async_lru_cache(maxsize=256)
async def get_itemstarts_best(ckey):
    assert TOKEN
    logger.debug('get_itemstarts_best(%s)', ckey)
    url = API_ITEMS_START_BEST.format(ckey)
    async with aiohttp.ClientSession() as client, client.get(url) as response:
        assert response.status == 200
        return await response.json()


@async_lru_cache(maxsize=256)
async def get_itemstarts_popular(ckey):
    assert TOKEN
    logger.debug('get_itemstarts_popular(%s)', ckey)
    url = API_ITEMS_START_POPULAR.format(ckey)
    async with aiohttp.ClientSession() as client, client.get(url) as response:
        assert response.status == 200
        return await response.json()


async def reset_cache():
    while True:
        get_itemsets_best.cache_clear()
        get_itemsets_popular.cache_clear()
        get_itemstarts_best.cache_clear()
        get_itemstarts_popular.cache_clear()

        await asyncio.sleep(60 * 60 * 24)
