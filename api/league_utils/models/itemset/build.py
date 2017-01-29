import collections
import logging
import operator

from ...api.riot import get_items
from ...models import Item
from ...utils import include, without
from .constants import BOOTS, CONSUMABLES, CONSUMABLES_EXTRA


UNWANTED_TAGS = {'Active', 'Boots', 'Consumable', 'Jungle', 'Lane', 'Trinket'}

logger = logging.getLogger()


def boots():
    return (Item(i) for i, _ in BOOTS)


def consumables(extra=False):
    if extra:
        return (Item(i) for i, _ in CONSUMABLES + CONSUMABLES_EXTRA)

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
            counted = collections.Counter()
            for item in items:
                counted.update((await item.tags) - UNWANTED_TAGS)

            for _ in range(weight_wants(kind, r == role)):
                wants += counted

    return wants


async def reorder(items, wants):
    ratings = {}
    for item in items:
        ratings[item] = sum(wants[tag] for tag in await item.tags)

    return [item for item, rating in sorted(ratings.items(),
                                            key=operator.itemgetter(1),
                                            reverse=True)
            if rating > 0]


async def build_itemset(ckey, starts, builds, role):
    items = [Item(iid) for iid in (await get_items())['data'].keys()]
    wants = await build_wants(builds, role)
    consumes = list(consumables(extra=True))

    early = include(starts['best'][role], starts['popular'][role],
                    await reorder(boots(), wants))
    build = without(include(builds['best'][role], builds['popular'][role]),
                    early, consumes)
    options = without(await reorder(items, wants), build, early, consumes)

    isg = [
        ('Consumables', consumables()),
        ('Early & Boots', early[:10]),
        ('Build', build[:10]),
        ('Options', options[:10]),
    ]

    # TODO: py36
    # champ_items = [item for item in items
    #                if await item.required_champion == ckey]
    champ_items = []
    for item in items:
        required_champion = await item.required_champion
        if required_champion == ckey:
            champ_items.append(item)
    # END TODO
    if champ_items:
        isg.append(('Champion Items', champ_items))

    return isg
