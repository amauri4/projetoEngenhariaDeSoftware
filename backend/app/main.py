from database.base import engine, Base
from models.HabitoBase import HabitoBase
from models.CategoriasHabito import CategoriaHabito
from models.RegistroDiario import RegistroDiario
from database import session
from models.Usuario import Usuario
from datetime import datetime
from repositories.UsuarioRepositories import UserRepository

# Usado para criar tabela no bd (*ALTERAR FUTURAMENTE, POIS NÃO INCLUI MUDANÇAS NAS ESTRUTURA DAS TABELAS -> usar alembic*)
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Banco de dados inicializado com sucesso!")
