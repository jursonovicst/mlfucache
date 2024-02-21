from cachetools import Cache


class BeladyCache(Cache):
    """Least Frequently Used (LFU) cache implementation with memory."""

    def __init__(self, maxsize, future, getsizeof=None):
        Cache.__init__(self, maxsize, getsizeof)
        self.__future = future
        self.__pointer = 0

    @property
    def future(self):
        return self.__future[self.__pointer:]

#    def __setitem__(self, key, value):
#        Cache.__setitem__(self, key, value)

    def __getitem__(self, item):
#        self.__pointer += 1
#        print(self.__pointer)
        Cache.__getitem__(self, item)

    def popitem(self):
        """Remove and return the `(key, value)` pair longest not needed again."""
        key = max(self.keys(), key=self.future.index)
        return key, self.pop(key)
