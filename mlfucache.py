import collections

from cachetools import Cache


class MLFUCache(Cache):
    """Least Frequently Used (LFU) cache implementation."""

    def __init__(self, maxsize, getsizeof=None):
        Cache.__init__(self, maxsize, getsizeof)
        self.__counter = collections.Counter()
        self.__parked = collections.Counter()  # <-- this is new

    def __getitem__(self, key, cache_getitem=Cache.__getitem__):
        value = cache_getitem(self, key)
        if key in self:  # __missing__ may not store item
            self.__counter[key] -= 1
        return value

    def __setitem__(self, key, value, cache_setitem=Cache.__setitem__):
        cache_setitem(self, key, value)
        self.__counter[key] -= 1 if key not in self.__parked else self.__parked.pop(key) + 1  # <-- this is new

    def __delitem__(self, key, cache_delitem=Cache.__delitem__):
        cache_delitem(self, key)
        self.__parked[key] = - self.__counter.pop(key)

    def popitem(self):
        """Remove and return the `(key, value)` pair least frequently used."""
        try:
            ((key, _),) = self.__counter.most_common(1)
            self.__counter[key] += 1  # <-- this will generate an extra getitem, compensate
        except ValueError:
            raise KeyError("%s is empty" % type(self).__name__) from None
        else:
            return (key, self.pop(key))

    @property
    def _debug_c(self):
        return self.__counter

    @property
    def _debug_p(self):
        return self.__parked
