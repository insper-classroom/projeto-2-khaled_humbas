Rotas API:

url_base = 100.48.20.219
# GET /imovel -> retorna todos os imóveis
# GET /imovel/<int:id> -> retorna imóvel específico com algum id inteiro
# POST /imovel -> coloca um novo imóvel ao banco de dados
## Corpo da Requisição (JSON)

### Campos Obrigatórios
| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `logradouro` | string | Nome da rua/avenida | "Paulista" |
| `tipo_logradouro` | string | Tipo do logradouro | "Avenida" |
| `bairro` | string | Nome do bairro | "Bela Vista" |
| `cidade` | string | Nome da cidade | "São Paulo" |
| `cep` | string | CEP no formato 00000-000 | "01310-100" |
| `tipo` | string | Tipo do imóvel | "Apartamento" |
| `valor` | float | Valor do imóvel | 750000.00 |
| `data_aquisicao` | string | Data no formato YYYY-MM-DD | "2024-03-10" |

# PUT /imovel/<int:id> -> Muda os dados de um imóvel com id inteiro

# POST /imovel -> coloca um novo imóvel ao banco de dados
## Corpo da Requisição (JSON)

### Campos Obrigatórios
| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `logradouro` | string | Nome da rua/avenida | "Paulista" |
| `tipo_logradouro` | string | Tipo do logradouro | "Avenida" |
| `bairro` | string | Nome do bairro | "Bela Vista" |
| `cidade` | string | Nome da cidade | "São Paulo" |
| `cep` | string | CEP no formato 00000-000 | "01310-100" |
| `tipo` | string | Tipo do imóvel | "Apartamento" |
| `valor` | float | Valor do imóvel | 750000.00 |
| `data_aquisicao` | string | Data no formato YYYY-MM-DD | "2024-03-10" |

# DELETE /imovel/<int:id> -> remove o imóvel com id inteiro

# GET /imovel/tipo/<string:tipo> -> lista todos os imóveis com um tipo (string) específico 

# GET /imovel/cidade/<string:cidade> -> lista todos os imóveis com cidade (string) específico