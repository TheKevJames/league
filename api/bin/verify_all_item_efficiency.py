#!/usr/bin/env python3
import asyncio

import aiohttp
import requests


response = requests.get(
    'http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/item.json')

async def get_item(iid):
    url = 'http://127.0.0.1:28006/item/{}/efficiency'.format(iid)
    async with aiohttp.ClientSession() as client, client.get(url) as resp:
        assert resp.status == 200
        return await resp.json()

async def get_all():
    done, _ = await asyncio.wait([asyncio.ensure_future(get_item(x))
                                  for x in response.json()['data'].keys()])
    itms = {}
    for f in done:
        body = await f
        itms[body['data'][0]['id']] = body['data'][0]['attributes']
    return itms

loop = asyncio.get_event_loop()
items = loop.run_until_complete(asyncio.ensure_future(get_all()))
