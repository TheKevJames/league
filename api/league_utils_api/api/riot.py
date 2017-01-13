import asyncio
import os

import aiohttp

from ..utils import async_lru_cache


TOKEN = os.environ['RIOT_TOKEN']

API_STATIC_DATA = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2'
API_CHAMP = API_STATIC_DATA + '/champion/{}?champData=all&api_key=' + TOKEN
API_ITEMS = API_STATIC_DATA + '/item?api_key=' + TOKEN
API_ITEM = API_STATIC_DATA + '/item/{}?itemData=all&api_key=' + TOKEN


@async_lru_cache(maxsize=128)
async def get_champ(cid):
    assert TOKEN
    url = API_CHAMP.format(cid)
    async with aiohttp.ClientSession() as client, client.get(url) as response:
        assert response.status == 200
        return await response.json()


@async_lru_cache(maxsize=256)
async def get_item(iid):
    assert TOKEN
    url = API_ITEM.format(iid)
    async with aiohttp.ClientSession() as client, client.get(url) as response:
        assert response.status == 200
        return await response.json()


@async_lru_cache(maxsize=2)
async def get_items():
    assert TOKEN
    url = API_ITEMS
    async with aiohttp.ClientSession() as client, client.get(url) as response:
        assert response.status == 200
        return await response.json()


async def reset_cache():
    while True:
        get_champ.cache_clear()
        get_item.cache_clear()
        get_items.cache_clear()

        # TODO: re-populate?

        await asyncio.sleep(60 * 60 * 24)
