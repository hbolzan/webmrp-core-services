import unittest
from logic import resolve


class BuildResolveTests(unittest.TestCase):
    def test_query(self):
        self.assertEqual(resolve.resolve(""), "")
