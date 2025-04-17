import pytest
from repositories.UsuarioRepositories import UserRepository
from models.Usuario import Usuario

@pytest.fixture
def popular_usuario(db_session):
    usuario = Usuario(nome="Usuário Teste", email="teste@teste.com", senha_hash="senha123")
    db_session.add(usuario)
    db_session.commit()
    return usuario

@pytest.fixture
def repo(db_session):
    return UserRepository(db_session)

def test_buscar_por_email(repo, popular_usuario):
    resultado = repo.buscar_por_email("teste@teste.com")
    assert resultado is not None
    assert resultado.email == "teste@teste.com"
    assert resultado.nome == "Usuário Teste"

def test_salvar_usuario(db_session):
    repo = UserRepository(db_session)
    novo_usuario = Usuario(nome="Novo Usuário", email="novo@teste.com", senha_hash="123456")
    resultado = repo.salvar(novo_usuario)

    assert resultado.id is not None
    assert resultado.email == "novo@teste.com"
    persistido = db_session.query(Usuario).filter_by(email="novo@teste.com").first()
    assert persistido is not None
    assert persistido.nome == "Novo Usuário"
