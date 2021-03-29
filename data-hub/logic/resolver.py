from toolz.itertoolz import first, second


def child_to_query(child_query, parent_query, parent_record):
    child_params = second(child_query)
    parent_pk = second(parent_query).get("pk", "id")
    return [first(child_query), {"filter": [{child_params.get("parent"): parent_record.get(parent_pk)}]}]
