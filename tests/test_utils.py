import collections

from hypothesis import given, strategies

from league_utils.utils import include, without


@given(strategies.lists(strategies.integers()))
def test_include_single_arg(l):
    assert include(l) == list(collections.OrderedDict.fromkeys(l))


@given(strategies.lists(strategies.integers()),
       strategies.lists(strategies.integers()),
       strategies.lists(strategies.integers()))
def test_include_mutliple_args(a, b, c):
    assert include(a, b, c) == \
        list(collections.OrderedDict.fromkeys(a + b + c))


def test_include_ranges():
    assert include(range(10), range(10)) == list(range(10))
    assert include(range(10), range(15)) == list(range(15))


@given(strategies.lists(strategies.integers()),
       strategies.lists(strategies.integers()),
       strategies.lists(strategies.integers()))
def test_without(a, b, c):
    assert without(a, b, c) == [x for x in a if x not in b and x not in c]
