import league_utils.api as api
import league_utils.models as models


def all_():
    return [models.Item(x['id'], x['name']) for x in api.get_item()]


def boots():
    return [
        # models.Item('1001', 'Boots of Speed'),
        models.Item('3006', "Berserker's Greaves"),
        models.Item('3009', 'Boots of Swiftness'),
        models.Item('3020', "Sorcerer's Shoes"),
        models.Item('3047', 'Ninja Tabi'),
        models.Item('3111', 'Mercury Treads'),
        models.Item('3117', 'Boots of Mobility'),
        models.Item('3158', 'Ionian Boots of Lucidity'),
    ]


# TODO: complete incomplete items in build
# def completed_items():
#     items = get_all()
#     incomplete = set([i.id for i in functools.reduce(
#         operator.add, [item.builds_from for item in items])])
#     return without([item for item in items if item.id not in incomplete],
#                          get_consumables(1), get_enchantments())


def biscuits():
    return [
        models.Item('2009', 'Total Biscuit of Rejuvenation'),
        models.Item('2010', 'Total Biscuit of Rejuvenation'),
    ]


def consumables():
    return [
        models.Item('2003', 'Health Potion'),
        # models.Item('2009', 'Total Biscuit of Rejuvenation'),
        # models.Item('2010', 'Total Biscuit of Rejuvenation'),
        models.Item('2055', 'Control Ward'),
        models.Item('2031', 'Refillable Potion'),
        # models.Item('2032', "Hunter's Potion"),
        # models.Item('2033', 'Corrupting Potion'),
        models.Item('2043', 'Vision Ward'),
        models.Item('2047', "Oracle's Extract"),
        # models.Item('2050', "Explorer's Ward"),  # removed in S4
        models.Item('3340', 'Warding Trinket'),
        models.Item('3341', 'Sweeping Lens'),
        models.Item('3363', 'Farsight Alteration'),
        models.Item('3364', 'Oracle Alteration'),
        models.Item('2138', 'Elixir of Iron'),
        models.Item('2139', 'Elixir of Sorcery'),
        models.Item('2140', 'Elixir of Wrath'),
    ]


def dorans():
    return [
        models.Item('1054', "Doran's Shield"),
        models.Item('1055', "Doran's Blade"),
        models.Item('1056', "Doran's Ring"),
        models.Item('1083', 'Cull'),
        models.Item('2051', "Guardian's Horn"),
        models.Item('3112', "Guardian's Orb"),
        models.Item('3184', "Guardian's Hammer"),
    ]


def enchantments():
    return [
        models.Item('1400', 'Enchantment: Warrior'),
        models.Item('1401', 'Enchantment: Cinderhulk'),
        models.Item('1402', 'Enchantment: Runic Echoes'),
        models.Item('1408', 'Enchantment: Warrior'),
        models.Item('1409', 'Enchantment: Cinderhulk'),
        models.Item('1410', 'Enchantment: Runic Echoes'),
        models.Item('1412', 'Enchantment: Warrior'),
        models.Item('1413', 'Enchantment: Cinderhulk'),
        models.Item('1414', 'Enchantment: Runic Echoes'),
        models.Item('1416', 'Enchantment: Bloodrazer'),
        models.Item('1418', 'Enchantment: Bloodrazer'),
        models.Item('1419', 'Enchantment: Bloodrazer'),
        models.Item('3671', 'Enchantment: Warrior'),
        models.Item('3672', 'Enchantment: Cinderhulk'),
        models.Item('3673', 'Enchantment: Runic Echoes'),
        models.Item('3675', 'Enchantment: Bloodrazor'),
    ]
