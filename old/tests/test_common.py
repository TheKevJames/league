import league_utils.common as common


def test_dedup():
    assert common.dedup([1, 1, 2]) == [1, 2]
    assert common.dedup(list(range(10)) + list(range(10))) == list(range(10))


def test_without():
    items = [1, 2, 3, 4, 5]

    assert common.without(items, items[-3:]) == items[:-3]

    assert set(common.without(set(items), set(items[-2:]))) == set(items[:-2])

    assert common.without(items, items[-1:], items[:1]) == items[1:-1]
