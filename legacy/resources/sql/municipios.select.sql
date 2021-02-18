select
  codigo, nome, uf
from (
  select
    mun.municipiocodigo as codigo, mun.municipionome as nome, ufs.ufsigla as uf
  from
    nfebase.ibge_municipios_reduzida mun
  join
    nfebase.ibge_ufs ufs
    on ufs.ufcodigo = mun.ufcodigo
  ) q1
{where}
{order_by}
