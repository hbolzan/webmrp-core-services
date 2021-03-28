import unittest
from logic import resolver


class BuildResolverTests(unittest.TestCase):
    def test_resolve(self):
        self.assertEqual(
            resolver.child_to_query(
                ["legacy.contacts", {"parent": "customer"}],
                ["legacy.customers", {}],
                {"id": 2, "name": "aaaa"}
            ),
            ["legacy.contacts", {"filter": [{"customer": 2}]}]
        )

        self.assertEqual(
            resolver.child_to_query(
                ["legacy.addresses", {"parent": "customer"}],
                ["legacy.customers", {}],
                {"id": 1, "name": "aaaa"}
            ),
            ["legacy.addresses", {"filter": [{"customer": 1}]}]
        )

        self.assertEqual(
            resolver.child_to_query(
                ["legacy.addresses", {"parent": "customer"}],
                ["legacy.customers", {"pk": "number"}],
                {"number": 1, "name": "aaaa"}
            ),
            ["legacy.addresses", {"filter": [{"customer": 1}]}]
        )
