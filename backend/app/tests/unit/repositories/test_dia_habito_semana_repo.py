import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from app.repositories.DiaHabitoSemanaRepository import DiaHabitoSemanaRepository
from app.models.DiaHabitoSemana import DiaHabitoSemana, DiaSemanaEnum


@pytest.fixture
def mock_db():
    return create_autospec(Session)

@pytest.fixture
def repo(mock_db):
    return DiaHabitoSemanaRepository(db=mock_db)

# ----------- buscar_todos -----------

def test_buscar_todos(repo, mock_db):
    dias = [DiaHabitoSemana(id=1, habito_id=1, dia=DiaSemanaEnum.SEGUNDA)]
    mock_db.query().all.return_value = dias
    resultado = repo.buscar_todos()
    assert resultado == dias

def test_buscar_todos_vazio(repo, mock_db):
    mock_db.query().all.return_value = []
    with pytest.raises(Exception, match="Nenhum dia de hábito semanal encontrado"):
        repo.buscar_todos()

# ----------- buscar_por_habito -----------

def test_buscar_por_habito(repo, mock_db):
    dias = [DiaHabitoSemana(id=2, habito_id=2, dia=DiaSemanaEnum.QUARTA)]
    mock_db.query().filter_by().all.return_value = dias
    resultado = repo.buscar_por_habito(2)
    assert resultado == dias

def test_buscar_por_habito_vazio(repo, mock_db):
    mock_db.query().filter_by().all.return_value = []
    with pytest.raises(Exception, match="Nenhum dia encontrado para o hábito informado"):
        repo.buscar_por_habito(999)

# ----------- adicionar_dia -----------

def test_adicionar_dia(repo, mock_db):
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    resultado = repo.adicionar_dia(habito_id=1, dia=DiaSemanaEnum.SEXTA)
    assert isinstance(resultado, DiaHabitoSemana)
    assert resultado.habito_id == 1
    assert resultado.dia == DiaSemanaEnum.SEXTA
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

def test_adicionar_dia_erro(repo, mock_db):
    mock_db.commit.side_effect = SQLAlchemyError("erro")
    with pytest.raises(Exception, match="Erro ao adicionar dia ao hábito semanal"):
        repo.adicionar_dia(habito_id=1, dia=DiaSemanaEnum.SABADO)
    mock_db.rollback.assert_called_once()

# ----------- remover_dia -----------

def test_remover_dia(repo, mock_db):
    dia = DiaHabitoSemana(id=1, habito_id=1, dia=DiaSemanaEnum.TERCA)
    mock_db.query().filter_by().first.return_value = dia
    resultado = repo.remover_dia(dia_id=1)
    mock_db.delete.assert_called_once_with(dia)
    mock_db.commit.assert_called_once()
    assert resultado is None  # A função não retorna nada

def test_remover_dia_nao_encontrado(repo, mock_db):
    mock_db.query().filter_by().first.return_value = None
    with pytest.raises(Exception, match="Dia não encontrado"):
        repo.remover_dia(dia_id=999)

# ----------- remover_por_usuario -----------

def test_remover_por_usuario(repo, mock_db):
    dias = [
        DiaHabitoSemana(id=1, habito_id=1, dia=DiaSemanaEnum.DOMINGO),
        DiaHabitoSemana(id=2, habito_id=1, dia=DiaSemanaEnum.QUINTA)
    ]
    mock_query = mock_db.query().join().filter_by()
    mock_query.all.return_value = dias
    resultado = repo.remover_por_usuario(usuario_id=1)
    assert resultado == 2
    assert mock_db.delete.call_count == 2
    mock_db.commit.assert_called_once()

def test_remover_por_usuario_vazio(repo, mock_db):
    mock_db.query().join().filter_by().all.return_value = []
    with pytest.raises(Exception, match="Nenhum dia de hábito semanal encontrado para este usuário"):
        repo.remover_por_usuario(usuario_id=2)
