from cachetools import Cache


class DenyCache(Cache):
    """Bélády's cache implementation."""

    def __init__(self, maxsize, allow: set, getsizeof=None):
        Cache.__init__(self, maxsize, getsizeof)
        self.__allow = allow

    def popitem(self):
        """Remove first not on allow list"""
        try:
            key = list(set(self.keys()) - self.__allow)[0]
        except ValueError:
            raise KeyError("%s is empty" % type(self).__name__) from None
        else:
            return (key, self.pop(key))
