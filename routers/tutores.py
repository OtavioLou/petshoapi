from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from database import get_db
from models import TutoresModel
from schemas import TutorSchema, TutorResponseSchema


#instancia de apirouter configurada com o prefixo e tag de entidade Cria um "mini conjunto" de rotas. Em vez de colocar todas as rotas no main.py, você pode separar:
router = APIRouter(
    prefix="/tutores",
    tags=["Tutores"]
)

#listar todos com suporte filtros por query parameter

@router.get("/", response_model=list[TutorResponseSchema], status_code=status.HTTP_200_OK)

def listar_tutores(nome: str = None, db: Session = Depends(get_db)):

    query = db.query(TutoresModel)

    if nome:

        query = query.filter(TutoresModel.nome.contains(nome))

    return query.all()

#busca por id
@router.get("/{tutor_id}", response_model=TutorResponseSchema, status_code=status.HTTP_200_OK)
def buscar_tutor_id(tutor_id: int, db: Session = Depends(get_db)):
    tutor = db.query(TutoresModel).filter(TutoresModel.id == tutor_id).first()

    if not tutor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="tutor não encontrado"
        )

    return tutor

#create
@router.post("/", response_model=TutorResponseSchema, status_code=status.HTTP_201_CREATED)
def criar_tutor(dados_tutor: TutorSchema, db: Session = Depends(get_db)):

    novo_tutor = TutoresModel(**dados_tutor.model_dump())

    db.add(novo_tutor) #sem isso o novo tutor não é colocado na sessão para ser salvo.
    db.commit()

    db.refresh(novo_tutor)

    return novo_tutor

#delete

@router.delete("/{tutor_id}", status_code=status.HTTP_200_OK)
def deletar_tutor(tutor_id: int, db: Session = Depends(get_db)):
    tutor = db.query(TutoresModel).filter(TutoresModel.id == tutor_id).first()

    if not tutor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="tutor não encontrado"
        )

    db.delete(tutor)
    db.commit()

    return {"mensagem": f"tutor {tutor_id} removido com sucesso"}