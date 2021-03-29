select
  addr.id, addr.participante, addr.tipo_de_endereco,
  addr.pais, paises.nome as pais_nome,
  addr.cep, addr.uf,
  addr.ibge_municipio, mun.municipionome as municipio_nome,
  addr.tipo_de_logradouro, addr.nome_do_logradouro,
  addr.numero, addr.complemento, addr.bairro, addr.rota
from
  nfe_participantes_enderecos addr
left join
  nfebase.paises paises
  on paises.codigo = addr.pais
left join
  nfebase.ibge_municipios_reduzida mun
  on mun.municipiocodigo = addr.ibge_municipio
{where}
{order_by}
