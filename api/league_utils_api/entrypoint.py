import asyncio
import json
import logging
import os

import aiohttp.web
import raven

from .models import Item


SENTRY_DSN = os.environ.get('SENTRY_DSN')

logger = logging.getLogger('test')
sentry = raven.Client(dsn=SENTRY_DSN)

ITEMS = {}


async def efficiency(request):
    try:
        iid = int(request.match_info['id'])
        if not iid in ITEMS:
            ITEMS[iid] = await Item.from_id(iid)

        return aiohttp.web.Response(status=200, text=json.dumps({
            'data': [{
                'type': 'item',
                'id': iid,
                'attributes': {
                    'cost': str(await ITEMS[iid].cost),
                    'efficiency': str(await ITEMS[iid].efficiency),
                    'worth': str(await ITEMS[iid].worth),
                }
            }]}))
    except asyncio.CancelledError:
        return aiohttp.web.Response(status=500)
    except Exception as e:
        logger.exception(e)
        sentry.captureException()
        return aiohttp.web.Response(status=500, text=json.dumps({
            'errors': [{
                'status': 500,
                'title': str(e),
            }]}))


async def ping(_request):
    return aiohttp.web.Response(text='ok')


def run():
    loop = asyncio.get_event_loop()

    app = aiohttp.web.Application()

    app.router.add_route('GET', '/ping', ping)
    app.router.add_route('GET', r'/item/{id:\d+}/efficiency', efficiency)

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
