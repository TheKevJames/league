import asyncio
import logging
import os
import re

import aiohttp

from ..constants import ITEM_DESCRIPTION_STAT_KEYS, ITEM_WORTH


LEAGUE_TOKEN = os.environ['LEAGUE_TOKEN']
STATIC_ITEM_API = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/item'

HTML_TAG = re.compile('<[^<]+?>')
ON_HIT_REGEX = re.compile(
    r'basic attacks deal(?: an additional)? (.*?)(?: (?:as|in))?(?: bonus)?'
    r'(?: (?:magic|physical))? damage(?: .*?)?(?: (?:on hit|vs\. monsters)).*')

logger = logging.getLogger()


class Item:
    @classmethod
    async def from_id(cls, iid):
        self = Item()
        self.iid = iid

        self._cost = 0
        self._description = ''
        self._name = ''
        self._stats = {}

        self._efficiency = None
        self._worth = None

        self._loaded = False
        return self

    @classmethod
    async def from_name(cls, name):
        url = '{}?api_key={}&itemData=all'.format(STATIC_ITEM_API,
                                                  LEAGUE_TOKEN)

        async with aiohttp.ClientSession() as c, c.get(url) as response:
            assert response.status == 200

            data = (await response.json())['data']
            item = [x for x in data.values() if x.get('name') == name]
            if not item:
                raise KeyError('Could not look up item "{}"'.format(name))

            return await Item.from_id(item[0]['id'])

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
            self._worth = sum(ITEM_WORTH[k] * v
                              for k, v in self._stats.items())
        return self._worth

    async def load_data(self):
        if self._loaded:
            return

        url = '{}/{}?api_key={}&itemData=all'.format(STATIC_ITEM_API, self.iid,
                                                     LEAGUE_TOKEN)

        try:
            async with aiohttp.ClientSession() as c, c.get(url) as response:
                assert response.status == 200
                data = await response.json()
        except Exception as e:
            logger.exception(e)
            raise KeyError('Could not look up item "{}"'.format(self.iid))

        self._cost = int(data.get('gold', {}).get('total', 0))
        self._description = data.get('description', "Missing description.")
        self._name = data.get('name', 'missing-name')

        await self.build_stats_from_description()

        self._loaded = True

    async def build_stats_from_description(self):
        def parse_value(value):
            if '%' in value:
                return 'Percent', float(value[1:-1]) / 100
            else:
                return 'Flat', float(value[1:])

        # async def from_consumable(consumable):
        #     if consumable.startswith('Restores'):
        #         # TODO: can potions be considered gold efficient?
        #         pass
        #     elif consumable.startswith('Grants +'):
        #         # TODO: can elixirs be considered gold efficient?
        #         pass
        #     else:
        #         # oracle, poro, ward
        #         return

        async def from_passive(passive):
            passive = passive.strip()

            if passive.startswith('+'):
                dvalue, dkey = passive.split(' ', 1)
                key, value = parse_value(dvalue)
                key = ITEM_DESCRIPTION_STAT_KEYS[dkey].format(key)
            elif passive.startswith('Basic attacks deal'):
                dvalue = ON_HIT_REGEX.match(passive.lower()).groups()[0]

                key = 'FlatOnHitMod'
                value = int(dvalue)
            elif passive.startswith('Grants'):
                # TODO: roa
                # logger.error(passive)
                return
            elif passive.startswith('Restores'):
                _, dvalue, dkey = passive.split(' ', 2)
                value = int(dvalue)
                if dkey == 'Health every 5 seconds.':
                    key = 'FlatHPRegenMod'
                    value /= 5
                else:
                    # TODO: some of these are parseable
                    # logger.error(passive)
                    return
            else:
                # TODO: some of these are parseable
                # logger.error(passive)
                return

            self._stats[key] = value

        async def from_stat(stat):
            if '<' in stat:
                stat = HTML_TAG.sub('', stat)
            stat = stat.strip()

            dvalue, dkey = stat.split(' ', 1)
            if dvalue == '+':
                # Sometimes used as a bullet point
                return

            key, value = parse_value(dvalue)
            key = ITEM_DESCRIPTION_STAT_KEYS[dkey].format(key)

            self._stats[key] = value

        async def from_unique(title, description):
            if '<' in description:
                description = HTML_TAG.sub('', description)
            description = description.strip(' .')

            if description.startswith('+'):
                dvalue, dkey = description.split(' ', 1)
                try:
                    dkey, dextra = dkey.split('. ', 1)
                    # dextra = 'Increases to +115 Movement Speed when out of '
                    #          'combat for 5 seconds.'
                    # TODO: unfuck this
                    if dextra.startswith('Increases to +115 Movement'):
                        # 115 - 25
                        self._stats['FlatMovementSpeedOutOfCombatMod'] = 90
                except ValueError:
                    pass

                key, value = parse_value(dvalue)
                key = ITEM_DESCRIPTION_STAT_KEYS[dkey].format(key)
            elif description.startswith('Basic attacks deal'):
                description = description.lower()

                dvalue = ON_HIT_REGEX.match(description).groups()[0]
                if "of ability power" in description:
                    flat, percent, _ = dvalue.split(' ', 2)
                    value = int(percent[2:-1]) / 100
                    value *= 100
                    value += int(flat)
                elif "target's current health" in description:
                    value = int(dvalue.split(' ', 1)[0][:-1]) / 100
                    value *= 2000
                elif "target's maximum health" in description:
                    value = int(dvalue.split(' ', 1)[0][:-1]) / 100
                    value *= 1250
                elif "total attack damage" in description:
                    low, _, high, _ = dvalue.split(' ', 3)
                    value = ((int(low[:-1]) + int(high[:-1])) / 2) / 100
                    value *= 125
                elif "your maximum health" in description:
                    flat, _, percent, _ = dvalue.split(' ', 3)
                    value = int(percent[:-1]) / 100
                    value *= 2500
                    value += int(flat)
                else:
                    value = int(dvalue)

                if 'vs. monster' in description:
                    key = 'FlatOnHitJungleMod'
                else:
                    key = 'FlatOnHitMod'
            else:
                # TODO: some of these are parseable
                # logger.error(title)
                # logger.error(description)
                return

            self._stats[key] = value

        d = self._description

        # if '<consumable>' in d:
        #    idx = d.find('</consumable>')
        #    consumable = d[idx + 14:d.find('<br>', idx)]
        #    await from_consumable(consumable)

        if '<stats>' in d:
            stats = d[d.find('<stats>') + 7:d.find('</stats>')]
            for stat in [x for x in stats.split('<br>')
                         if x and 'Limit>' not in x]:
                await from_stat(stat)

        if '<passive>' in d:
            idx = -1
            while True:
                idx = d.find('<passive>', idx + 1)
                if idx == -1:
                    break

                idx = d.find('</passive>', idx)
                description_end_idx = d.find('<br>', idx)
                if description_end_idx == -1:
                    description_end_idx = None

                description = d[idx + 10:description_end_idx]
                await from_passive(description)

        if '<unique>' in d:
            idx = -1
            while True:
                idx = d.find('<unique>', idx + 1)
                if idx == -1:
                    break

                unique_end_idx = d.find('</unique>', idx)
                description_end_idx = d.find('<br>', unique_end_idx)
                if description_end_idx == -1:
                    description_end_idx = None

                title = d[idx + 8:unique_end_idx]
                description = d[unique_end_idx + 9:description_end_idx]
                await from_unique(title, description)
