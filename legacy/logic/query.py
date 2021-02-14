def select(root_path, resource_name, condition="", order=""):
    try:
        return resource_select(root_path, resource_name, condition, order)
    except FileNotFoundError:
        return default_select(resource_name, condition, order)


def resource_select(root_path, resource_name, condition, order):
    with open("{}/sql/{}.select.sql".format(root_path, resource_name)) as f:
        return f.read().format(where=where(condition), order_by=order_by(order))


def default_select(table_name, condition, order):
    return " ".join(["select * from {}".format(table_name)] +\
        ([] if not condition else [where(condition)]) +\
        ([] if not order else [order_by(order)]))


def where(condition):
    return "" if (not condition) else "where {}".format(condition)


def order_by(order):
    return "" if (not order) else "order by {}".format(order)


if __name__ == '__main__':
    unittest.main()
