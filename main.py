from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="petshop")


# =========================
# CONTRATOS DE REQUISIÇÃO
# =========================

class TutorSchema(BaseModel):
    nome: str
    telefone: str
    email: str


class PetSchema(BaseModel):
    nome: str
    raça: str
    tutorid: int


# =========================
# DADOS
# =========================

tutores = [
    {"id": 1, "nome": "Otavio", "telefone": "11 91234-5678", "email": "otavio@email.com"},
    {"id": 2, "nome": "Caua", "telefone": "11 99876-5432", "email": "Caua@email.com"},
    {"id": 3, "nome": "Matheus", "telefone": "11 98765-1234", "email": "Matheus@email.com"},
    {"id": 4, "nome": "Camila", "telefone": "11 97654-3210", "email": "camila@email.com"},
    {"id": 5, "nome": "Rafael", "telefone": "11 96543-2109", "email": "rafael@email.com"},
]

pets = [
    {"id": 1, "nome": "Duke", "raça": "Vira-Lata", "tutorid": 1},
    {"id": 2, "nome": "Totó", "raça": "Labrador", "tutorid": 2},
    {"id": 3, "nome": "Princesinha", "raça": "Pastor-Alemão", "tutorid": 3},
    {"id": 4, "nome": "Chakal", "raça": "Bulldog", "tutorid": 4},
    {"id": 5, "nome": "York", "raça": "Yorkshire", "tutorid": 5},
]


# =========================
# ROTA INICIAL
# =========================

@app.get("/")
def home():
    return {"mensagem": "API rodando com sucesso"}


# =========================
# LISTAR TODOS OS TUTORES
# =========================

@app.get("/tutores", status_code=status.HTTP_200_OK)
def listar_tutores(nome: str | None = None):

    if nome:
        resultado = [
            tutor for tutor in tutores
            if nome.lower() in tutor["nome"].lower()
        ]

        return resultado

    return tutores


# =========================
# BUSCAR TUTOR POR ID
# =========================

@app.get("/tutores/{tutor_id}", status_code=status.HTTP_200_OK)
def buscar_tutor_id(tutor_id: int):

    for tutor in tutores:
        if tutor["id"] == tutor_id:
            return tutor

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Tutor não encontrado"
    )


# =========================
# CADASTRAR NOVO TUTOR
# =========================

@app.post("/tutores", status_code=status.HTTP_201_CREATED)
def criar_tutor(dados_tutor: TutorSchema):

    novo_id = len(tutores) + 1

    novo_registro = {
        "id": novo_id,
        **dados_tutor.model_dump()
    }

    tutores.append(novo_registro)

    return novo_registro


# =========================
# REMOVER TUTOR POR ID
# =========================

@app.delete("/tutores/{tutor_id}", status_code=status.HTTP_200_OK)
def deletar_tutor(tutor_id: int):

    for index, tutor in enumerate(tutores):

        if tutor["id"] == tutor_id:
            tutores.pop(index)

            return {
                "mensagem": f"Tutor {tutor_id} removido com sucesso"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Tutor não encontrado"
    )