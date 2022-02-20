from ..logic.misc import remove_separators

resource = {
        "source": "fornecedores.select.sql",
        "singular": "fornecedor",
        "pk": "id",
        "query_pk": "frn.id",
        "exclude_from_upsert": ["pais_nome", "municipio_nome"],
        "before_post": {
            "cnpj": remove_separators,
            "cpf": remove_separators,
        },
    }
