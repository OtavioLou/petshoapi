from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from database import get_db
from models import FreelancerModel
from schemas import FreelancerResponseSchema, FreelancerSchema


#instancia de apirouter configurada com o prefixo e tag de entidade Cria um "mini conjunto" de rotas. Em vez de colocar todas as rotas no main.py, você pode separar:
router = APIRouter(
    prefix="/freelancer",
    tags=["freelancer"]
)

#listar todos com suporte filtros por query parameter

@router.get("/", response_model=list[FreelancerResponseSchema], status_code=status.HTTP_200_OK)

def listar_freelancer(habilidade: str = None, db: Session = Depends(get_db)):

    query = db.query(FreelancerModel)

    if habilidade:

        query = query.filter(FreelancerModel.habilidade.contains(habilidade))

    return query.all()

#busca por id
@router.get("/{freelancer_id}", response_model=FreelancerResponseSchema, status_code=status.HTTP_200_OK)
def buscar_freelancer_id(freelancer_id: int, db: Session = Depends(get_db)):
    freelancer = db.query(FreelancerModel).filter(FreelancerModel.id_freelancer == freelancer_id).first()

    if not freelancer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="freelancer não encontrado"
        )

    return freelancer

#create
@router.post("/", response_model=FreelancerResponseSchema, status_code=status.HTTP_201_CREATED)
def criar_freelancer(dados_freelancer: FreelancerSchema, db: Session = Depends(get_db)):

    novo_freelancer = FreelancerModel(**dados_freelancer.model_dump())

    db.add(novo_freelancer)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="erro ao cadastrar freelancer."
        )

    db.refresh(novo_freelancer)
    return novo_freelancer

#delete

@router.delete("/{freelancer_id}", status_code=status.HTTP_200_OK)
def deletar_freelancer(freelancer_id: int, db: Session = Depends(get_db)):
    freelancer = db.query(FreelancerModel).filter(FreelancerModel.id_freelancer == freelancer_id).first()
    if not freelancer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="freelancer não encontrado"
        )

    db.delete(freelancer)
    db.commit()

    return {"mensagem": f"freelancer {freelancer_id} removido com sucesso"}