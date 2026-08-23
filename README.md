Projeto feito por: Otavio Augusto, Caua Rodriguez e Matheus Elias



API desenvolvida com FastAPI para gerenciamento de um PetShop. O sistema controla o cadastro de tutores (donos dos animais) e dos pets vinculados a cada tutor, permitindo consultar e futuramente gerenciar essas informações de forma simples via endpoints HTTP.

### Tabela 1 — Tutores

| Campo | Tipo | Descrição |
|---|---|---|
| id | int | Identificador único do tutor |
| nome | string | Nome do tutor |
| telefone | string | Telefone do tutor |
| email | string | E-mail do tutor |

### Tabela 2 — Pets

| Campo | Tipo | Descrição |
|---|---|---|
| id | int | Identificador único do pet |
| nome | string | Nome do pet |
| raça | string | Raça do pet |
| tutorid | int | Identificador do tutor responsável |

## Contrato das Rotas HTTP

As rotas abaixo representam as operações CRUD da entidade `Tutores`.

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/tutores` | Lista todos os tutores |
| GET | `/tutores/{tutor_id}` | Busca um tutor pelo ID |
| POST | `/tutores` | Cadastra um novo tutor |
| DELETE | `/tutores/{tutor_id}` | Remove um tutor pelo ID |