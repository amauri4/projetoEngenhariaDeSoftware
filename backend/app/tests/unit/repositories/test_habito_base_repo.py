import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from app.repositories.HabitoBaseRepository import HabitoBaseRepository
from app.models.HabitoBase import HabitoBase
from app.models.CategoriasHabito import CategoriaHabito


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def repository(mock_session):
    return HabitoBaseRepository(mock_session)


def test_buscar_todos_sucesso(repository, mock_session):
    mock_session.query.return_value.all.return_value = [HabitoBase(id=1, nome="Test", categoria_id=1)]

    result = repository.buscar_todos()
    assert len(result) == 1
    assert isinstance(result[0], HabitoBase)


def test_buscar_todos_vazio(repository, mock_session):
    mock_session.query.return_value.all.return_value = []

    with pytest.raises(Exception, match="Nenhum hábito encontrado."):
        repository.buscar_todos()


def test_buscar_por_id_sucesso(repository, mock_session):
    mock_session.query.return_value.filter_by.return_value.first.return_value = HabitoBase(id=1, nome="Test", categoria_id=1)

    result = repository.buscar_por_id(1)
    assert result.nome == "Test"


def test_buscar_por_id_nao_encontrado(repository, mock_session):
    mock_session.query.return_value.filter_by.return_value.first.return_value = None

    with pytest.raises(Exception, match="Hábito não encontrado."):
        repository.buscar_por_id(1)


def test_criar_habito_sucesso(repository, mock_session):
    mock_session.query.return_value.filter_by.return_value.first.return_value = CategoriaHabito(id=1, nome="Saúde")

    result = repository.criar_habito(nome="Correr", categoria_id=1)
    assert isinstance(result, HabitoBase)
    assert result.nome == "Correr"
    assert result.categoria_id == 1
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_criar_habito_categoria_nao_encontrada(repository, mock_session):
    mock_session.query.return_value.filter_by.return_value.first.return_value = None

    with pytest.raises(Exception, match="Categoria não encontrada."):
        repository.criar_habito(nome="Correr", categoria_id=99)


def test_atualizar_habito_sucesso(repository, mock_session):
    habito = HabitoBase(id=1, nome="Antigo", categoria_id=1)
    categoria = CategoriaHabito(id=2, nome="Nova")

    mock_session.query.return_value.filter_by.side_effect = [
        MagicMock(first=MagicMock(return_value=habito)),   # Habito
        MagicMock(first=MagicMock(return_value=categoria)) # Categoria
    ]

    result = repository.atualizar_habito(1, "Novo Nome", 2)
    assert result.nome == "Novo Nome"
    assert result.categoria_id == 2
    mock_session.commit.assert_called_once()


def test_atualizar_habito_nao_encontrado(repository, mock_session):
    mock_session.query.return_value.filter_by.return_value.first.return_value = None

    with pytest.raises(Exception, match="Hábito não encontrado."):
        repository.atualizar_habito(1, "Novo", 2)


def test_remover_habito_sucesso(repository, mock_session):
    habito = HabitoBase(id=1, nome="Apagar", categoria_id=1)
    mock_session.query.return_value.filter_by.return_value.first.return_value = habito

    repository.remover_habito(1)
    mock_session.delete.assert_called_once_with(habito)
    mock_session.commit.assert_called_once()


def test_remover_habito_nao_encontrado(repository, mock_session):
    mock_session.query.return_value.filter_by.return_value.first.return_value = None

    with pytest.raises(Exception, match="Hábito não encontrado."):
        repository.remover_habito(1)
