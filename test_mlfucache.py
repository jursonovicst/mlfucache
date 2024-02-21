from unittest import TestCase

from mlfucache import MLFUCache


class TestMLFUCache(TestCase):
    def test_mlfucache(self):
        c = MLFUCache(2)
        self.assertEquals(2, c.maxsize)

        c[1] = 1
        c[2] = 2
        self.assertEquals(1, c[1])
        self.assertEquals(1, c.pop(1))
        with self.assertRaises(KeyError):
            c[1]
