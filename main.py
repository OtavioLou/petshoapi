from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

from database import Base, engine
from routers import categoria, usuario, freelancer
from models import CategoriaModel, UsuarioModel, FreelancerModel


# Criar as tabelas do banco de dados
Base.metadata.create_all(bind=engine)


# Configuracao da API
app = FastAPI(
    title="Freejob",
    description="API para cadastro de freelancers"
)


# Tratamento de erros de registros duplicados
@app.exception_handler(IntegrityError)
async def integrity_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=409,
        content={
            "detail": "Registro duplicado ou em conflito com dados existentes."
        }
    )


# Tratamento de erros de validacao
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    erros = []

    for erro in exc.errors():
        campo = str(erro["loc"][-1])
        tipo = erro["type"]

        if tipo == "missing":
            mensagem = f"O campo '{campo}' e obrigatorio."

        elif tipo == "string_too_short":
            mensagem = f"O campo '{campo}' possui poucos caracteres."

        elif tipo == "string_too_long":
            mensagem = f"O campo '{campo}' ultrapassou o limite de caracteres."

        elif tipo == "greater_than":
            mensagem = (
                f"O campo '{campo}' deve ser maior que "
                "o valor minimo permitido."
            )

        elif tipo == "value_error" and campo == "email":
            mensagem = "Informe um endereco de e-mail valido."

        elif tipo == "value_error" and campo == "telefone":
            mensagem = erro["msg"].replace("Value error, ", "")

        elif tipo == "literal_error":
            mensagem = (
                f"O valor informado para o campo '{campo}' "
                "nao e permitido."
            )

        else:
            mensagem = (
                f"O valor informado para o campo '{campo}' e invalido."
            )

        erros.append({
            "campo": campo,
            "mensagem": mensagem
        })

    return JSONResponse(
        status_code=422,
        content={
            "detail": "Os dados informados sao invalidos.",
            "erros": erros
        }
    )


# Incluir as rotas
app.include_router(categoria.router)
app.include_router(usuario.router)
app.include_router(freelancer.router)


# Rota principal
@app.get("/")
def home():
    return {"mensagem": "api com sucesso"}