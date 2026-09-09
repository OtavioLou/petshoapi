from fastapi import FastAPI, HTTPException, status

from pydantic import BaseModel

from database import Base, engine

from routers import categoria, usuario, freelancer

Base.metadata.create_all(bind=engine)

# titulo

app = FastAPI(
    title="Freejob",
    description="api para cadastro de freelancers"
)

# incluir rotas

app.include_router(categoria.router)
app.include_router(usuario.router)
app.include_router(freelancer.router)
# rota raiz

@app.get("/")
def home():
    return {"mensagem": "api com sucesso"}
    