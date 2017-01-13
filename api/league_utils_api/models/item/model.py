import asyncio
import logging

import aiohttp

from ...error import APIError
from ...api.riot import get_item
from .stats import build_stats
from .worth import calculate_worth, split_stats


logger = logging.getLogger()


class Item:
    def __init__(self):
        self.iid = None

        self._cost = 0
        self._description = ''
        self._name = ''
        self._stats = {}

        self._efficiency = None
        self._ignored_stats = {}
        self._included_stats = {}
        self._worth = None

        self._loaded = False

    @classmethod
    async def from_id(cls, iid):
        self = Item()
        self.iid = iid
        return self

    @property
    async def cost(self):
        await self.load_data()
        return self._cost

    @property
    async def description(self):
        await self.load_data()
        return self._description

    @property
    async def efficiency(self):
        if self._efficiency is None:
            try:
                self._efficiency = (await self.worth) / (await self.cost)
                self._efficiency = round(self._efficiency, 3)
            except ZeroDivisionError:
                self._efficiency = 0
        return self._efficiency

    @property
    async def ignored_stats(self):
        await self.load_data()
        return self._ignored_stats

    @property
    async def included_stats(self):
        await self.load_data()
        return self._included_stats

    @property
    async def name(self):
        await self.load_data()
        return self._name

    @property
    async def stats(self):
        await self.load_data()
        return self._stats

    @property
    async def worth(self):
        await self.load_data()
        if self._worth is None:
            self._worth = calculate_worth(self._stats)

            ignored, included = split_stats(self._stats)
            self._ignored_stats.update(ignored)
            self._included_stats.update(included)
        return self._worth

    async def load_data(self):
        if self._loaded:
            return

        try:
            data = await get_item(self.iid)
        except (aiohttp.ClientDisconnectedError, asyncio.CancelledError):
            raise
        except AssertionError as e:
            raise APIError(404, 'item {} does not exist'.format(self.iid))
        except Exception as e:
            logger.exception(e)
            raise APIError(500, 'error looking up item {}'.format(self.iid))

        self._cost = int(data.get('gold', {}).get('total', 0))
        self._description = data.get('description', "Missing description.")
        self._name = data.get('name', 'missing-name')

        self._stats, self._ignored_stats = await build_stats(self._description)

        self._loaded = True
