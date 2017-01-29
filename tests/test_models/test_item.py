from hypothesis import example, given, strategies

from league_utils.models import Item


@given(strategies.integers(), strategies.integers())
@example(0, 0)
@example(0, 1)
def test_equality(l, r):
    if l == r:
        assert Item(l) == Item(r)
    else:
        assert Item(l) != Item(r)
