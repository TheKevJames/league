import league_utils.models as models


def test_equality():
    corki = models.Champion(42, 'Corki', 'Corki')
    assert corki == corki

    yorick = models.Champion(83, 'Yorick', 'Yorick')
    assert corki != yorick

    yorick_copy = models.Champion(83, 'Yorick', 'Yorick')
    assert yorick == yorick_copy


def test_repr():
    assert str(models.Champion(83, 'Yorick', 'Yorick')) == '[83 - Yorick]'
