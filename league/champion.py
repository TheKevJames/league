import collections
import json
import os

import bs4
import requests

from .api import api
from .item import Item
from .item import get_boots
from .item import get_consumables
from .item import without_items
from .item_set import make_block
from .item_set import make_set
from .role import Role
from .tag import get_wanted_order
from .tag import get_wants


class Champion(object):
    def __init__(self, id_, key=None, name=None):
        self.id = id_

        self._key = key  # itemset folder name
        self._name = name  # human-readable

        self._roles = None
        self._stats = None

        self._builds = collections.defaultdict(list)
        self._starts = collections.defaultdict(list)

    def __repr__(self):
        return '[{} - {}]'.format(self.id, self.name)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.id)

    def get_champion_page(self, role=None):
        url = 'http://champion.gg/champion/{}'.format(self.key)
        if role:
            url += '/{}'.format(role.name)

        return url

    def _load(self):
        info = api.static_get_champion(self.id, champ_data='all')
        self._key = info['key']
        self._name = info['name']
        self._stats = info['stats']

    @property
    def key(self):
        if not self._key:
            self._load()
        return self._key

    @property
    def name(self):
        if not self._name:
            self._load()
        return self._name

    @property
    def roles(self):
        if not self._roles:
            resp = requests.get(self.get_champion_page())
            soup = bs4.BeautifulSoup(resp.text, 'html.parser')
            self._roles = set([
                Role(x.text.strip())
                for x in soup.select('.champion-profile ul li a h3')])
        return self._roles

    @property
    def stats(self):
        if not self._stats:
            self.load()
        return self._stats

    def builds(self, role):
        if role not in self.roles:
            raise Exception('No data available for {} {}'.format(self, role))

        if not self._builds[role]:
            resp = requests.get(self.get_champion_page(role))
            soup = bs4.BeautifulSoup(resp.text, 'html.parser')
            self._builds[role] = [
                Item(x['src'].split('/')[-1].split('.')[0], x['tooltip'])
                for x in soup.select('.col-md-7 .build-wrapper a img')]
        return self._builds[role]

    def starts(self, role):
        if role not in self.roles:
            raise Exception('No data available for {} {}'.format(self, role))

        if not self._starts[role]:
            resp = requests.get(self.get_champion_page(role))
            soup = bs4.BeautifulSoup(resp.text, 'html.parser')
            self._starts[role] = [
                Item(x['src'].split('/')[-1].split('.')[0], x['tooltip'])
                for x in soup.select('.col-md-5 .build-wrapper a img')]
        return self._starts[role]

    def wants(self, role):
        return get_wants([build.tags for build in self.builds(role)])

    def sets(self, folder=None):
        for role in self.roles:
            consumables = get_consumables()
            early = list(collections.OrderedDict.fromkeys(
                without_items(self.starts(role), get_consumables(1)) + \
                get_wanted_order(self.wants(role), get_boots())))
            build = list(collections.OrderedDict.fromkeys(
                without_items(self.builds(role), get_consumables(1), early)))

            data = make_set(
                role.name, 'SR', self.key,
                [make_block('Consumables', consumables),
                 make_block('Early & Boots', early),
                 make_block('Build', build)])

            if not folder:
                print(json.dumps(data))
                continue

            fl = os.path.join(folder, '{}_{}.json'.format(self.key, role.name))
            with open(fl, 'w') as f:
                f.write(json.dumps(data))


def get_all():
    champs = []
    for champ in api.static_get_champion_list()['data'].values():
        champs.append(Champion(champ['id'], champ['key'], champ['name']))
    return champs
