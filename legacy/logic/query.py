from .misc import identity

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


def to_filter(params):
    return " and ".join(
        map(
            lambda filter_by, filter_with: "cast({} as varchar) = '{}'".format(filter_by, filter_with),
            params.get("filterBy").split(","), params.get("filterWith").split(",")
        )
    )


def params_to_filter(params):
    return "" if not params.get("filterBy") else to_filter(params)


def to_search_condition(params):
    return " or ".join(
        list(map(
            lambda f: "cast({} as varchar) ilike '%{}%'".format(f, params.get("searchValue")),
            filter(lambda x: x, params.get("searchFields", "").split(","))
        ))
    )


def params_to_search_condition(params):
    search_filter = params_to_filter(params)
    search_condition = to_search_condition(params)
    if search_filter and search_condition:
        return "({}) and ({})".format(search_filter, search_condition)
    return search_filter or search_condition


def from_index(resources_index, source_name):
    source = resources_index.get(
        source_name,
        {"source": source_name, "singular": source_name, "pk": "id"}
    )
    return {
        "source": source.get("source", source_name),
        "singular": source.get("singular", source_name),
        "query_pk": source.get("query_pk", "id"),
        "pk": source.get("pk", "id"),
        "exclude_from_upsert": source.get("exclude_from_upsert", []),
        "before_post": source.get("before_post", {}),
    }


def is_number(x):
    t = type(x)
    return t == int or t == float


def single_quoted_str(s):
    return "'{}'".format(s)


def maybe_quoted_str(v):
    return str(v) if is_number(v) else single_quoted_str(v)


def with_before_post(resource, payload, k, v):
    fn = resource.get("before_post", {}).get(k, identity)
    return fn(payload, v)


def edit_set(payload, resource):
    return ", ".join(
        [
            k + " = " + maybe_quoted_str(with_before_post(resource, payload, k, v))
            for (k, v) in payload.items()
            if k != "__pk__" and k != resource.pk and k not in resource["exclude_from_upsert"]
        ]
    )


def append_set(payload, resource):
    fields = {
        k: with_before_post(resource, payload, k, v) for k, v in payload.items()
        if v is not None and k != resource["pk"] and k not in resource["exclude_from_upsert"]
    }
    return [
        fields.keys(),
        [maybe_quoted_str(v) for v in fields.values()],
    ]
