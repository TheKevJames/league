import functools
import operator


def without(lh, *rh):
    return [x for x in lh if x not in set(functools.reduce(operator.add, rh))]
