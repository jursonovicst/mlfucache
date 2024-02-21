import collections

from cachetools import Cache


class MLFUCache(Cache):
    """Least Frequently Used (LFU) cache implementation with memory."""

    #     def __init__(self, maxsize, getsizeof=None):
    #         Cache.__init__(self, maxsize, getsizeof)
    #         self.__counter = collections.Counter()

    def __init__(self, maxsize, getsizeof=None):
        Cache.__init__(self, maxsize, getsizeof)
        self.__counter = collections.Counter()
        self.__parked = collections.Counter()

    #     def __getitem__(self, key, cache_getitem=Cache.__getitem__):
    #         value = cache_getitem(self, key)
    #         if key in self:  # __missing__ may not store item
    #             self.__counter[key] -= 1
    #         return value

    def __getitem__(self, key, cache_getitem=Cache.__getitem__):
        value = cache_getitem(self, key)
        if key in self:  # __missing__ may not store item
            self.__counter[key] -= 1 if key not in self.__parked else self.__parked.pop(key) + 1
        return value

    #     def __setitem__(self, key, value, cache_setitem=Cache.__setitem__):
    #         cache_setitem(self, key, value)
    #         self.__counter[key] -= 1

    def __setitem__(self, key, value, cache_setitem=Cache.__setitem__):
        cache_setitem(self, key, value)
        self.__counter[key] -= 1 if key not in self.__parked else self.__parked.pop(key) + 1

    #     def __delitem__(self, key, cache_delitem=Cache.__delitem__):
    #         cache_delitem(self, key)
    #         del self.__counter[key]

    def __delitem__(self, key, cache_delitem=Cache.__delitem__):
        cache_delitem(self, key)
        self.__parked[key] = -self.__counter.pop(key)  # <-- this is new

    # no change
    def popitem(self):
        """Remove and return the `(key, value)` pair least frequently used."""
        try:
            ((key, _),) = self.__counter.most_common(1)
        except ValueError:
            raise KeyError("%s is empty" % type(self).__name__) from None
        else:
            return (key, self.pop(key))
