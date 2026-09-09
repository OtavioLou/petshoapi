from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from database import get_db
from models import UsuarioModel
from schemas import UsuarioResponseSchema, UsuarioSchema


#instancia de apirouter configurada com o prefixo e tag de entidade Cria um "mini conjunto" de rotas. Em vez de colocar todas as rotas no main.py, você pode separar:
router = APIRouter(
    prefix="/usuario",
    tags=["usuario"]
)

#listar todos com suporte filtros por query parameter

@router.get("/", response_model=list[UsuarioResponseSchema], status_code=status.HTTP_200_OK)

def listar_usuario(nome: str = None, db: Session = Depends(get_db)):

    query = db.query(UsuarioModel)

    if nome:

        query = query.filter(UsuarioModel.nome.contains(nome))

    return query.all()

#busca por id
@router.get("/{usuario_id}", response_model=UsuarioResponseSchema, status_code=status.HTTP_200_OK)
def buscar_usuario_id(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id_usuario == usuario_id).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="usuario não encontrado"
        )

    return usuario

#create
@router.post("/", response_model=UsuarioResponseSchema, status_code=status.HTTP_201_CREATED)
def criar_usuario(dados_usuario: UsuarioSchema, db: Session = Depends(get_db)):

    novo_usuario = UsuarioModel(**dados_usuario.model_dump())

    db.add(novo_usuario)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe uma usuario com esse nome."
        )

    db.refresh(novo_usuario)
    return novo_usuario

#delete

@router.delete("/{usuario_id}", status_code=status.HTTP_200_OK)
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id_usuario == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="usuario não encontrado"
        )

    db.delete(usuario)
    db.commit()

    return {"mensagem": f"usuario {usuario_id} removido com sucesso"}