from fastapi import FastAPI, HTTPException, status

from pydantic import BaseModel

from database import Base, engine

from routers import tutores

Base.metadata.create_all(bind=engine)

# titulo

app = FastAPI(
    title="Petshop",
    description="api para cadastro de tutores e animais"
)

# incluir rotas

app.include_router(tutores.router)

# rota raiz

@app.get("/")
def home():
    return {"mensagem": "api com sucesso"}