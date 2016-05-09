from riotwatcher import game_maps

import league_utils.api as api


class Item(object):
    def __init__(self, id_, name=None):
        self.id = id_

        self._name = name

        self._builds_from = None
        self._champion = None
        self._champion_unlocked = False
        # TODO: do something with these
        #  ["Butcher's Bridge", 'Howling Abyss', "Summoner's Rift",
        #   'The Crystal Scar', 'The Proving Grounds', 'Twisted Treeline']
        self._maps = None
        # TODO: do something with these
        # ['FlatArmorMod', 'FlatCritChanceMod', 'FlatHPPoolMod',
        #  'FlatHPRegenMod', 'FlatMPPoolMod', 'FlatMPRegenMod',
        #  'FlatMagicDamageMod', 'FlatMovementSpeedMod',
        #  'FlatPhysicalDamageMod', 'FlatSpellBlockMod',
        #  'PercentAttackSpeedMod', 'PercentLifeStealMod',
        #  'PercentMovementSpeedMod']
        self._stats = None
        # TODO: do something else with these?
        # ['Active', 'Armor', 'ArmorPenetration', 'AttackSpeed', 'Aura',
        #  'Bilgewater', 'Boots', 'Consumable', 'CooldownReduction',
        #  'CriticalStrike', 'Damage', 'GoldPer', 'Health', 'HealthRegen',
        #  'Jungle', 'Lane', 'LifeSteal', 'MagicPenetration', 'Mana',
        #  'ManaRegen', 'NonbootsMovement', 'OnHit', 'Slow', 'SpellBlock',
        #  'SpellDamage', 'SpellVamp', 'Stealth', 'Tenacity', 'Trinket',
        #  'Vision']
        self._tags = None

    def __repr__(self):
        return '[{} - {}]'.format(self.id, self.name)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.id)

    # fix missing riot tags
    def _get_missing_tags(self):
        if 'Biscuit of Rejuvenation' in self.name:
            return ['Consumable', 'HealthRegen', 'ManaRegen']
        elif "Death's Daughter" in self.name:
            return ['Damage', 'Slow']
        elif 'Enchantment' in self.name:
            if any(x in self.name for x in ('Alacrity', 'Captain',
                                            'Distortion', 'Furor')):
                return ['Boots']
            elif 'Bloodrazor' in self.name:
                return ['AttackSpeed', 'Jungle', 'OnHit']
            elif 'Cinderhulk' in self.name:
                return ['Aura', 'Health', 'Jungle', 'SpellDamage']
            elif 'Runeglaive' in self.name:
                return ['CooldownReduction', 'Jungle', 'Mana', 'ManaRegen',
                        'OnHit', 'SpellDamage']
            elif 'Runic Echoes' in self.name:
                return ['Jungle', 'NonbootsMovement', 'SpellDamage']
            elif 'Warrior' in self.name:
                return ['CooldownReduction', 'Damage', 'Jungle']
        elif 'Fire at Will' in self.name:
            return ['AttackSpeed', 'Damage']
        elif 'Hex Core' in self.name:
            return ['Mana', 'SpellDamage']
        elif 'Poro-Snax' in self.name:
            return []
        elif 'Raise Morale' in self.name:
            return ['NonbootsMovement']

        raise Exception('No tags for %r.' % self)

    # riot data
    def _load_riot(self):
        info = api.riot.static_get_item(self.id, item_data='all')

        self._name = info['name']

        self._builds_from = [Item(x) for x in info.get('from', list())]

        self._maps = set()
        for map_ in [k for k, v in info['maps'].items() if v]:
            for game_map in [g for g in game_maps if str(g['map_id']) == map_]:
                self._maps.add(game_map['name'])

        self._stats = info['stats']

        try:
            self._tags = set(info['tags']) - set(['Bilgewater'])
        except KeyError:
            self._tags = set(self._get_missing_tags())

        if self.name in ('Boots of Mobility', 'Boots of Swiftness'):
            # Champions that really want movement speed should consider these
            # boots
            self._tags.add('NonbootsMovement')

    @property
    def builds_from(self):
        if isinstance(self._builds_from, type(None)):
            self._load_riot()
        return self._builds_from

    @property
    def maps(self):
        if not self._maps:
            self._load_riot()
        return self._maps

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

    @property
    def tags(self):
        if isinstance(self._tags, type(None)):
            self._load_riot()
        return self._tags

    # additional data
    @property
    def champion(self):
        if not self._champion and not self._champion_unlocked:
            if 'Hex Core' in self.name:
                self._champion = 'Viktor'
            elif self.name == 'The Black Spear':
                self._champion = 'Kalista'
            elif any(x == self.name for x in ("Death's Daughter",
                                              'Fire at Will',
                                              'Raise Morale')):
                self._champion = 'Gangplank'
            else:
                self._champion_unlocked = True
        return self._champion
