from cachetools import Cache


class BeladyCache(Cache):
    """Bélády's cache implementation."""

    def __init__(self, maxsize, future, getsizeof=None):
        Cache.__init__(self, maxsize, getsizeof)
        self.__future = future
        self.__pointer = -1

    def __getitem__(self, key, cache_getitem=Cache.__getitem__):
        self.__pointer += 1
        return cache_getitem(self, key)

    def popitem(self):
        """Remove and return the `(key, value)` pair longest not needed again."""
        key = max(self, key=lambda k: self.__future.index(k, self.__pointer) if k in self.__future else float('inf'))
        return key, self.pop(key)
