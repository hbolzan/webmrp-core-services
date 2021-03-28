# Data Hub Service

This is a data concentrator service which resolves providers and gets data from named sources.

## Single Queries

### query

### get_one


## Composite Queries

### resolve
The `resolve` method gets a composite query and resolves all its data, returning a json result, much like a GraphQL query.

Query has the following format
```
"query" = [
    "legacy.fornecedores",
    {
        "pk": "id",
        "one": id,
        "columns": ["*"],
        "children": {
            "contatos": [
                "legacy.fornecedores-contatos",
                {
                    "parent": "participante", 
                    "order_by": "nome",
                    "filter": [{"active": True}],
                }
            ],
            "enderecos": ["legacy.fornecedores-enderecos", {"parent": "participante", "order_by": ["id"]}],
        }
    }
]
```

A query is a list with two elements. The first element is a string that represents the pair `provider.source` and the second element is a dictionary with query params. Params are:

* `pk`: indicates which colum is the pk. If table pk is composite, `pk` must be a list. If `pk` is not provided, `id` will be used by default.
* `one`: retrieves a single row where the pk corresponds to the value provided to `one`.
* `columns`: list of columns to be retrieved. Default value is `["*"]`.
* `filter`: a list of conditions where each condition is a dictionary that must contain one ore more columns and matching values. The combination of columns in one condition makes an `AND` condition. The combination of conditions in a list makes an `OR` condition. Params `one` and `filter` are muttulally exclusive. Below, some examples of filters translation to SQL where clauses.
```
[{"name": "Some Name"}] => WHERE name = 'Some Name'
[{"name.ilike": "%Some Name%"}] => WHERE name ilike '%Some Name%'
[{"name.ilike": "%Some Name%", "country": "BR"}] => WHERE name ilike '%Some Name%' AND country = 'BR'

[{"country": "BR", "age.gte": 18}, {"age.gte": 21}] => WHERE (country = 'BR' AND age >= 18) OR (age >= 21)
```
* `parent`: mandatory parameter in child queries, `parent` determines which column links to parent query. If parent `pk` is composite, `parent` must be a list.

* `children`: a list of queries. It's mandatory that each child query decllares a `parent` argument. If filter conditions are included, they will be `AND`ed with `parent` to compose the query filter.
* `order_by`: indicates for which column(s) the result should be ordered.
