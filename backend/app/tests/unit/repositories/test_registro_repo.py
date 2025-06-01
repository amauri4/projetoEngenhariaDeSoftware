import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError

from app.repositories.registro_diario_repository import RegistroDiarioRepository
from app.models.RegistroDiario import RegistroDiario
from app.models.HabitoUsuario import HabitoUsuario


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def repo(mock_db):
    return RegistroDiarioRepository(mock_db)


def test_buscar_todos_sucesso(repo, mock_db):
    registro_mock = MagicMock(spec=RegistroDiario)
    mock_db.query.return_value.all.return_value = [registro_mock]

    resultado = repo.buscar_todos()

    assert resultado == [registro_mock]
    mock_db.query.assert_called_once_with(RegistroDiario)
    mock_db.query.return_value.all.assert_called_once()


def test_buscar_todos_nao_encontra(repo, mock_db):
    mock_db.query.return_value.all.return_value = []

    with pytest.raises(Exception) as e:
        repo.buscar_todos()
    assert "Nenhum registro encontrado" in str(e.value)
    # rollback não é chamado porque o erro é NoResultFound capturado diretamente


def test_buscar_todos_erro_sqlalchemy(repo, mock_db):
    mock_db.query.return_value.all.side_effect = SQLAlchemyError("Erro DB")
    with pytest.raises(Exception) as e:
        repo.buscar_todos()
    assert "Erro ao buscar registros" in str(e.value)
    mock_db.rollback.assert_called_once()


def test_criar_registro_sucesso(repo, mock_db):
    habito_mock = MagicMock(spec=HabitoUsuario)
    habito_mock.id = 1
    mock_db.query.return_value.filter_by.return_value.first.return_value = habito_mock
    mock_db.add.return_value = None
    mock_db.commit.return_value = None

    data = datetime.now()
    resultado = repo.criar_registro(data=data, habito_id=1, concluido=True)

    assert resultado.concluido is True
    assert resultado.habito_id == 1
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


def test_criar_registro_habito_nao_encontrado(repo, mock_db):
    mock_db.query.return_value.filter_by.return_value.first.return_value = None
    with pytest.raises(Exception) as e:
        repo.criar_registro(datetime.now(), habito_id=999)
    assert "Hábito não encontrado" in str(e.value)


def test_criar_registro_erro_sqlalchemy(repo, mock_db):
    habito_mock = MagicMock(spec=HabitoUsuario)
    mock_db.query.return_value.filter_by.return_value.first.return_value = habito_mock
    mock_db.add.side_effect = SQLAlchemyError("Erro DB")

    with pytest.raises(Exception) as e:
        repo.criar_registro(datetime.now(), habito_id=1)
    assert "Erro ao criar registro" in str(e.value)
    mock_db.rollback.assert_called_once()


def test_atualizar_registro_sucesso(repo, mock_db):
    registro_mock = MagicMock(spec=RegistroDiario)
    mock_db.query.return_value.filter_by.return_value.first.return_value = registro_mock
    mock_db.commit.return_value = None

    resultado = repo.atualizar_registro(registro_id=1, concluido=True)
    assert resultado == registro_mock
    assert registro_mock.concluido is True
    mock_db.commit.assert_called_once()


def test_atualizar_registro_nao_encontrado(repo, mock_db):
    mock_db.query.return_value.filter_by.return_value.first.return_value = None
    with pytest.raises(Exception) as e:
        repo.atualizar_registro(1, True)
    assert "Registro não encontrado" in str(e.value)


def test_remover_registro_sucesso(repo, mock_db):
    registro_mock = MagicMock(spec=RegistroDiario)
    mock_db.query.return_value.filter_by.return_value.first.return_value = registro_mock
    mock_db.delete.return_value = None
    mock_db.commit.return_value = None

    repo.remover_registro(1)
    mock_db.delete.assert_called_once_with(registro_mock)
    mock_db.commit.assert_called_once()


def test_remover_registro_nao_encontrado(repo, mock_db):
    mock_db.query.return_value.filter_by.return_value.first.return_value = None
    with pytest.raises(Exception) as e:
        repo.remover_registro(1)
    assert "Registro não encontrado" in str(e.value)


def test_buscar_por_usuario_sucesso(repo, mock_db):
    registro_mock = MagicMock(spec=RegistroDiario)
    mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = [registro_mock]

    resultado = repo.buscar_por_usuario(usuario_id=1)
    assert resultado == [registro_mock]


def test_buscar_por_usuario_nao_encontra(repo, mock_db):
    mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = []
    with pytest.raises(Exception) as e:
        repo.buscar_por_usuario(1)
    assert "Nenhum registro encontrado para o usuário" in str(e.value)


def test_buscar_concluidos_por_usuario_sucesso(repo, mock_db):
    registro_mock = MagicMock(spec=RegistroDiario)
    mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = [registro_mock]

    resultado = repo.buscar_concluidos_por_usuario(usuario_id=1)
    assert resultado == [registro_mock]


def test_buscar_concluidos_por_usuario_nao_encontra(repo, mock_db):
    mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = []
    with pytest.raises(Exception) as e:
        repo.buscar_concluidos_por_usuario(1)
    assert "Nenhum registro concluído encontrado para o usuário" in str(e.value)


def test_buscar_por_data_com_filtros(repo, mock_db):
    registro_mock = MagicMock(spec=RegistroDiario)
    query_mock = MagicMock()
    mock_db.query.return_value.join.return_value.filter.return_value = query_mock
    query_mock.filter.return_value = query_mock
    query_mock.all.return_value = [registro_mock]

    resultado = repo.buscar_por_data(
        usuario_id=1,
        data_inicio=datetime(2020, 1, 1),
        data_fim=datetime(2020, 12, 31)
    )
    assert resultado == [registro_mock]


def test_buscar_por_data_sem_resultado(repo, mock_db):
    query_mock = MagicMock()
    mock_db.query.return_value.join.return_value.filter.return_value = query_mock
    query_mock.filter.return_value = query_mock
    query_mock.all.return_value = []
    with pytest.raises(Exception) as e:
        repo.buscar_por_data(usuario_id=1)
    assert "Nenhum registro encontrado para o filtro de data" in str(e.value)


def test_buscar_por_data_especifica_sucesso(repo, mock_db):
    registro_mock = MagicMock(spec=RegistroDiario)
    mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = [registro_mock]

    data_especifica = datetime(2020, 1, 1)
    resultado = repo.buscar_por_data_especifica(usuario_id=1, data_especifica=data_especifica)
    assert resultado == [registro_mock]


def test_buscar_por_data_especifica_sem_resultado(repo, mock_db):
    mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = []
    data_especifica = datetime(2020, 1, 1)
    with pytest.raises(Exception) as e:
        repo.buscar_por_data_especifica(usuario_id=1, data_especifica=data_especifica)
    assert "Nenhum registro encontrado para a data" in str(e.value)
