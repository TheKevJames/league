import functools
import operator

from riotwatcher import game_maps

from .api import api


class Item(object):
    def __init__(self, id_, name=None):
        self.id = id_

        self._name = name

        self._builds_from = None
        self._champion = None
        self._champion_unlocked = False
        self._maps = None  # ["Butcher's Bridge", 'Howling Abyss', "Summoner's Rift", 'The Crystal Scar', 'The Proving Grounds', 'Twisted Treeline']
        self._stats = None  # ['FlatArmorMod', 'FlatCritChanceMod', 'FlatHPPoolMod', 'FlatHPRegenMod', 'FlatMPPoolMod', 'FlatMPRegenMod', 'FlatMagicDamageMod', 'FlatMovementSpeedMod', 'FlatPhysicalDamageMod', 'FlatSpellBlockMod', 'PercentAttackSpeedMod', 'PercentLifeStealMod', 'PercentMovementSpeedMod']
        self._tags = None  # ['Active', 'Armor', 'ArmorPenetration', 'AttackSpeed', 'Aura', 'Bilgewater', 'Boots', 'Consumable', 'CooldownReduction', 'CriticalStrike', 'Damage', 'GoldPer', 'Health', 'HealthRegen', 'Jungle', 'Lane', 'LifeSteal', 'MagicPenetration', 'Mana', 'ManaRegen', 'NonbootsMovement', 'OnHit', 'Slow', 'SpellBlock', 'SpellDamage', 'SpellVamp', 'Stealth', 'Tenacity', 'Trinket', 'Vision']

    def __repr__(self):
        return '[{} - {}]'.format(self.id, self.name)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.id)

    def _get_missing_tags(self):
        if 'Biscuit of Rejuvenation' in self.name:
            return ['Consumable', 'HealthRegen', 'ManaRegen']
        elif 'Enchantment' in self.name:
            if any(x in self.name for x in ('Alacrity', 'Captain',
                                            'Distortion', 'Furor')):
                return ['Boots']
            elif 'Cinderhulk' in self.name:
                return ['Aura', 'Health', 'Jungle', 'SpellDamage']
            elif 'Devourer' in self.name:
                return ['AttackSpeed', 'Jungle', 'OnHit']
            elif 'Runeglaive' in self.name:
                return ['CooldownReduction', 'Jungle', 'Mana', 'ManaRegen',
                        'OnHit', 'SpellDamage']
            elif 'Runic Echoes' in self.name:
                return ['Jungle', 'NonbootsMovement', 'SpellDamage']
            elif 'Warrior' in self.name:
                return ['CooldownReduction', 'Damage', 'Jungle']
        elif 'Hex Core' in self.name:
            return ['Mana', 'SpellDamage']
        elif 'Fire at Will' in self.name:
            return ['AttackSpeed', 'Damage']
        elif "Death's Daughter" in self.name:
            return ['Damage', 'Slow']
        elif 'Raise Morale' in self.name:
            return ['NonbootsMovement']
        elif 'Poro-Snax' in self.name:
            return []

        raise Exception('No tags for %r.' % self)

    def _load(self):
        info = api.static_get_item(self.id, item_data='all')

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
    def name(self):
        if not self._name:
            self._load()
        return self._name

    @property
    def builds_from(self):
        if isinstance(self._builds_from, type(None)):
            self._load()
        return self._builds_from

    @property
    def champion(self):
        if not self._champion and not self._champion_unlocked:
            if 'Hex Core' in self.name:
                self._champion = 'Viktor'
            elif any(x in self.name for x in ("Death's Daughter",
                                              'Fire at Will', 'Raise Morale')):
                self._champion = 'Gankplank'
            else:
                self._champion_unlocked = True
        return self._champion

    @property
    def maps(self):
        if not self._maps:
            self._load()
        return self._maps

    @property
    def stats(self):
        if not self._stats:
            self._load()
        return self._stats

    @property
    def tags(self):
        if isinstance(self._tags, type(None)):
            self._load()
        return self._tags


def get_all():
    items = []
    for item in api.static_get_item_list()['data'].values():
        items.append(Item(str(item['id']), item['name']))
    return items


def get_boots():
    return [
        Item('3158', 'Ionian Boots of Lucidity]'),
        Item('3006', "Berserker's Greaves"),
        Item('3009', 'Boots of Swiftness'),
        Item('3020', "Sorcerer's Shoes"),
        Item('3047', 'Ninja Tabi'),
        Item('3111', 'Mercury Treads'),
        Item('3117', 'Boots of Mobility'),
    ]


def get_completed():
    items = get_all()
    incomplete = set([i.id for i in functools.reduce(
        operator.add, [item.builds_from for item in items])])
    return without_items([item for item in items if item.id not in incomplete],
                         get_consumables(1), get_enchantments())


def get_consumables(extras=False):
    consumables = [
        Item('2003', 'Health Potion'),
        Item('2031', 'Refillable Potion'),
        Item('2043', 'Vision Ward'),
        Item('3340', 'Warding Trinket'),
        Item('3341', 'Sweeping Lens'),
        Item('3363', 'Farsight Alteration'),
        Item('3364', 'Oracle Alteration'),
    ]
    if extras:
        consumables.append(Item('2009', 'Total Biscuit of Rejuvenation'))
        consumables.append(Item('2010', 'Total Biscuit of Rejuvenation'))
        consumables.append(Item('2138', 'Elixir of Iron'))

    return consumables


def get_enchantments():
    return [
        Item('1301', 'Enchantment: Alacrity'),
        Item('1302', 'Enchantment: Captain'),
        Item('1303', 'Enchantment: Distortion'),
        Item('1305', 'Enchantment: Furor'),
        Item('1306', 'Enchantment: Alacrity'),
        Item('1307', 'Enchantment: Captain'),
        Item('1308', 'Enchantment: Distortion'),
        Item('1317', 'Enchantment: Captain'),
        Item('1320', 'Enchantment: Furor'),
        Item('1322', 'Enchantment: Captain'),
        Item('1323', 'Enchantment: Distortion'),
        Item('1328', 'Enchantment: Distortion'),
        Item('1330', 'Enchantment: Furor'),
        Item('1331', 'Enchantment: Alacrity'),
        Item('1409', 'Enchantment: Cinderhulk'),
        Item('1413', 'Enchantment: Cinderhulk'),
        Item('1414', 'Enchantment: Runic Echoes'),
        Item('3241', 'Enchantment: Alacrity'),
        Item('3671', 'Enchantment: Warrior'),
        Item('3673', 'Enchantment: Runic Echoes'),
        Item('3674', 'Enchantment: Devourer'),
    ]


def without_items(lhs, *rhs):
    return [item for item in lhs
            if item not in set(functools.reduce(operator.add, rhs))]
