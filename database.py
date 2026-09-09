from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Definindo conexão com o SQLite
DATABASE_URL = "sqlite:///./freejob.db"

# Criando o motor do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Irá gerar sessões de leitura e escrita no banco
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Classe pai da qual todos os modelos de tabela herdam
Base = declarative_base()

# Maneira de iniciar e encerrar o banco de dados de forma segura
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

