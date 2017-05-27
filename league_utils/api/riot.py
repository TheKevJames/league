# TODO: global session
import asyncio
import logging
import os

import aiohttp

from ..utils import async_lru_cache


TOKEN = os.environ.get('RIOT_TOKEN', '')
API_HEADERS = {'X-Riot-Token': TOKEN}

API_STATIC_DATA = 'https://na1.api.riotgames.com/lol/static-data/v3'
API_CHAMP = API_STATIC_DATA + '/champions/{}?champData=all'
API_CHAMPS = API_STATIC_DATA + '/champions'
API_ITEM = API_STATIC_DATA + '/items/{}?itemData=all'
API_ITEMS = API_STATIC_DATA + '/items'

logger = logging.getLogger()


@async_lru_cache(maxsize=256)
async def get_champ(cid):
    assert TOKEN
    logger.debug('get_champ(%s)', cid)
    url = API_CHAMP.format(cid)
    async with aiohttp.ClientSession() as client:
        async with client.get(url, headers=API_HEADERS) as response:
            assert response.status == 200
            return await response.json()


@async_lru_cache(maxsize=2)
async def get_champs():
    assert TOKEN
    logger.debug('get_champs()')
    url = API_CHAMPS
    async with aiohttp.ClientSession() as client:
        async with client.get(url, headers=API_HEADERS) as response:
            assert response.status == 200
            return await response.json()


@async_lru_cache(maxsize=256)
async def get_item(iid):
    assert TOKEN
    logger.debug('get_item(%s)', iid)
    url = API_ITEM.format(iid)
    async with aiohttp.ClientSession() as client:
        async with client.get(url, headers=API_HEADERS) as response:
            assert response.status == 200
            return await response.json()


@async_lru_cache(maxsize=2)
async def get_items():
    assert TOKEN
    logger.debug('get_items()')
    url = API_ITEMS
    async with aiohttp.ClientSession() as client:
        async with client.get(url, headers=API_HEADERS) as response:
            assert response.status == 200
            return await response.json()


async def reset_cache():
    while True:
        get_champ.cache_clear()
        get_champs.cache_clear()
        get_item.cache_clear()
        get_items.cache_clear()

        try:
            tasks = []
            for iid in (await get_items())['data']:
                tasks.append(asyncio.ensure_future(get_item(int(iid))))

            await asyncio.gather(*tasks)
            logger.debug('riot cache refreshed')
        except Exception as e:  # pylint: disable=broad-except
            logger.error('error refreshing riot cache')
            logger.exception(e)

        await asyncio.sleep(60 * 60 * 24)
