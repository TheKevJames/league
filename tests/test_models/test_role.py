import league_utils.models as models


def test_equality():
    mid = models.Role('Mid')
    assert mid == mid

    top = models.Role('Top')
    assert mid != top

    top_copy = models.Role('Top')
    assert top == top_copy


def test_repr():
    assert str(models.Role('Jungle')) == '[Jungle]'
