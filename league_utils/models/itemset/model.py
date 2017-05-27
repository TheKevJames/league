import asyncio
import logging

import aiohttp

from ...api.championgg import get_itemsets_best, get_itemsets_popular
from ...api.championgg import get_itemstarts_best, get_itemstarts_popular
from ...api.riot import get_champ
from ...error import APIError
from ...models import Item
from .build import build_itemset


logger = logging.getLogger()


class Itemset:
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.cid = None
        self.role = None

        self._ckey = ''
        self._builds = {'best': {}, 'popular': {}}
        self._starts = {'best': {}, 'popular': {}}

        self._blocks = []
        self._roles = []

        self._loaded = False

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.cid == other.cid \
            and self.role == other.role

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash('{}-{}'.format(self.cid, self.role))

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

    @property
    async def roles(self):
        await self.load_data()
        return self._roles

    async def load_data(self):
        def convert_role(r):
            # TODO: create role model (heh)
            r = r.lower()
            if r == 'duo_support':
                return 'support'
            elif r == 'duo_carry':
                return 'adc'
            return r

        if self._loaded:
            return

        try:
            self._ckey = (await get_champ(self.cid))['key']
        except (aiohttp.ClientDisconnectedError, asyncio.CancelledError):
            raise
        except AssertionError as e:
            raise APIError(404, 'champ {} does not exist'.format(self.cid))
        except Exception as e:
            logger.exception(e)
            raise APIError(500, 'error looking up champ {}'.format(self.cid))

        best = asyncio.ensure_future(get_itemsets_best(self.cid))
        pop = asyncio.ensure_future(get_itemsets_popular(self.cid))
        sbest = asyncio.ensure_future(get_itemstarts_best(self.cid))
        spop = asyncio.ensure_future(get_itemstarts_popular(self.cid))

        winrate = '?'
        for iset in await best:
            role = convert_role(iset['role'])
            items = [Item(i) for i in iset['items']]
            if role == self.role:
                winrate = '{0:.3f}'.format(iset['winrate'] * 100)

            self._builds['best'][role] = items

        for iset in await pop:
            role = convert_role(iset['role'])
            items = [Item(i) for i in iset['items']]

            self._builds['popular'][role] = items

        for iset in await sbest:
            role = convert_role(iset['role'])
            items = [Item(i) for i in iset['items']]

            self._starts['best'][role] = items

        for iset in await spop:
            role = convert_role(iset['role'])
            items = [Item(i) for i in iset['items']]

            self._starts['popular'][role] = items

        self._roles = self._builds['best'].keys()
        if self.role in self._roles:
            title = 'champion.gg Best Winrate ({}%)'.format(winrate)
            self._blocks.append((title, self._builds['best'][self.role]))

            # Implies API had data for this champ & role
            iset = await build_itemset(self._ckey, self._starts, self._builds,
                                       self.role)
            self._blocks = iset + self._blocks

        self._loaded = True
