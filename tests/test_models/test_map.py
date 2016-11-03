import league_utils.models as models


def test_equality():
    summoners = models.Map(11)
    assert summoners == summoners

    abyss = models.Map(12)
    assert summoners != abyss

    abyss_copy = models.Map(12)
    assert abyss == abyss_copy


def test_repr():
    assert str(models.Map(11)) == "[Summoner's Rift]"


def test_gold():
    summoners = models.Map(11)
    assert summoners.starting_gold == 500
    assert summoners.gold_per_ten == 20.4

    abyss = models.Map(12)
    assert abyss.starting_gold == 1400
    assert abyss.gold_per_ten == 50
