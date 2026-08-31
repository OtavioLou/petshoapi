from sqlalchemy import Column, Integer, String
from database import Base

class TutoresModel(Base):
    __tablename__ = "tutores"  # nome da tabela

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    nome = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        nullable=False
    )

    telefone = Column(
        String,
        nullable=False
    )

