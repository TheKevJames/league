import collections
import functools


def async_lru_cache(maxsize=128):
    cache = collections.OrderedDict()

    def cache_clear():
        nonlocal cache
        cache = collections.OrderedDict()

    def decorator(fn):
        @functools.wraps(fn)
        async def memoizer(*args, **kwargs):
            key = str((args, kwargs))

            try:
                cache[key] = cache.pop(key)
            except KeyError:
                if len(cache) >= maxsize:
                    cache.popitem(last=False)

                cache[key] = await fn(*args, **kwargs)

            return cache[key]

        memoizer.cache_clear = cache_clear
        return memoizer

    return decorator
