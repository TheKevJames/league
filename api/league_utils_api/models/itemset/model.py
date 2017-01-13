import asyncio
import logging

import aiohttp

from ...api.championgg import get_itemsets_best, get_itemsets_popular
from ...api.riot import get_champ
from ...error import APIError
from ...models import Item
from .build import build_itemset


logger = logging.getLogger()


class Itemset:
    def __init__(self):
        self.cid = None
        self.role = None

        self._ckey = ''
        self._builds = {'best': {}, 'popular': {}}
        self._starts = {'best': {}, 'popular': {}}

        self._blocks = []

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
        if not self._blocks:
            err = 'could not create itemset for champ {} in role {}'.format(
                self.cid, self.role)
            raise APIError(404, err)

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
            'champion': self._ckey,

            'blocks': [{
                'type': name,
                'items': [{'count': 1, 'id': str(item.iid)} for item in items],
            } for name, items in self._blocks],
        }

    async def load_data(self):
        if self._loaded:
            return

        try:
            self._ckey = (await get_champ(self.cid))['key']

            best = await get_itemsets_best(self._ckey)
            popular = await get_itemsets_popular(self._ckey)

            starts_best = await get_itemsets_best(self._ckey)
            starts_popular = await get_itemsets_popular(self._ckey)
        except (aiohttp.ClientDisconnectedError, asyncio.CancelledError):
            raise
        except AssertionError as e:
            raise APIError(404, 'champ {} does not exist'.format(self.cid))
        except Exception as e:
            logger.exception(e)
            raise APIError(500, 'error looking up champ {}'.format(self.cid))

        for iset in best:
            items = [Item(i) for i in iset['items']]

            role = iset['role'].lower()
            self._builds['best'][role] = items

            if role != self.role:
                continue

            title = 'champion.gg Best Winrate ({}%)'.format(iset['winPercent'])
            self._blocks.append((title, items))

        for iset in popular:
            items = [Item(i) for i in iset['items']]

            role = iset['role'].lower()
            self._builds['popular'][role] = items

            if role != self.role:
                continue

            title = 'champion.gg Most Popular ({}%)'.format(iset['winPercent'])
            self._blocks.append((title, items))

        for iset in starts_best:
            items = [Item(i) for i in iset['items']]
            self._starts['best'][iset['role'].lower()] = items

        for iset in starts_popular:
            items = [Item(i) for i in iset['items']]
            self._starts['popular'][iset['role'].lower()] = items

        if self._blocks:
            # Implies API had data for this champ & role
            iset = await build_itemset(self._ckey, self._starts, self._builds,
                                       self.role)
            self._blocks = iset + self._blocks

        self._loaded = True
