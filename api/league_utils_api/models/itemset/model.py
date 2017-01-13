import asyncio
import logging

import aiohttp

from ...api.championgg import get_itemsets_best, get_itemsets_popular
from ...api.riot import get_champ
from ...error import APIError
from ...models import Item


logger = logging.getLogger()


class Itemset:
    def __init__(self):
        self.cid = None
        self.role = None

        self.ckey = None

        self.blocks = []

        self._loaded = False

    @classmethod
    async def from_cid_and_role(cls, cid, role):
        self = Itemset()
        self.cid = cid
        self.role = role.lower()
        return self

    @property
    async def rendered(self):
        await self.load_data()
        return {
            'title': '{} (auto-generated)'.format(self.role),
            'map': 'SR',
            'mode': 'any',

            'type': 'custom',
            'sortrank': 1,
            'priority': False,

            'isGlobalForChampions': False,
            'associatedChampions': list(),
            'associatedMaps': [],
            'isGlobalForMaps': True,
            'champion': self.ckey,

            'blocks': [{
                'type': name,
                'items': [{'count': 1, 'id': str(item.iid)} for item in items],
            } for name, items in self.blocks],
        }

    async def load_data(self):
        if self._loaded:
            return

        try:
            self.ckey = (await get_champ(self.cid))['key']
            best = await get_itemsets_best(self.ckey)
            popular = await get_itemsets_popular(self.ckey)
        except (aiohttp.ClientDisconnectedError, asyncio.CancelledError):
            raise
        except AssertionError as e:
            raise APIError(404, 'champ {} does not exist'.format(self.cid))
        except Exception as e:
            logger.exception(e)
            raise APIError(500, 'error looking up champ {}'.format(self.cid))

        # TODO: use items from other roles as info
        for iset in best:
            if iset['role'].lower() != self.role:
                continue

            title = 'champion.gg Best Winrate ({}%)'.format(iset['winPercent'])
            # TODO: python 3.6
            # items = [await Item.from_id(i) for i in iset['items']]
            items = [Item() for _ in iset['items']]
            for item, data in zip(items, iset['items']):
                item.iid = data
            self.blocks.append((title, items))
        for iset in popular:
            if iset['role'].lower() != self.role:
                continue

            title = 'champion.gg Most Popular ({}%)'.format(iset['winPercent'])
            # TODO: python 3.6
            # items = [await Item.from_id(i) for i in iset['items']]
            items = [Item() for _ in iset['items']]
            for item, data in zip(items, iset['items']):
                item.iid = data
            self.blocks.append((title, items))

        self._loaded = True
