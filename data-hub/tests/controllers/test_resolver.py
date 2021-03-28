import unittest
from tests.controllers.resolver_helpers import MockedProvider, contacts, addresses
from controllers import resolver


class BuildResolverTests(unittest.TestCase):
    def test_resolve(self):
        self.assertEqual(
            resolver.resolve(MockedProvider, ["legacy.customers", {"one": 2}]),
            {"id": 2, "name": "fghi"}
        )

        self.assertEqual(
            resolver.resolve(MockedProvider, ["legacy.customers", {"filter": [{"id": 2}]}]),
            [{"id": 2, "name": "fghi"}]
        )

        self.assertEqual(
            resolver.resolve(
                MockedProvider,
                [
                    "legacy.customers",
                    {"filter": [{"id": 2}]}
                ]
            ),
            [{"id": 2, "name": "fghi"}]
        )

        self.assertEqual(
            resolver.resolve(
                MockedProvider,
                [
                    "legacy.customers",
                    {
                        "one": 2,
                        "children": {
                            "contacts": ["legacy.contacts", {"parent": "customer"}],
                        }
                    }
                ]
            ),
            {
                "id": 2,
                "name": "fghi",
                "contacts": contacts,
            }
        )

        self.assertEqual(
            resolver.resolve(
                MockedProvider,
                [
                    "legacy.customers",
                    {
                        "one": 2,
                        "children": {
                            "contacts": ["legacy.contacts", {"parent": "customer"}],
                            "addresses": ["legacy.addresses", {"parent": "customer"}],
                        }
                    }
                ]
            ),
            {
                "id": 2,
                "name": "fghi",
                "addresses": addresses,
                "contacts": contacts,
            }
        )
