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
