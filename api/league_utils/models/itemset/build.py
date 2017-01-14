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


async def build_itemset(champ, starts, builds, role):
    # TODO: py36 merge below lines
    item_ids = (await get_items())['data'].keys()
    items = [Item(iid) for iid in item_ids]
    wants = await build_wants(builds, role)

    consume = list(consumables())
    early = starts['best'][role] + await reorder(boots(), wants)
    build = without(builds['best'][role], early, consume)
    options = without(await reorder(items, wants), build, early, consume)[:10]

    isg = [
        ('Consumables', consume),
        ('Early & Boots', early),
        ('Build', build),
        ('Options', options),
    ]
    # TODO: py26
    # champ_items = [item for item in items
    #                if await item.required_champion == champ]
    champ_items = []
    for item in items:
        required_champion = await item.required_champion
        if required_champion == champ:
            champ_items.append(item)
    # END TODO
    if champ_items:
        isg.append(('Champion Items', champ_items))

    return isg
