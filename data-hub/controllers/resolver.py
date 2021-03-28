import functools
from toolz.dicttoolz import assoc, dissoc
from toolz.itertoolz import first, second
from ..logic.resolver import child_to_query


def resolve(provider, query):
    resource, params = query
    provider_name, source = resource.split(".")
    data = list(
        with_children(
            provider,
            query,
            provider(provider_name).resolve([source, dissoc(params, "children")])
        )
    )
    return first(data) if params.get("one") else data


def with_children(provider, parent, data):
    return map(lambda row: row_with_children(provider, parent, row), data)


def row_with_children(provider, parent, row):
    _, params = parent
    children = params.get("children")
    if children:
        return functools.reduce(
            lambda r, child_key: with_child(provider, parent, child_key, children.get(child_key), r),
            children.keys(),
            row,
        )
    return row


def with_child(provider, parent, child_key, child, row):
    return assoc(row, child_key, resolve(provider, child_to_query(child, parent, row)))
