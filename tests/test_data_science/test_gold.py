import league_utils.data_science.gold as gold


def test_passively_generated():
    assert gold.passively_generated(100000, 0, 0) == 0

    assert gold.passively_generated(1, 1100, 1000) == 10
    assert gold.passively_generated(1, 110, 100) == 1

    assert gold.passively_generated(
        1, gold.PASSIVE_ENABLED + 20, gold.PASSIVE_ENABLED) == 2
    assert gold.passively_generated(
        1, gold.PASSIVE_ENABLED + 20, 0) == 2
