from database.base import engine, Base
from models.habito_base import HabitoBase
from models.categorias_habito import CategoriaHabito
from models.registro_diario import RegistroDiario
from database import session
from models.usuario import Usuario

# Usado para criar tabela no bd (*ALTERAR FUTURAMENTE, POIS NÃO INCLUI MUDANÇAS NAS ESTRUTURA DAS TABELAS -> usar alembic*)
def init_db():
    Base.metadata.create_all(bind=engine)

def test_db():
    db: session = next(session.get_db())  
    usuario_existente = db.query(Usuario).filter(Usuario.email == "joao@email.com").first()

    if usuario_existente:
        print(f"Usuário com o email {usuario_existente.email} já existe!")
    else:
        novo_usuario = Usuario(nome="João", email="joao@email.com", senha_hash="123")
        db.add(novo_usuario)
        db.commit()  
        db.refresh(novo_usuario)  #

        print(f"Usuário criado: {novo_usuario.nome} (ID: {novo_usuario.id})")

    db.close()  




if __name__ == "__main__":
    init_db()
    print("Banco de dados inicializado com sucesso!")
    test_db()
