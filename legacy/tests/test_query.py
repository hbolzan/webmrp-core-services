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

    def test_params_to_filter(self):
        self.assertEqual(query.params_to_filter({}), "")
        self.assertEqual(
            query.params_to_filter({"filterBy": "uf", "filterWith": "SP"}),
            "cast(uf as varchar) = 'SP'"
        )
        self.assertEqual(
            query.params_to_filter({"filterBy": "uf", "filterWith": "RJ"}),
            "cast(uf as varchar) = 'RJ'"
        )
        self.assertEqual(
            query.params_to_filter({"filterBy": "pais", "filterWith": "1058"}),
            "cast(pais as varchar) = '1058'"
        )
        self.assertEqual(
            query.params_to_filter({"filterBy": "pais,uf", "filterWith": "1058,SP"}),
            "cast(pais as varchar) = '1058' and cast(uf as varchar) = 'SP'"
        )

    def test_params_to_search_condition(self):
        self.assertEqual(query.params_to_search_condition({}), "")
        self.assertEqual(
            query.params_to_search_condition({"searchValue": "xyz", "searchFields": "a,b,c"}),
            "cast(a as varchar) ilike '%xyz%' or cast(b as varchar) ilike '%xyz%' or cast(c as varchar) ilike '%xyz%'"
        )
        self.assertEqual(
            query.params_to_search_condition(
                {"searchValue": "xyz", "searchFields": "b,c", "filterBy": "uf", "filterWith": "SP"}
            ),
            "(cast(uf as varchar) = 'SP') and (cast(b as varchar) ilike '%xyz%' or cast(c as varchar) ilike '%xyz%')"
        )
        self.assertEqual(
            query.params_to_search_condition(
                {"filterBy": "uf", "filterWith": "SP"}
            ),
            "cast(uf as varchar) = 'SP'"
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
