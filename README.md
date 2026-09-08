Projeto feito por: Otavio Augusto, Caua Rodriguez e Matheus Elias

API desenvolvida com FastAPI para gerenciamento do **Freejob**, uma plataforma de marketplace de freelancers voltada para o setor de tecnologia/TI. O sistema controla o cadastro de categorias, usuários (clientes e freelancers) e dos perfis de freelancer vinculados a cada usuário, permitindo consultar, cadastrar e remover essas informações via endpoints HTTP.

### Tabela 1 — Categoria

| Campo | Tipo | Descrição |
|---|---|---|
| id_categoria | int | Identificador único da categoria |
| nome | string | Nome da categoria (ex: Design, Desenvolvimento) |

### Tabela 2 — Usuario

| Campo | Tipo | Descrição |
|---|---|---|
| id_usuario | int | Identificador único do usuário |
| nome | string | Nome do usuário |
| email | string | E-mail do usuário |
| telefone | string | Telefone do usuário |
| tipo_usuario | string | Tipo do usuário (ex: Cliente, Freelancer) — padrão "cliente" |
| data_cadastro | datetime | Data em que o usuário foi cadastrado |

### Tabela 3 — Freelancer

| Campo | Tipo | Descrição |
|---|---|---|
| id_freelancer | int | Identificador único do perfil de freelancer |
| especialidade | string | Especialidade do freelancer |
| valor_hora | int | Valor cobrado por hora de trabalho |
| bio | string | Descrição/biografia do freelancer |
| habilidade | string | Habilidades do freelancer |
| id_usuario | int | Identificador do usuário vinculado a este perfil |
| id_categoria | int | Identificador da categoria vinculada a este perfil |

## Contrato das Rotas HTTP

### Usuario

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/usuario/` | Lista todos os usuários (aceita filtro `?nome=`) |
| GET | `/usuario/{usuario_id}` | Busca um usuário pelo ID |
| POST | `/usuario/` | Cadastra um novo usuário |
| DELETE | `/usuario/{usuario_id}` | Remove um usuário pelo ID |

### Freelancer

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/freelancer/` | Lista todos os freelancers (aceita filtro `?habilidade=`) |
| GET | `/freelancer/{freelancer_id}` | Busca um freelancer pelo ID |
| POST | `/freelancer/` | Cadastra um novo perfil de freelancer (requer `id_usuario` e `id_categoria` já existentes) |
| DELETE | `/freelancer/{freelancer_id}` | Remove um freelancer pelo ID |

### Categoria

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/categoria/` | Lista todas as categorias |
| GET | `/categoria/{categoria_id}` | Busca uma categoria pelo ID |
| POST | `/categoria/` | Cadastra uma nova categoria |
| DELETE | `/categoria/{categoria_id}` | Remove uma categoria pelo ID |