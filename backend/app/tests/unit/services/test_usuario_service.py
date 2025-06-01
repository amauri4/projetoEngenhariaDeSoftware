import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import SQLAlchemyError
from app.models.Usuario import Usuario
from app.repositories.UserRepository import UserRepository

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def user_repo(mock_db):
    return UserRepository(mock_db)

def test_buscar_por_email_sucesso(user_repo, mock_db):
    user = Usuario(id=1, email="teste@example.com")
    mock_db.query().filter_by().first.return_value = user

    resultado = user_repo.buscar_por_email("teste@example.com")
    assert resultado == user
    mock_db.query.assert_called_once_with(Usuario)

def test_buscar_por_email_erro(user_repo, mock_db):
    mock_db.query.side_effect = SQLAlchemyError("Erro no DB")
    with pytest.raises(Exception) as excinfo:
        user_repo.buscar_por_email("teste@example.com")
    assert "Erro ao buscar usuário por e-mail" in str(excinfo.value)
    mock_db.rollback.assert_called_once()

def test_buscar_por_id_sucesso(user_repo, mock_db):
    user = Usuario(id=1, email="teste@example.com")
    mock_db.query().filter_by().first.return_value = user

    resultado = user_repo.buscar_por_id(1)
    assert resultado == user
    mock_db.query.assert_called_once_with(Usuario)

def test_salvar_sucesso(user_repo, mock_db):
    user = Usuario(id=1, email="teste@example.com")

    resultado = user_repo.salvar(user)
    assert resultado == user
    mock_db.add.assert_called_once_with(user)
    mock_db.commit.assert_called_once()

def test_salvar_erro(user_repo, mock_db):
    user = Usuario(id=1, email="teste@example.com")
    mock_db.add.side_effect = SQLAlchemyError("Erro ao salvar")

    with pytest.raises(Exception) as excinfo:
        user_repo.salvar(user)
    assert "Erro ao salvar usuário" in str(excinfo.value)
    mock_db.rollback.assert_called_once()

def test_atualizar_sucesso(user_repo, mock_db):
    user = Usuario(id=1, email="teste@example.com")

    resultado = user_repo.atualizar(user)
    assert resultado == user
    mock_db.merge.assert_called_once_with(user)
    mock_db.commit.assert_called_once()

def test_deletar_sucesso(user_repo, mock_db):
    user = Usuario(id=1, email="teste@example.com")

    resultado = user_repo.deletar(user)
    assert resultado is True
    mock_db.delete.assert_called_once_with(user)
    mock_db.commit.assert_called_once()

def test_deletar_erro(user_repo, mock_db):
    user = Usuario(id=1, email="teste@example.com")
    mock_db.delete.side_effect = SQLAlchemyError("Erro ao deletar")

    with pytest.raises(Exception) as excinfo:
        user_repo.deletar(user)
    assert "Erro ao deletar usuário" in str(excinfo.value)
    mock_db.rollback.assert_called_once()
