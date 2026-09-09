from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from sqlalchemy.sql import func

class CategoriaModel(Base):
    __tablename__ = "categoria"  # nome da tabela

    id_categoria = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    nome = Column(
        String,
        nullable=False,
        unique=True
    )

class UsuarioModel(Base):
    __tablename__ = "usuario"  # nome da tabela

    id_usuario = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    nome = Column(
        String,
        nullable=False,
        unique=True
    )

    email = Column(
        String,
        nullable=False,
        unique=True,

    )

    data_cadastro = Column(
        DateTime(timezone=True),
        server_default=func.now()
    
    )

    telefone = Column(
        String,
        nullable=False,
        unique=True,

    )

    tipo_usuario = Column(
        String,
        nullable=False,
        default="cliente" 
    )
    
class FreelancerModel(Base):
    __tablename__ = "freelancer"  # nome da tabela

    id_freelancer = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    especialidade = Column(
        String,
        nullable=True,
        
    )

    valor_hora = Column(
        Integer,
        nullable=True,
        
    )

    bio = Column(
        String,
        nullable=True,

    )



    habilidade = Column(
        String,
        nullable=False,
    )

    id_usuario = Column(
        Integer, 
        ForeignKey("usuario.id_usuario")
        )

    id_categoria = Column(
        Integer, 
        ForeignKey("categoria.id_categoria")
        )



