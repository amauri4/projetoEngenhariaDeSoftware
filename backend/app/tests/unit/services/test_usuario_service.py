import pytest
from app.services.UsuarioService import UserService
from app.models.Usuario import Usuario
from app.utils.gerar_verificar_hash import gerar_hash_senha

@pytest.fixture
def user_service(db_session):
    return UserService(db_session)

@pytest.fixture
def usuario_existente(db_session):
    usuario = Usuario(
        nome="Usuário Existente",
        email="existente@teste.com",
        senha_hash=gerar_hash_senha("senha123")
    )
    db_session.add(usuario)
    db_session.commit()
    return usuario

def test_criar_usuario_sucesso(user_service, db_session):
    usuario = user_service.criar_usuario("Novo Usuário", "novo@teste.com", "minha_senha")

    assert usuario.id is not None
    assert usuario.email == "novo@teste.com"
    assert usuario.nome == "Novo Usuário"

    persistido = db_session.query(Usuario).filter_by(email="novo@teste.com").first()
    assert persistido is not None
    assert persistido.senha_hash != "minha_senha"  

def test_criar_usuario_email_existente(user_service, usuario_existente):
    with pytest.raises(Exception) as exc:
        user_service.criar_usuario("Outro", "existente@teste.com", "outra_senha")

    assert "Já existe um usuário com este e-mail." in str(exc.value)

def test_autenticar_usuario_sucesso(user_service, usuario_existente):
    usuario = user_service.autenticar_usuario("existente@teste.com", "senha123")
    assert usuario is not None
    assert usuario.email == "existente@teste.com"

def test_autenticar_usuario_senha_errada(user_service, usuario_existente):
    with pytest.raises(Exception) as exc:
        user_service.autenticar_usuario("existente@teste.com", "senhaErrada")
    assert "Credenciais inválidas." in str(exc.value)

def test_autenticar_usuario_inexistente(user_service):
    with pytest.raises(Exception) as exc:
        user_service.autenticar_usuario("naoexiste@teste.com", "qualquercoisa")
    assert "Credenciais inválidas." in str(exc.value)
