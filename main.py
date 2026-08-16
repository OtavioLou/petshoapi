from fastapi import FastAPI
app = FastAPI(tittle= "petshop")

tutores = [
    {"id": 1, "nome": "Otavio", "telefone": "11 91234-5678", "email": "otavio@email.com"},
    {"id": 2, "nome": "Caua", "telefone": "11 99876-5432", "email": "Caua@email.com"},
    {"id": 3, "nome": "Matheus", "telefone": "11 98765-1234", "email": "Matheus@email.com"},
    {"id": 4, "nome": "Camila", "telefone": "11 97654-3210", "email": "camila@email.com"},
    {"id": 5, "nome": "Rafael", "telefone": "11 96543-2109", "email": "rafael@email.com"},
]

@app.get("/")


def home():

    return {"mensagem": "api rodando com sucesso"}

@app.get("/tutores")
def listar_tutores():
    return tutores

