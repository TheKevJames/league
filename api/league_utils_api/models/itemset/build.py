import collections
import logging
import operator

from ...api.riot import get_items
from ...models import Item
from ...utils import without
from .constants import BOOTS, CONSUMABLES


UNWANTED_TAGS = {'Active', 'Boots', 'Consumable', 'Jungle', 'Lane', 'Trinket'}

logger = logging.getLogger()


def boots():
    return (Item(i) for i, _ in BOOTS)


def consumables():
    return (Item(i) for i, _ in CONSUMABLES)


def weight_wants(kind, is_role):
    return {
        ('best', True): 5,
        ('best', False): 3,
        ('popular', True): 4,
        ('popular', False): 2,
    }[(kind, is_role)]


async def build_wants(builds, role):
    wants = collections.Counter()
    for kind in ('best', 'popular'):
        for r, items in builds[kind].items():
            # TODO: py36
            # counted = collections.Counter(
            #     [(await item.tags) - UNWANTED_TAGS for item in items])
            counted = collections.Counter()
            for item in items:
                counted.update((await item.tags) - UNWANTED_TAGS)
            # END TODO

            for _ in range(weight_wants(kind, r == role)):
                wants += counted

    return wants


async def reorder(items, wants):
    # TODO: py36
    # ratings = {item: sum(wants[t] for t in await item.tags)
    #            for item in items}
    ratings = {}
    for item in items:
        ratings[item] = sum(wants[tag] for tag in await item.tags)
    # END TODO
    return [item for item, rating in sorted(ratings.items(),
                                            key=operator.itemgetter(1),
                                            reverse=True) if rating > 0]


async def build_itemset(starts, builds, role):
    # TODO: py36 merge below lines
    item_ids = (await get_items())['data'].keys()
    items = (Item(iid) for iid in item_ids)
    wants = await build_wants(builds, role)

    early = starts['best'][role] + await reorder(boots(), wants)
    build = without(builds['best'][role], early, list(consumables()))
    options = without(await reorder(items, wants), build, early,
                      list(consumables()))[:10]

    return [
        ('Consumables', consumables()),
        ('Early & Boots', early),
        ('Build', build),
        ('Options', options),
    ]