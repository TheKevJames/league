# TODO: global session
import asyncio
import logging
import os
import time

import aiohttp

from ..utils import async_lru_cache


try:
    TOKEN = os.environ['RIOT_TOKEN']
except KeyError:
    try:
        TOKEN = open('/run/secrets/riot_token').read().rstrip()
    except IOError:
        TOKEN = None
API_HEADERS = {'X-Riot-Token': TOKEN}

API_STATIC_DATA = 'https://na1.api.riotgames.com/lol/static-data/v3'
API_CHAMP = API_STATIC_DATA + '/champions/{}?champData=all'
API_CHAMPS = API_STATIC_DATA + '/champions'
API_ITEM = API_STATIC_DATA + '/items/{}?itemData=all'
API_ITEMS = API_STATIC_DATA + '/items'

logger = logging.getLogger()


class RateLimiter:
    INTERVAL = 10
    TOKENS = 250  # Riot gives us 500 per 10s, but lets play it safe

    def __init__(self):
        self.tokens = self.TOKENS
        self.updated_at = time.monotonic()

    def add_new_tokens(self):
        now = time.monotonic()
        if now - self.updated_at >= self.INTERVAL:
            self.updated_at = now
            self.tokens = self.TOKENS

    async def wait_for_token(self):
        while self.tokens < 1:
            self.add_new_tokens()
            await asyncio.sleep(1)

        self.tokens -= 1

    async def get(self, client, url, *args, **kwargs):
        await self.wait_for_token()
        response = client.get(url, *args, **kwargs)
        if response.status == 429:
            logger.info('got 429 accessing %s', url)
            self.tokens = 0

            try:
                retry_after = int(response.headers['Retry-After'])
                logger.info('retrying %s in %ds', url, retry_after)
                await asyncio.sleep(retry_after)
                return self.get(client, url, *args, **kwargs)
            except (KeyError, ValueError):
                logger.warning('bad Retry-After, got %s', response.headers)

        return response


LIMITER = RateLimiter()


@async_lru_cache(maxsize=256)
async def get_champ(cid):
    assert TOKEN
    logger.debug('get_champ(%s)', cid)
    url = API_CHAMP.format(cid)
    async with aiohttp.ClientSession() as client:
        async with LIMITER.get(client, url, headers=API_HEADERS) as response:
            assert response.status == 200
            return await response.json()


@async_lru_cache(maxsize=2)
async def get_champs():
    assert TOKEN
    logger.debug('get_champs()')
    url = API_CHAMPS
    async with aiohttp.ClientSession() as client:
        async with LIMITER.get(client, url, headers=API_HEADERS) as response:
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
        async with LIMITER.get(client, url, headers=API_HEADERS) as response:
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
