import asyncio
import collections
import functools
import itertools
import operator


def async_lru_cache(maxsize=128):
    cache = collections.OrderedDict()
    locks = collections.defaultdict(asyncio.Lock)

    def cache_clear():
        nonlocal cache
        cache = collections.OrderedDict()

    def cache_info():
        Info = collections.namedtuple('cache_info', ['maxsize', 'cursize'])
        return Info(maxsize, len(cache))

    def decorator(fn):
        @functools.wraps(fn)
        async def memoizer(*args, **kwargs):
            key = str((args, kwargs))

            with await locks[key]:
                try:
                    cache[key] = cache.pop(key)
                except KeyError:
                    if len(cache) >= maxsize:
                        cache.popitem(last=False)

                    cache[key] = await fn(*args, **kwargs)

                return cache[key]

        memoizer.cache_clear = cache_clear
        memoizer.cache_info = cache_info
        return memoizer

    return decorator


def include(*l):
    return list(collections.OrderedDict.fromkeys(itertools.chain(*l)))


def without(lh, *rh):
    return [x for x in lh if x not in set(functools.reduce(operator.add, rh))]
