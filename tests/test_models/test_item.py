import league_utils.models as models


def test_champion_specific():
    champion_specific = [
        ('Gangplank', "Death's Daughter"),
        ('Gangplank', 'Fire at Will'),
        ('Gangplank', 'Raise Morale'),
        ('Viktor', 'Prototype Hex Core'),
        ('Viktor', 'The Hex Core mk-1'),
        ('Viktor', 'The Hex Core mk-2'),
        ('Viktor', 'Perfect Hex Core'),
    ]

    for c, n in champion_specific:
        assert models.Item(0, name=n).champion == c
