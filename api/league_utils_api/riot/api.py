import asyncio
import os

import aiohttp

from ..utils import async_lru_cache


TOKEN = os.environ['RIOT_TOKEN']

API_STATIC_DATA = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2'
API_ITEMS = API_STATIC_DATA + '/item?itemListData=all&api_key=' + TOKEN
API_ITEM = API_STATIC_DATA + '/item/{}?itemData=all&api_key=' + TOKEN


@async_lru_cache(maxsize=256)
async def get_item(iid):
    assert TOKEN
    url = API_ITEM.format(iid)
    async with aiohttp.ClientSession() as client, client.get(url) as response:
        assert response.status == 200
        return await response.json()


async def clear_cache():
    while True:
        get_item.cache_clear()

        await asyncio.sleep(60 * 60 * 12)
