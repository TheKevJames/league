import league_utils.models as models


def test_equality():
    bot = models.Lane('Bot')
    assert bot == bot

    mid = models.Lane('Mid')
    assert bot != mid

    mid_copy = models.Lane('Mid')
    assert mid == mid_copy


def test_repr():
    assert str(models.Lane('Bot')) == '[bot]'
