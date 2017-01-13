import asyncio
import logging

import aiohttp
import aiohttp.web

from .error import APIError
from .models import Item, Itemset
from .monitor import SENTRY
from .api.championgg import reset_cache as reset_championgg_cache
from .api.riot import reset_cache as reset_riot_cache


logger = logging.getLogger('test')


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
    except Exception as e:
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
    except Exception as e:
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


def run():
    loop = asyncio.get_event_loop()

    asyncio.ensure_future(reset_championgg_cache())
    asyncio.ensure_future(reset_riot_cache())

    app = aiohttp.web.Application()

    app.router.add_route('GET', '/ping', ping)
    app.router.add_route('GET', r'/item/{id:\d+}/efficiency', efficiency)
    app.router.add_route('GET', r'/champ/{id:\d+}/itemset/{role:\w+}', itemset)

    handler = app.make_handler(access_log=None)
    server = loop.create_server(handler, '0.0.0.0', 8080)
    srv = loop.run_until_complete(server)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(app.shutdown())
        loop.run_until_complete(handler.finish_connections(60.0))
        loop.run_until_complete(app.cleanup())
        loop.close()
