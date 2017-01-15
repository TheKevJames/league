import asyncio
import sys

import aiohttp
import aiohttp.web
import docopt
import tqdm

from .api.championgg import reset_cache as reset_championgg_cache
from .api.riot import reset_cache as reset_riot_cache
from .cli import get_itemsets, parse_champs, save_itemset, Output
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


def isg():
    """league-utils Item Set Generator.

Usage:
  league-utils-isg [options]

Options:
  --champ=<champ>     Get info for only this champion (by name or id).
  --path=<path>       Override the path to your LoL installation.
                      By default, this is:
                      "C:\\Program Files\\Riot Games\\League of Legends"
"""
    # TODO: catch KeyboardInterrupt
    args = docopt.docopt(isg.__doc__, version='1.0.0', argv=sys.argv[1:])

    output = Output(args['--path'])
    print('Using League install path: {}'.format(output.path))

    loop = asyncio.get_event_loop()
    champ = loop.run_until_complete(parse_champs(args['--champ']))
    if not champ:
        print('Could not find champion {}'.format(args['--champ']))
        return

    output.ensure_paths(champ)
    roles = ['Top', 'Jungle', 'Mid', 'ADC', 'Support']

    print('Downloading itemsets...')
    tasks = get_itemsets(champ, roles)
    itemsets = loop.run_until_complete(tasks)

    print('Saving itemsets...')
    for (ckey, role, iset) in tqdm.tqdm([x for x in itemsets if all(x)]):
        save_itemset(ckey, role, iset, output)
