from cachetools import Cache


class BeladyCache(Cache):
    """Bélády's cache implementation."""

    def __init__(self, maxsize, future, getsizeof=None):
        Cache.__init__(self, maxsize, getsizeof)
        self.__future = future
        self.__time = 0

    @property
    def time(self) -> int:
        return self.__time

    @time.setter
    def time(self, v: int) -> None:
        if v < 0:
            raise ValueError(f"None negative time: {v}")
        self.__time = v

    def popitem(self):
        """Remove and return the `(key, value)` pair longest not needed again."""
        key = max(self, key=lambda k: self.__future.index(k, self.__time) if k in self.__future else float('inf'))
        #print(f"Pop {key} at {self.time}")
        return key, self.pop(key)
