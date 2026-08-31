from pydantic import BaseModel, ConfigDict


#schema de entrada de dados (post/requisição)
class TutorSchema(BaseModel):
    nome: str
    telefone: str
    email: str

#Schema saida de dados (aparecer o ID)

class TutorResponseSchema(TutorSchema):
    id: int


# Permitir que o Pydantic leia objetos do banco de dados 
model_config = ConfigDict(from_attributes=True)

#configdict foi usado pq o pydantic atualizado pede pra usar.