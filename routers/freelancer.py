from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import FreelancerModel, UsuarioModel, CategoriaModel
from schemas import FreelancerSchema, FreelancerResponseSchema

router = APIRouter(
    prefix="/freelancer",
    tags=["Freelancer"]
)


@router.get("/", response_model=list[FreelancerResponseSchema])
def listar_freelancers(habilidade: str | None = None, db: Session = Depends(get_db)):
    query = db.query(FreelancerModel)

    if habilidade:
        query = query.filter(FreelancerModel.habilidade.ilike(f"%{habilidade}%"))

    return query.all()


@router.get("/{freelancer_id}", response_model=FreelancerResponseSchema)
def buscar_freelancer(freelancer_id: int, db: Session = Depends(get_db)):
    freelancer = db.query(FreelancerModel).filter(
        FreelancerModel.id_freelancer == freelancer_id
    ).first()

    if not freelancer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Freelancer não encontrado"
        )

    return freelancer


@router.post("/", response_model=FreelancerResponseSchema, status_code=status.HTTP_201_CREATED)
def criar_freelancer(freelancer: FreelancerSchema, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.id_usuario == freelancer.id_usuario
    ).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário informado não existe"
        )

    categoria = db.query(CategoriaModel).filter(
        CategoriaModel.id_categoria == freelancer.id_categoria
    ).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria informada não existe"
        )

    novo_freelancer = FreelancerModel(**freelancer.model_dump())
    db.add(novo_freelancer)
    db.commit()
    db.refresh(novo_freelancer)
    return novo_freelancer


@router.put("/{freelancer_id}", response_model=FreelancerResponseSchema)
def atualizar_freelancer(freelancer_id: int, freelancer: FreelancerSchema, db: Session = Depends(get_db)):
    freelancer_existente = db.query(FreelancerModel).filter(
        FreelancerModel.id_freelancer == freelancer_id
    ).first()

    if not freelancer_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Freelancer não encontrado"
        )

    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.id_usuario == freelancer.id_usuario
    ).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário informado não existe"
        )

    categoria = db.query(CategoriaModel).filter(
        CategoriaModel.id_categoria == freelancer.id_categoria
    ).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria informada não existe"
        )

    for campo, valor in freelancer.model_dump().items():
        setattr(freelancer_existente, campo, valor)

    db.commit()
    db.refresh(freelancer_existente)
    return freelancer_existente


@router.delete("/{freelancer_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_freelancer(freelancer_id: int, db: Session = Depends(get_db)):
    freelancer = db.query(FreelancerModel).filter(
        FreelancerModel.id_freelancer == freelancer_id
    ).first()

    if not freelancer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Freelancer não encontrado"
        )

    db.delete(freelancer)
    db.commit()
    return None