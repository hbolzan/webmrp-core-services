select
  frn.*,
  paises.nome as pais_nome,
  mun.municipionome as municipio_nome
from
  view_nfe_fornecedores frn
left join
  nfebase.paises paises
  on paises.codigo = frn.pais
left join
  nfebase.ibge_municipios_reduzida mun
  on mun.municipiocodigo = frn.ibge_municipio
{where}
{order_by}
