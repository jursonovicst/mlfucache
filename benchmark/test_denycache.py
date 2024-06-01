from unittest import TestCase

from denycache import DenyCache


class TestDenyCache(TestCase):
    def test_denycache(self):
        c = DenyCache(3, allow={1, 2})
        self.assertEqual(3, c.maxsize)

        self.assertDictEqual(dict(c), {})

        c[1] = None
        self.assertDictEqual(dict(c), {1: None})

        c[1] = None
        self.assertDictEqual(dict(c), {1: None})

        c[2] = None
        self.assertDictEqual(dict(c), {1: None, 2: None})

        c[3] = None
        self.assertDictEqual(dict(c), {1: None, 2: None, 3: None})

        c[4] = None
        self.assertDictEqual(dict(c), {1: None, 2: None, 4: None})

        c[2] = None
        self.assertDictEqual(dict(c), {1: None, 2: None, 4: None})

        c[4] = None
        self.assertDictEqual(dict(c), {1: None, 2: None, 4: None})
