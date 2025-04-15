from .base import SessionLocal

def get_db(): #Função para obter uma sessão do banco de dados
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
