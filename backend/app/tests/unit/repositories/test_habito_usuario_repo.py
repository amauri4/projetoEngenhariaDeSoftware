import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError

from app.models.Aplicacao1.frequencia_enums import FrequenciaEnum
from app.models.DiaHabitoSemana import DiaSemanaEnum
from app.models.HabitoUsuario import HabitoUsuario
from app.models.HabitoBase import HabitoBase
from app.models.Usuario import Usuario
from app.models.DiaHabitoSemana import DiaHabitoSemana

from app.repositories.habito_usuario_repository import HabitoUsuarioRepository


@pytest.fixture
def mock_db():
    return MagicMock()


def test_buscar_todos_sucesso(mock_db):
    habito_mock = MagicMock()
    mock_db.query.return_value.all.return_value = [habito_mock]

    repo = HabitoUsuarioRepository(mock_db)
    resultado = repo.buscar_todos()

    assert resultado == [habito_mock]
    mock_db.query.assert_called_once_with(HabitoUsuario)


def test_buscar_todos_sem_resultado_gera_erro(mock_db):
    mock_db.query.return_value.all.return_value = []

    repo = HabitoUsuarioRepository(mock_db)
    with pytest.raises(Exception, match="Nenhum hábito de usuário encontrado."):
        repo.buscar_todos()
    mock_db.rollback.assert_called_once()


def test_criar_habito_usuario_sucesso(mock_db):
    habito_base = MagicMock(spec=HabitoBase)
    usuario = MagicMock(spec=Usuario)
    mock_db.query.return_value.filter_by.return_value.first.side_effect = [habito_base, usuario]

    # Mock do novo hábito criado
    novo_habito = MagicMock(spec=HabitoUsuario)
    novo_habito.id = 1

    # Patch do construtor para retornar o mock criado
    with patch("app.repositories.habito_usuario_repository.HabitoUsuario", return_value=novo_habito):
        repo = HabitoUsuarioRepository(mock_db)
        resultado = repo.criar_habito_usuario(
            descricao="Dormir bem",
            habito_base_id=1,
            usuario_id=2,
            frequencia=FrequenciaEnum.diaria,
            data_inicio=datetime.now(),
            quantidade_semanal=3,
            dias_da_semana=["segunda", "terca"]
        )

    assert resultado == novo_habito
    mock_db.add.assert_any_call(novo_habito)
    mock_db.commit.assert_called_once()


def test_criar_habito_usuario_sem_habito_base_ou_usuario(mock_db):
    mock_db.query.return_value.filter_by.return_value.first.side_effect = [None, None]

    repo = HabitoUsuarioRepository(mock_db)
    with pytest.raises(Exception, match="Hábito base ou usuário não encontrado."):
        repo.criar_habito_usuario(
            descricao="Dormir bem",
            habito_base_id=1,
            usuario_id=2,
            frequencia=FrequenciaEnum.semanal,
            data_inicio=datetime.now()
        )
    mock_db.rollback.assert_called_once()


def test_atualizar_habito_usuario_sucesso(mock_db):
    habito = MagicMock(spec=HabitoUsuario)
    habito.id = 1
    mock_db.query.return_value.filter_by.return_value.first.return_value = habito

    repo = HabitoUsuarioRepository(mock_db)
    resultado = repo.atualizar_habito_usuario(
        habito_usuario_id=1,
        nova_descricao="Nova desc",
        novo_habito_base_id=2,
        novo_usuario_id=3,
        nova_data_inicio=datetime.now(),
        nova_frequencia=FrequenciaEnum.diaria,
        nova_quantidade_semanal=4,
        novos_dias_da_semana=["segunda", "quarta"]
    )

    assert resultado == habito
    assert habito.descricao == "Nova desc"
    assert habito.habito_base_id == 2
    assert habito.usuario_id == 3
    assert habito.frequencia == FrequenciaEnum.diaria
    mock_db.commit.assert_called_once()


