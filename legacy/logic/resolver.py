import functools

def resolve(query):
    return functools.reduce(
        lambda resolved, fn: fn(resolved, *query),
        [
            with_source,
            with_columns,
            with_one,
            with_filter,
            with_order_by,
        ],
        {}
    )


def with_source(resolved, resource, _):
    return dict(resolved, **{"source": resource})


def with_columns(resolved, _, params):
    return dict(resolved, columns=", ".join(params.get("columns", ["*"])))


def with_one(resolved, _, params):
    one = params.get("one")
    if one:
        return dict(
            resolved,
            where = "{} = {}".format(params.get("pk", "id"), one)
        )
    return resolved


def with_filter(resolved, _, params):
    params_filter = params.get("filter", [])
    resolved_where = resolved.get("where")
    where = "({})".format(") OR (".join(map(and_filter, params_filter)))
    if len(params_filter) > 0:
        return dict(
            resolved,
            where = where if not resolved_where else "({}) AND ({})".format(resolved_where, where)
        )
    return resolved


def and_filter(cond):
    return " AND ".join(map(where_piece, cond.keys(), cond.values()))


def where_piece(column, value):
    template = "{} '{}'" if type(value) == str else "{} {}"
    return template.format(with_operator(column), value)


operators = {"eq": "=", "gt": ">", "gte": ">=", "lt": "<", "lte": "<=", "like": "like", "ilike": "ilike"}


def with_operator(column):
    try:
        col_name, operator = column.split(".")
    except ValueError:
        col_name, operator = column, "eq"
    return "{} {}".format(col_name, operators.get(operator))


def with_order_by(resolved, _, params):
    order_by = params.get("order_by", [])
    if len(order_by) > 0:
        return dict(
            resolved,
            order_by = ", ".join(order_by)
        )
    return resolved


def to_sql(resolved):
    return functools.reduce(
        lambda sql, fn: fn(sql, resolved),
        [
            sql_with_select_from,
            sql_with_where,
            sql_with_order_by,
        ],
        ""
    )


def sql_with_select_from(sql, resolved):
    return "SELECT {} FROM {}".format(resolved.get("columns", "*"), resolved.get("source"))


def sql_with_where(sql, resolved):
    where = resolved.get("where")
    if where:
        return "{} WHERE {}".format(sql, where)
    return sql


def sql_with_order_by(sql, resolved):
    order_by = resolved.get("order_by")
    if order_by:
        return "{} ORDER BY {}".format(sql, order_by)
    return sql
