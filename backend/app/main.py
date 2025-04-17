from database.base import engine, Base

# Usado para criar tabela no bd (*ALTERAR FUTURAMENTE, POIS NÃO INCLUI MUDANÇAS NAS ESTRUTURA DAS TABELAS -> usar alembic*)
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Banco de dados inicializado com sucesso!")
