import unittest
from logic import query


class BuildQueryTests(unittest.TestCase):
    def test_where(self):
        self.assertEqual(query.where(""), "")
        self.assertEqual(
            query.where("x like '%a%' and y > 1"),
            "where x like '%a%' and y > 1"
        )

    def test_order_by(self):
        self.assertEqual(query.order_by(""), "")
        self.assertEqual(query.order_by("z"), "order by z")

    def test_default_select(self):
        self.assertEqual(query.default_select("items", "", ""), "select * from items")
        self.assertEqual(query.default_select("items", "x > 1", ""), "select * from items where x > 1")
        self.assertEqual(query.default_select("items", "", "z"), "select * from items order by z")

    def test_params_to_search_where(self):
        self.assertEqual(query.params_to_search_where({}), "")
        self.assertEqual(
            query.params_to_search_where({"searchValue": "xyz", "searchFields": "a,b,c"}),
            "cast(a as varchar) ilike '%xyz%' or cast(b as varchar) ilike '%xyz%' or cast(c as varchar) ilike '%xyz%'"
        )

    def test_from_index(self):
        self.assertEqual(query.from_index({}, "items"), ("items", "items", "id"))
        self.assertEqual(
            query.from_index({"items": {"source": "view_items"}}, "items"),
            ("view_items", "items", "id")
        )
        self.assertEqual(
            query.from_index({"items": {"source": "view_items", "singular": "item", "pk": "code"}}, "items"),
            ("view_items", "item", "code")
        )
