import asyncio
import logging

import aiohttp

from ..api.riot import get_champs
from ..error import APIError
from ..models import Item, Itemset
from ..monitor import SENTRY


logger = logging.getLogger()


async def champs(_request):
    try:
        data = (await get_champs())['data']

        return aiohttp.web.json_response(status=200, data={
            'data': [{
                'type': 'champ',
                'id': blob['id'],
                'attributes': {
                    'id': blob['id'],
                    'key': blob['key'],
                    'name': blob['name'],
                }
            } for blob in data.values()]
        })
    except (aiohttp.ClientDisconnectedError, asyncio.CancelledError):
        return aiohttp.web.Response(status=500)
    except APIError as e:
        return aiohttp.web.json_response(status=e.status, data={
            'errors': [{
                'status': e.status,
                'title': str(e),
            }]})
    except Exception as e:  # pylint: disable=broad-except
        logger.exception(e)
        SENTRY.captureException()
        return aiohttp.web.json_response(status=500, data={
            'errors': [{
                'status': 500,
                'title': 'internal error occured',
                'detail': str(e),
            }]})


async def efficiency(request):
    try:
        iid = int(request.match_info['id'])
        item = Item(iid)

        return aiohttp.web.json_response(status=200, data={
            'data': [{
                'type': 'item',
                'id': iid,
                'attributes': {
                    'cost': str(await item.cost),
                    'efficiency': str(await item.efficiency),
                    'worth': str(round(await item.worth, 3)),

                    'ignored_stats': (await item.ignored_stats),
                    'included_stats': (await item.included_stats),
                }
            }]})
    except (aiohttp.ClientDisconnectedError, asyncio.CancelledError):
        return aiohttp.web.Response(status=500)
    except APIError as e:
        return aiohttp.web.json_response(status=e.status, data={
            'errors': [{
                'status': e.status,
                'title': str(e),
            }]})
    except Exception as e:  # pylint: disable=broad-except
        logger.exception(e)
        SENTRY.captureException()
        return aiohttp.web.json_response(status=500, data={
            'errors': [{
                'status': 500,
                'title': 'internal error occured',
                'detail': str(e),
            }]})


async def itemset(request):
    try:
        cid = int(request.match_info['id'])
        role = str(request.match_info['role'])
        iset = await Itemset.from_cid_and_role(cid, role)

        return aiohttp.web.json_response(status=200, data=await iset.rendered)
    except (aiohttp.ClientDisconnectedError, asyncio.CancelledError):
        return aiohttp.web.Response(status=500)
    except APIError as e:
        return aiohttp.web.json_response(status=e.status, data={
            'errors': [{
                'status': e.status,
                'title': str(e),
            }]})
    except Exception as e:  # pylint: disable=broad-except
        logger.exception(e)
        SENTRY.captureException()
        return aiohttp.web.json_response(status=500, data={
            'errors': [{
                'status': 500,
                'title': 'internal error occured',
                'detail': str(e),
            }]})


async def ping(_request):
    return aiohttp.web.Response(text='ok')
