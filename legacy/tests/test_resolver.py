import unittest
from logic import resolver


class BuildResolverTests(unittest.TestCase):
    def test_with_one(self):
        self.assertEqual(resolver.with_one({"columns": "*"}, "", {}), {"columns": "*"})
        self.assertEqual(resolver.with_one({}, "", {"one": 1234}), {"where": "id = 1234"})

    def test_with_columns(self):
        self.assertEqual(resolver.with_columns({}, "", {}), {"columns": "*"})
        self.assertEqual(resolver.with_columns({}, "", {"columns": ["*"]}), {"columns": "*"})
        self.assertEqual(resolver.with_columns({}, "", {"columns": ["id", "name"]}), {"columns": "id, name"})
        self.assertEqual(
            resolver.with_columns({}, "", {"columns": ["id", "name", "phone"]}),
            {"columns": "id, name, phone"}
        )

    def test_with_operator(self):
        self.assertEqual(resolver.with_operator("age"), "age =")
        self.assertEqual(resolver.with_operator("age.eq"), "age =")
        self.assertEqual(resolver.with_operator("age.gt"), "age >")
        self.assertEqual(resolver.with_operator("age.gte"), "age >=")
        self.assertEqual(resolver.with_operator("age.lt"), "age <")
        self.assertEqual(resolver.with_operator("age.lte"), "age <=")
        self.assertEqual(resolver.with_operator("age.like"), "age like")
        self.assertEqual(resolver.with_operator("age.ilike"), "age ilike")

    def test_where_piece(self):
        self.assertEqual(resolver.where_piece("name", "My Name") , "name = 'My Name'")
        self.assertEqual(resolver.where_piece("country", "BR") , "country = 'BR'")
        self.assertEqual(resolver.where_piece("level", 1) , "level = 1")
        self.assertEqual(resolver.where_piece("value", 12.34) , "value = 12.34")
        self.assertEqual(resolver.where_piece("age.gt", 18) , "age > 18")

    def test_and_filter(self):
        self.assertEqual(resolver.and_filter({"name": "My Name"}), "name = 'My Name'")
        self.assertEqual(resolver.and_filter({"country": "BR"}), "country = 'BR'")
        self.assertEqual(
            resolver.and_filter({"country": "BR", "name": "My Name"}),
            "country = 'BR' AND name = 'My Name'"
        )
        self.assertEqual(
            resolver.and_filter({"country": "BR", "age.gte": 18}),
            "country = 'BR' AND age >= 18"
        )

    def test_with_filter(self):
        self.assertEqual(resolver.with_filter({}, "", {}), {})
        self.assertEqual(
            resolver.with_filter({}, "", {"filter": [{"name": "My Name"}]}),
            {"where": "(name = 'My Name')"}
        )

        self.assertEqual(
            resolver.with_filter({}, "", {"filter": [{"country": "BR"}]}),
            {"where": "(country = 'BR')"}
        )

        self.assertEqual(
            resolver.with_filter({}, "", {"filter": [{"country": "BR", "age.gte": 18}, {"age.gte": 21}]}),
            {"where": "(country = 'BR' AND age >= 18) OR (age >= 21)"}
        )

    def test_with_order_by(self):
        self.assertEqual(resolver.with_order_by({}, "", {}), {})
        self.assertEqual(resolver.with_order_by({}, "", {"order_by": ["id"]}), {"order_by": "id"})

    def test_resolve(self):
        self.assertEqual(resolver.resolve(["fornecedores", {}]), {"columns": "*", "source": "fornecedores"})
        self.assertEqual(resolver.resolve(["customers", {}]), {"columns": "*", "source": "customers"})

        self.assertEqual(
            resolver.resolve(["customers", {"one": 1234}]),
            {"columns": "*", "source": "customers", "where": "id = 1234"}
        )

        self.assertEqual(
            resolver.resolve(["customers", {"pk": "number", "one": 1234}]),
            {"columns": "*", "source": "customers", "where": "number = 1234"}
        )

        self.assertEqual(
            resolver.resolve(["customers", {"columns": ["id", "name"]}]),
            {"columns": "id, name", "source": "customers"}
        )

        self.assertEqual(
            resolver.resolve(
                [
                    "customers",
                    {
                        "one": 1234,
                        "columns": ["id", "name"],
                        "filter": [{"country": "BR", "age.gte": 18}, {"age.gte": 21}],
                        "filter": [{"country": "BR", "age.gte": 18}, {"age.gte": 21}],
                    }
                ]
            ),
            {
                "columns": "id, name", "source": "customers",
                "where": "(id = 1234) AND ((country = 'BR' AND age >= 18) OR (age >= 21))"
            }
        )

        self.assertEqual(
            resolver.resolve(
                [
                    "customers",
                    {
                        "one": 1234,
                        "columns": ["id", "name"],
                        "filter": [{"country": "BR", "age.gte": 18}, {"age.gte": 21}],
                        "order_by": ["country", "name", "id"],
                    }
                ]
            ),
            {
                "columns": "id, name",
                "source": "customers",
                "where": "(id = 1234) AND ((country = 'BR' AND age >= 18) OR (age >= 21))",
                "order_by": "country, name, id",
            }
        )

    def test_to_sql(self):
        self.assertEqual(resolver.to_sql({"source": "customers"}), "SELECT * FROM customers")
        self.assertEqual(resolver.to_sql({"source": "countries"}), "SELECT * FROM countries")

        self.assertEqual(
            resolver.to_sql({"source": "customers", "columns": "id, name"}),
            "SELECT id, name FROM customers"
        )

        self.assertEqual(
            resolver.to_sql({"source": "customers", "columns": "id, name", "where": "country = 'BR'"}),
            "SELECT id, name FROM customers WHERE country = 'BR'"
        )

        self.assertEqual(
            resolver.to_sql({
                "source": "customers",
                "columns": "id, name",
                "where": "country = 'BR'",
                "order_by": "country, name, id",
            }),
            "SELECT id, name FROM customers WHERE country = 'BR' ORDER BY country, name, id"
        )
