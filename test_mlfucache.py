from unittest import TestCase

from mlfucache import MLFUCache


class TestMLFUCache(TestCase):
    def test_mlfucache(self):
        c = MLFUCache(2)
        self.assertEqual(2, c.maxsize)

        self.assertDictEqual(c._debug_c, {})
        self.assertDictEqual(c._debug_p, {})

        c[1] = None
        self.assertDictEqual(c._debug_c, {1: -1})
        self.assertDictEqual(c._debug_p, {})

        c[1] = None
        self.assertDictEqual(c._debug_c, {1: -2})
        self.assertDictEqual(c._debug_p, {})

        self.assertIsNone(c[1])
        self.assertDictEqual(c._debug_c, {1: -3})
        self.assertDictEqual(c._debug_p, {})

        c[2] = None
        self.assertDictEqual(c._debug_c, {1: -3, 2: -1})
        self.assertDictEqual(c._debug_p, {})

        c[2] = None
        self.assertDictEqual(c._debug_c, {1: -3, 2: -2})
        self.assertDictEqual(c._debug_p, {})

        c[3] = None
        self.assertDictEqual(c._debug_c, {1: -3, 3: -1})
        self.assertDictEqual(c._debug_p, {2: 2})

        c[2] = None
        self.assertDictEqual(c._debug_c, {1: -3, 2: -3})
        self.assertDictEqual(c._debug_p, {3: 1})

        with self.assertRaises(KeyError):
            c[4]
        self.assertDictEqual(c._debug_c, {1: -3, 2: -3})
        self.assertDictEqual(c._debug_p, {3: 1})

        self.assertEqual(None, c.pop(2))
        self.assertDictEqual(c._debug_c, {1: -3})
        self.assertDictEqual(c._debug_p, {3: 1, 2: 4})  # this is wrong!
