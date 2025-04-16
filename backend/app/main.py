from database.base import engine, Base
from models.HabitoBase import HabitoBase
from models.CategoriasHabito import CategoriaHabito
from models.RegistroDiario import RegistroDiario
from database import session
from models.Usuario import Usuario
from datetime import datetime
from repositories.UserRepositories import UserRepository

# Usado para criar tabela no bd (*ALTERAR FUTURAMENTE, POIS NÃO INCLUI MUDANÇAS NAS ESTRUTURA DAS TABELAS -> usar alembic*)
def init_db():
    Base.metadata.create_all(bind=engine)

def test_db():
    db: session = next(session.get_db())      
    usuario_existente = db.query(Usuario).filter(Usuario.email == "joao@email.com").first()

    if usuario_existente:
        print(f"Usuário com o email {usuario_existente.email} já existe!")
        novo_usuario = usuario_existente
    else:
        novo_usuario = Usuario(nome="João", email="joao@email.com", senha_hash="123")
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        print(f"Usuário criado: {novo_usuario.nome} (ID: {novo_usuario.id})")

    categoria_existente = db.query(CategoriaHabito).filter(CategoriaHabito.nome == "Saúde").first()

    if categoria_existente:
        print(f"Categoria de hábito {categoria_existente.nome} já existe!")
    else:
        nova_categoria = CategoriaHabito(nome="Saúde")
        db.add(nova_categoria)
        db.commit()
        db.refresh(nova_categoria)
        print(f"Categoria de hábito criada: {nova_categoria.nome} (ID: {nova_categoria.id})")

    categoria = db.query(CategoriaHabito).filter(CategoriaHabito.nome == "Saúde").first()
    if categoria:
        novo_habito = HabitoBase(nome="Beber água", descricao="Beber 2L de água por dia", categoria_id=categoria.id, usuario_id=novo_usuario.id)
        db.add(novo_habito)
        db.commit()
        db.refresh(novo_habito)
        print(f"Hábito criado: {novo_habito.nome} (ID: {novo_habito.id})")
    else:
        print("Categoria de hábito não encontrada.")

    habito = db.query(HabitoBase).filter(HabitoBase.nome == "Beber água").first()
    if habito:
        novo_registro = RegistroDiario(habito_id=habito.id, data=datetime.now(), concluido=True)
        db.add(novo_registro)
        db.commit()
        db.refresh(novo_registro)
        print(f"Registro diário criado: Hábito: {novo_registro.habito_id} - Completado: {novo_registro.concluido} (ID: {novo_registro.id})")
    else:
        print("Hábito não encontrado para registro diário.")
    db.close()

def test_repo():
    db: session = next(session.get_db())
    usuario_existente = db.query(Usuario).filter(Usuario.email == "joao@email.com").first()
    get_user = UserRepository()
    search_by_email = get_user.find_by_email('joao@email.com')
    assert search_by_email.email == usuario_existente.email
    user = Usuario(email="novo@email.com", nome="Novo Usuário", senha_hash='1234')

    saved_user = get_user.save(user)

    assert saved_user.email == "novo@email.com"
    assert saved_user.nome == "Novo Usuário"
    usuario_salvo = db.query(Usuario).filter(Usuario.email == "novo@email.com").first()
    assert usuario_salvo is not None
    assert usuario_salvo.email == "novo@email.com"
    assert usuario_salvo.nome == "Novo Usuário"

    db.close()


if __name__ == "__main__":
    init_db()
    print("Banco de dados inicializado com sucesso!")
    test_db()
    test_repo()
