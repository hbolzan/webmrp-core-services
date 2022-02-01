resources_index = {
    "fornecedores": {
        "source": "fornecedores.select.sql",
        "singular": "fornecedor",
        "pk": "id",
        "query_pk": "frn.id",
    },
    "paises": {"source": "nfebase.paises", "singular": "país", "pk": "codigo"},
    "municipios": {"source": "nfebase.ibge_municipios_reduzida", "singular": "municipio", "pk": "municipiocodigo"},
}
