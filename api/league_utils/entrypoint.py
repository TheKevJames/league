import asyncio

import aiohttp
import aiohttp.web

from .api.championgg import reset_cache as reset_championgg_cache
from .api.riot import reset_cache as reset_riot_cache
from .server import champs, efficiency, itemset, ping


def api():
    loop = asyncio.get_event_loop()

    asyncio.ensure_future(reset_championgg_cache())
    asyncio.ensure_future(reset_riot_cache())

    app = aiohttp.web.Application()

    app.router.add_route('GET', '/ping', ping)
    app.router.add_route('GET', r'/item/{id:\d+}/efficiency', efficiency)
    app.router.add_route('GET', r'/champ', champs)
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
