import league_utils.api as api
from .map import Map


class ItemEffects(object):
    def __init__(self, item_id, payload):
        self.item_id = item_id
        self._payload = payload

        if self.item_id == 3096:
            # Nomad's Medallion
            self.cdr = int(self._payload['Effect3Amount'])  # or 4?
            self.gold_per_farm = int(self._payload['Effect2Amount'])
            self.gold_per_ten = int(self._payload['Effect1Amount'])
            self.health_per_farm = int(self._payload['Effect4Amount'])  # or 3?
        elif self.item_id == 3097:
            # Targon's Brace
            self.charge_interval = int(self._payload['Effect3Amount'])
            self.execute_threshold = lambda level: \
                (int(self._payload['Effect1Amount']) +
                 level * int(self._payload['Effect6Amount']))
            self.gold_per_ten = int(self._payload['Effect5Amount'])
            self.health_per_farm = int(self._payload['Effect2Amount'])
            self.max_charges = int(self._payload['Effect4Amount'])
        elif self.item_id == 3098:
            # Frostfang
            self.damage_per_poke = int(self._payload['Effect2Amount'])  # 1?
            self.disable_time = int(self._payload['Effect3Amount'])
            self.full_charge_interval = int(self._payload['Effect5Amount'])
            self.gold_per_poke = int(self._payload['Effect1Amount'])  # 2?
            self.gold_per_ten = int(self._payload['Effect6Amount'])
            self.max_charges = int(self._payload['Effect4Amount'])

            self.charge_interval = self.full_charge_interval / self.max_charges
        elif self.item_id == 3301:
            # Ancient Coin
            self.gold_per_farm = int(self._payload['Effect1Amount'])
            self.health_per_farm = int(self._payload['Effect2Amount'])
        elif self.item_id == 3302:
            # Relic Shield
            self.charge_interval = 40
            self.execute_threshold = lambda level: \
                (int(self._payload['Effect1Amount']) +
                 level * int(self._payload['Effect4Amount']))
            self.gold_per_ten = int(self._payload['Effect3Amount'])
            self.health_per_farm = int(self._payload['Effect2Amount'])
            self.max_charges = 2
        elif self.item_id == 3303:
            # Spellthief's Edge
            self.damage_per_poke = int(self._payload['Effect1Amount'])
            self.disable_time = int(self._payload['Effect3Amount'])
            self.full_charge_interval = int(self._payload['Effect5Amount'])
            self.gold_per_poke = int(self._payload['Effect2Amount'])
            self.gold_per_ten = int(self._payload['Effect6Amount'])
            self.max_charges = int(self._payload['Effect4Amount'])

            self.charge_interval = self.full_charge_interval / self.max_charges

    def gold_at_time(self, time_current, time_purchase=0, **kwargs):
        import league_utils.data_science.gold as gold

        if self.item_id == 3096:
            # Nomad's Medallion
            return gold.maximum_passively_generated_from_farm(
                kwargs['lane'], self.gold_per_farm, time_current,
                farm_rate=kwargs['adc_farm_rate'], time_purchase=time_purchase)
        elif self.item_id == 3097:
            # Targon's Brace
            passive = gold.passively_generated(
                self.gold_per_ten, time_current, time_purchase=time_purchase)
            farm = gold.maximum_minion_kill(
                kwargs['lane'], time_current,
                kill_interval=self.charge_interval,
                kill_rate=kwargs['support_farm_rate'],
                time_purchase=time_purchase)
            return passive + farm
        elif self.item_id == 3098:
            # Frostfang
            passive = gold.passively_generated(
                self.gold_per_ten, time_current, time_purchase=time_purchase)
            poke = gold.poking(
                self.gold_per_poke, self.max_charges,
                self.full_charge_interval, time_current,
                poke_rate=kwargs['support_poke_rate'],
                time_purchase=time_purchase)
            return passive + poke
        elif self.item_id == 3301:
            # Ancient Coin
            return gold.maximum_passively_generated_from_farm(
                kwargs['lane'], self.gold_per_farm, time_current,
                farm_rate=kwargs['adc_farm_rate'])
        elif self.item_id == 3302:
            # Relic Shield
            passive = gold.passively_generated(self.gold_per_ten, time_current)
            farm = gold.maximum_minion_kill(
                kwargs['lane'], time_current,
                kill_interval=self.charge_interval,
                kill_rate=kwargs['support_farm_rate'])
            return passive + farm
        elif self.item_id == 3303:
            # Spellthief's Edge
            passive = gold.passively_generated(self.gold_per_ten, time_current)
            poke = gold.poking(
                self.gold_per_poke, self.max_charges,
                self.full_charge_interval, time_current,
                poke_rate=kwargs['support_poke_rate'])
            return passive + poke

        raise Exception("No gold/time function for '{}'.".format(self.item_id))


class Item(object):
    def __init__(self, id_, name=None):
        self.id = id_

        self._name = name

        self._builds_from = None
        self._champion = None
        self._champion_unlocked = False
        self._cost = None
        self._effects = None
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
        elif self.name in ('Entropy Field', 'Flash Zone',
                           'Nexus Siege: Siege Weapon Slot', 'Port Pad',
                           'Shield Totem', 'Siege Ballista', 'Siege Refund',
                           'Siege Sight Warder', 'Siege Teleport',
                           'Siege Teleport (Inactive)',
                           'Siege Warp', 'Siege Warp (Inactive)',
                           'Tower: Beam of Ruination', 'Tower: Storm Bulwark',
                           'Tower Surge: Beam of Ruination',
                           'Tower Surge: Firestorm Bulwark',
                           'Vanguard Banner'):
            # TODO: new game mode items?
            return []

        raise Exception('No tags for %r.' % self)

    # riot data
    def _load_riot(self):
        info = api.riot.static_get_item(self.id, item_data='all')

        self._builds_from = [Item(x) for x in info.get('from', list())]
        self._cost = int(info['gold']['total'])
        self._effects = ItemEffects(self.id, info.get('effect', {}))
        self._maps = {Map(k) for k, v in info['maps'].items() if v}
        self._name = info['name']
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
    def cost(self):
        if not self._cost:
            self._load_riot()
        return self._cost

    @property
    def effects(self):
        if not self._effects:
            self._load_riot()
        return self._effects

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

    def dump(self):
        if self.builds_from:
            print('{} ({})'.format(
                self, ' + '.join((str(i) for i in self.builds_from))))
        else:
            print(self)
        print('  Costs: {}g'.format(self.cost))
        print('  Provides: {}'.format(self.stats))
        print('  Tags: {}'.format(self.tags))
        print('  Available on: {}'.format(self.maps))
        # print('  {}'.format(self.effects))
