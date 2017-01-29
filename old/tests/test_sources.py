import collections

import league_utils.sources as sources


class ChampionMock(object):
    def __init__(self, key):
        self.key = key

        self.roles = list()
        self.builds = collections.defaultdict(list)
        self.starts = collections.defaultdict(list)


def test_champion_gg():
    key = 'Thresh'

    champ = ChampionMock(key)
    assert champ.key == key
    assert not champ.roles
    assert not champ.builds
    assert not champ.starts

    sources.champion_gg(champ)
    assert champ.key == key
    assert champ.roles
    assert champ.builds
    assert champ.starts
