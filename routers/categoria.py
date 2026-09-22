from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import CategoriaModel
from schemas import CategoriaSchema, CategoriaResponseSchema

router = APIRouter(
    prefix="/categoria",
    tags=["Categoria"]
)


@router.get("/", response_model=list[CategoriaResponseSchema])
def listar_categorias(db: Session = Depends(get_db)):
    categorias = db.query(CategoriaModel).all()
    return categorias


@router.get("/{categoria_id}", response_model=CategoriaResponseSchema)
def buscar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(CategoriaModel).filter(
        CategoriaModel.id_categoria == categoria_id
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada"
        )

    return categoria


@router.post("/", response_model=CategoriaResponseSchema, status_code=status.HTTP_201_CREATED)
def criar_categoria(categoria: CategoriaSchema, db: Session = Depends(get_db)):
    nova_categoria = CategoriaModel(**categoria.model_dump())
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    return nova_categoria


@router.put("/{categoria_id}", response_model=CategoriaResponseSchema)
def atualizar_categoria(categoria_id: int, categoria: CategoriaSchema, db: Session = Depends(get_db)):
    categoria_existente = db.query(CategoriaModel).filter(
        CategoriaModel.id_categoria == categoria_id
    ).first()

    if not categoria_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada"
        )

    for campo, valor in categoria.model_dump().items():
        setattr(categoria_existente, campo, valor)

    db.commit()
    db.refresh(categoria_existente)
    return categoria_existente


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(CategoriaModel).filter(
        CategoriaModel.id_categoria == categoria_id
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada"
        )

    db.delete(categoria)
    db.commit()
    return None