def test_atualizar_habito_usuario_nao_encontrado(mock_db):
    mock_db.query.return_value.filter_by.return_value.first.return_value = None

    repo = HabitoUsuarioRepository(mock_db)
    with pytest.raises(Exception, match="Hábito de usuário não encontrado."):
        repo.atualizar_habito_usuario(
            habito_usuario_id=1,
            nova_descricao="desc",
            novo_habito_base_id=2,
            novo_usuario_id=3,
            nova_data_inicio=datetime.now(),
            nova_frequencia=FrequenciaEnum.semanal
        )
    mock_db.rollback.assert_called_once()


def test_remover_habito_usuario_sucesso(mock_db):
    habito = MagicMock(spec=HabitoUsuario)
    mock_db.query.return_value.filter_by.return_value.first.return_value = habito

    repo = HabitoUsuarioRepository(mock_db)
    repo.remover_habito_usuario(1)

    mock_db.delete.assert_called_once_with(habito)
    mock_db.commit.assert_called_once()


def test_remover_habito_usuario_nao_encontrado(mock_db):
    mock_db.query.return_value.filter_by.return_value.first.return_value = None

    repo = HabitoUsuarioRepository(mock_db)
    with pytest.raises(Exception, match="Hábito de usuário não encontrado."):
        repo.remover_habito_usuario(1)
    mock_db.rollback.assert_called_once()


def test_buscar_por_email_sucesso(mock_db):
    usuario = MagicMock(spec=Usuario)
    usuario.id = 1
    habito1 = MagicMock(spec=HabitoUsuario)
    habito2 = MagicMock(spec=HabitoUsuario)

    mock_db.query.return_value.filter_by.return_value.first.return_value = usuario
    mock_db.query.return_value.filter_by.return_value.all.return_value = [habito1, habito2]

    repo = HabitoUsuarioRepository(mock_db)
    resultado = repo.buscar_por_email("teste@email.com")

    assert resultado == [habito1, habito2]


def test_buscar_por_email_usuario_nao_encontrado(mock_db):
    mock_db.query.return_value.filter_by.return_value.first.return_value = None

    repo = HabitoUsuarioRepository(mock_db)
    with pytest.raises(Exception, match="Usuário não encontrado."):
        repo.buscar_por_email("teste@email.com")
    mock_db.rollback.assert_called_once()


def test_buscar_por_email_sem_habitos(mock_db):
    usuario = MagicMock(spec=Usuario)
    usuario.id = 1

    mock_db.query.return_value.filter_by.return_value.first.return_value = usuario
    mock_db.query.return_value.filter_by.return_value.all.return_value = []

    repo = HabitoUsuarioRepository(mock_db)
    with pytest.raises(Exception, match="Nenhum hábito encontrado para o usuário."):
        repo.buscar_por_email("teste@email.com")
    mock_db.rollback.assert_called_once()


def test_buscar_por_id_sucesso(mock_db):
    habito1 = MagicMock(spec=HabitoUsuario)
    mock_db.query.return_value.filter_by.return_value.all.return_value = [habito1]

    repo = HabitoUsuarioRepository(mock_db)
    resultado = repo.buscar_por_id(1)

    assert resultado == [habito1]


def test_buscar_por_id_nao_encontrado(mock_db):
    mock_db.query.return_value.filter_by.return_value.all.return_value = []

    repo = HabitoUsuarioRepository(mock_db)
    with pytest.raises(Exception, match="Hábito de usuário não encontrado."):
        repo.buscar_por_id(1)
    mock_db.rollback.assert_called_once()


def test_buscar_por_usuario_sucesso(mock_db):
    usuario = MagicMock(spec=Usuario)
    usuario.id = 1
    habito1 = MagicMock(spec=HabitoUsuario)

    mock_db.query.return_value.filter_by.return_value.first.return_value = usuario
    mock_db.query.return_value.filter.return_value.all.return_value = [habito1]

    repo = HabitoUsuarioRepository(mock_db)
    resultado = repo.buscar_por_usuario(1)

    assert resultado == [habito1]


def test_buscar_por_usuario_usuario_nao_encontrado(mock_db):
    mock_db.query.return_value.filter_by.return_value.first.return_value = None

    repo = HabitoUsuarioRepository(mock_db)
    with pytest.raises(Exception, match="Usuário não encontrado."):
        repo.buscar_por_usuario(1)
    mock_db.rollback.assert_called_once()
