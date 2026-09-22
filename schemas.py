from pydantic import BaseModel, ConfigDict
from datetime import datetime


#schema de entrada de dados (post/requisição)
class CategoriaSchema(BaseModel):
    nome: str

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    telefone: str
    tipo_usuario: str

class FreelancerSchema(BaseModel):
    
    valor_hora: int
    bio: str
    habilidade: str
    id_usuario: int
    id_categoria: int

    

    

#Schema saida de dados (aparecer o ID)

class CategoriaResponseSchema(CategoriaSchema):
    id_categoria: int
    model_config = ConfigDict(from_attributes=True)


class UsuarioResponseSchema(UsuarioSchema):
    id_usuario: int
    data_cadastro: datetime
    model_config = ConfigDict(from_attributes=True)


class FreelancerResponseSchema(FreelancerSchema):
    id_freelancer: int
    model_config = ConfigDict(from_attributes=True)





# Permitir que o Pydantic leia objetos do banco de dados 
model_config = ConfigDict(from_attributes=True)

#configdict foi usado pq o pydantic atualizado pede pra usar.