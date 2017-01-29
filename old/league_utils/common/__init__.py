from collections import OrderedDict
import functools
import operator


def dedup(l):
    return list(OrderedDict.fromkeys(l))


def without(lh, *rh):
    return [x for x in lh if x not in set(functools.reduce(operator.add, rh))]
