from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import UsuarioModel
from schemas import UsuarioSchema, UsuarioResponseSchema

router = APIRouter(
    prefix="/usuario",
    tags=["Usuario"]
)


@router.get("/", response_model=list[UsuarioResponseSchema])
def listar_usuarios(nome: str | None = None, db: Session = Depends(get_db)):
    query = db.query(UsuarioModel)

    if nome:
        query = query.filter(UsuarioModel.nome.ilike(f"%{nome}%"))

    return query.all()


@router.get("/{usuario_id}", response_model=UsuarioResponseSchema)
def buscar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.id_usuario == usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    return usuario


@router.post("/", response_model=UsuarioResponseSchema, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    novo_usuario = UsuarioModel(**usuario.model_dump())
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


@router.put("/{usuario_id}", response_model=UsuarioResponseSchema)
def atualizar_usuario(usuario_id: int, usuario: UsuarioSchema, db: Session = Depends(get_db)):
    usuario_existente = db.query(UsuarioModel).filter(
        UsuarioModel.id_usuario == usuario_id
    ).first()

    if not usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    for campo, valor in usuario.model_dump().items():
        setattr(usuario_existente, campo, valor)

    db.commit()
    db.refresh(usuario_existente)
    return usuario_existente


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.id_usuario == usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    db.delete(usuario)
    db.commit()
    return None