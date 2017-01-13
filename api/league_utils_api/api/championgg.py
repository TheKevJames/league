import asyncio
import os

import aiohttp

from ..utils import async_lru_cache


TOKEN = os.environ['CHAMPIONGG_TOKEN']

API_BASE = 'http://api.champion.gg'
API_ITEMS = API_BASE + '/champion/{}/items/finished'
API_ITEMS_POPULAR = API_ITEMS + '/mostPopular?api_key=' + TOKEN
API_ITEMS_BEST = API_ITEMS + '/mostWins?api_key=' + TOKEN


@async_lru_cache(maxsize=256)
async def get_itemsets_best(ckey):
    assert TOKEN
    url = API_ITEMS_BEST.format(ckey)
    async with aiohttp.ClientSession() as client, client.get(url) as response:
        assert response.status == 200
        return await response.json()


@async_lru_cache(maxsize=256)
async def get_itemsets_popular(ckey):
    assert TOKEN
    url = API_ITEMS_POPULAR.format(ckey)
    async with aiohttp.ClientSession() as client, client.get(url) as response:
        assert response.status == 200
        return await response.json()


async def clear_cache():
    while True:
        get_itemsets_best.cache_clear()
        get_itemsets_popular.cache_clear()

        await asyncio.sleep(60 * 60 * 24)
