import collections

import league_utils.api as api


class Champion(object):
    def __init__(self, id_, key=None, name=None):
        self.id = id_

        self._key = key  # itemset folder name
        self._name = name  # human-readable
        self._stats = None

        self.roles = list()
        self.builds = collections.defaultdict(list)
        self.starts = collections.defaultdict(list)

    def __repr__(self):
        return '[{} - {}]'.format(self.id, self.name)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.id)

    # riot data
    def _load_riot(self):
        info = api.riot.static_get_champion(self.id, champ_data='all')

        self._key = info['key']
        self._name = info['name']
        self._stats = info['stats']

    @property
    def key(self):
        if not self._key:
            self._load_riot()
        return self._key

    @property
    def name(self):
        if not self._name:
            self._load_riot()
        return self._name

    @property
    def stats(self):
        if not self._stats:
            self._load_riot()
        return self._stats
