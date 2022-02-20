from .resources.fornecedores import resource
resources_index = {
    "fornecedores": resource,

    "paises": {
        "source": "nfebase.paises",
        "singular": "país",
        "pk": "codigo"
    },

    "municipios": {
        "source": "nfebase.ibge_municipios_reduzida",
        "singular": "municipio",
        "pk": "municipiocodigo"
    },
}
