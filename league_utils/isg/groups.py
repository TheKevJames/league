import league_utils.api as api
import league_utils.models as models


def all_():
    return [models.Item(x['id'], x['name']) for x in api.get_item()]


def boots():
    return [
        models.Item('3158', 'Ionian Boots of Lucidity'),
        models.Item('3006', "Berserker's Greaves"),
        models.Item('3009', 'Boots of Swiftness'),
        models.Item('3020', "Sorcerer's Shoes"),
        models.Item('3047', 'Ninja Tabi'),
        models.Item('3111', 'Mercury Treads'),
        models.Item('3117', 'Boots of Mobility'),
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
        models.Item('2031', 'Refillable Potion'),
        models.Item('2043', 'Vision Ward'),
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
        ('1054', "Doran's Shield"),
        ('1055', "Doran's Blade"),
        ('1056', "Doran's Ring"),
        ('1083', 'Cull'),
    ]


def enchantments():
    return [
        models.Item('1301', 'Enchantment: Alacrity'),
        models.Item('1302', 'Enchantment: Captain'),
        models.Item('1303', 'Enchantment: Distortion'),
        models.Item('1305', 'Enchantment: Furor'),
        models.Item('1306', 'Enchantment: Alacrity'),
        models.Item('1307', 'Enchantment: Captain'),
        models.Item('1308', 'Enchantment: Distortion'),
        models.Item('1317', 'Enchantment: Captain'),
        models.Item('1320', 'Enchantment: Furor'),
        models.Item('1322', 'Enchantment: Captain'),
        models.Item('1323', 'Enchantment: Distortion'),
        models.Item('1328', 'Enchantment: Distortion'),
        models.Item('1330', 'Enchantment: Furor'),
        models.Item('1331', 'Enchantment: Alacrity'),
        models.Item('1409', 'Enchantment: Cinderhulk'),
        models.Item('1413', 'Enchantment: Cinderhulk'),
        models.Item('1414', 'Enchantment: Runic Echoes'),
        models.Item('3241', 'Enchantment: Alacrity'),
        models.Item('3671', 'Enchantment: Warrior'),
        models.Item('3673', 'Enchantment: Runic Echoes'),
        models.Item('3675', 'Enchantment: Bloodrazor'),
    ]
