import league_utils.isg as isg


def test_boots():
    boots = isg.groups.boots()
    assert len(boots) == 7


def test_biscuits():
    biscuits = isg.groups.biscuits()
    assert len(biscuits) == 2


def test_consumables():
    consumables = isg.groups.consumables()
    assert len(consumables) == 12


def test_dorans():
    dorans = isg.groups.dorans()
    assert len(dorans) == 7


def test_enchantments():
    enchantments = isg.groups.enchantments()
    assert len(enchantments) == 16
