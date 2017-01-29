import league_utils.models as models


def test_champion_specific():
    champion_specific = [
        ('Gangplank', "Death's Daughter"),
        ('Gangplank', 'Fire at Will'),
        ('Gangplank', 'Raise Morale'),
        ('Kalista', 'The Black Spear'),
        ('Viktor', 'Prototype Hex Core'),
        ('Viktor', 'The Hex Core mk-1'),
        ('Viktor', 'The Hex Core mk-2'),
        ('Viktor', 'Perfect Hex Core'),
    ]

    for c, n in champion_specific:
        assert models.Item(0, name=n).champion == c

    normalItem = models.Item(0, name='Boots of Swiftness')
    assert not normalItem.champion


def test_equality():
    item0 = models.Item(0)
    assert item0 == item0

    item1 = models.Item(1)
    assert item0 != item1

    item1_copy = models.Item(1)
    assert item1 == item1_copy


def test_repr():
    assert str(models.Item(99, name='Testing Helm')) == '[99 - Testing Helm]'
