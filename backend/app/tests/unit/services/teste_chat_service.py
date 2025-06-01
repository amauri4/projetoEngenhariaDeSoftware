import pytest
from unittest.mock import MagicMock, patch
from app.models.Usuario import Usuario
from app.services.UserService import UserService

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def service(mock_db):
    # Reset singleton para cada teste
    UserService._instance = None
    return UserService(mock_db)

def test_criar_usuario_sucesso(service):
    usuario_mock = Usuario(nome="Teste", email="teste@example.com", senha_hash="minhasenha")
    # Mocka buscar_por_email para não achar usuário existente
    service.user_repository.buscar_por_email = MagicMock(return_value=None)
    # Mocka salvar para retornar o usuário salvo
    service.user_repository.salvar = MagicMock(return_value=usuario_mock)

    with patch("app.services.UserService.gerar_hash_senha", return_value="hash_da_senha"):
        resultado = service.criar_usuario(usuario_mock)
    
    assert resultado == usuario_mock
    service.user_repository.buscar_por_email.assert_called_once_with("teste@example.com")
    service.user_repository.salvar.assert_called_once()
    
def test_criar_usuario_ja_existente(service):
    usuario_mock = Usuario(nome="Teste", email="teste@example.com", senha_hash="minhasenha")
    service.user_repository.buscar_por_email = MagicMock(return_value=usuario_mock)
    
    with pytest.raises(Exception) as excinfo:
        service.criar_usuario(usuario_mock)
    assert "Já existe um usuário com este e-mail." in str(excinfo.value)

def test_autenticar_usuario_sucesso(service):
    usuario_mock = Usuario(nome="Teste", email="teste@example.com", senha_hash="hash_correto")
    service.user_repository.buscar_por_email = MagicMock(return_value=usuario_mock)

    with patch("app.services.UserService.verificar_senha", return_value=True):
        resultado = service.autenticar_usuario("teste@example.com", "senha_teste")

    assert resultado == usuario_mock
    service.user_repository.buscar_por_email.assert_called_once_with("teste@example.com")

def test_autenticar_usuario_falha_email(service):
    service.user_repository.buscar_por_email = MagicMock(return_value=None)
    with pytest.raises(Exception) as excinfo:
        service.autenticar_usuario("invalido@example.com", "senha")
    assert "Credenciais inválidas." in str(excinfo.value)

def test_autenticar_usuario_falha_senha(service):
    usuario_mock = Usuario(nome="Teste", email="teste@example.com", senha_hash="hash_correto")
    service.user_repository.buscar_por_email = MagicMock(return_value=usuario_mock)
    with patch("app.services.UserService.verificar_senha", return_value=False):
        with pytest.raises(Exception) as excinfo:
            service.autenticar_usuario("teste@example.com", "senha_errada")
    assert "Credenciais inválidas." in str(excinfo.value)
