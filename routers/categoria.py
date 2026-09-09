from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from database import get_db
from models import CategoriaModel
from schemas import CategoriaSchema, CategoriaResponseSchema


#instancia de apirouter configurada com o prefixo e tag de entidade Cria um "mini conjunto" de rotas. Em vez de colocar todas as rotas no main.py, você pode separar:
router = APIRouter(
    prefix="/categoria",
    tags=["categoria"]
)

#listar todos com suporte filtros por query parameter

@router.get("/", response_model=list[CategoriaResponseSchema], status_code=status.HTTP_200_OK)

def listar_categoria(nome: str = None, db: Session = Depends(get_db)):

    query = db.query(CategoriaModel)

    if nome:

        query = query.filter(CategoriaModel.nome.contains(nome))

    return query.all()

#busca por id
@router.get("/{categoria_id}", response_model=CategoriaResponseSchema, status_code=status.HTTP_200_OK)
def buscar_categoria_id(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(CategoriaModel).filter(CategoriaModel.id_categoria == categoria_id).first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="categoria não encontrado"
        )

    return categoria

#create
@router.post("/", response_model=CategoriaResponseSchema, status_code=status.HTTP_201_CREATED)
def criar_categoria(dados_categoria: CategoriaSchema, db: Session = Depends(get_db)):

    novo_categoria = CategoriaModel(**dados_categoria.model_dump())

    db.add(novo_categoria)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe uma categoria com esse nome."
        )

    db.refresh(novo_categoria)
    return novo_categoria

#delete

@router.delete("/{categoria_id}", status_code=status.HTTP_200_OK)
def deletar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(CategoriaModel).filter(CategoriaModel.id_categoria == categoria_id).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="categoria não encontrado"
        )

    db.delete(categoria)
    db.commit()

    return {"mensagem": f"categoria {categoria_id} removido com sucesso"}