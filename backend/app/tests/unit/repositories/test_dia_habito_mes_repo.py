import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from app.repositories.DiaHabitoMesRepository import DiaHabitoMesRepository
from app.models.DiaHabitoMes import DiaHabitoMes


@pytest.fixture
def mock_db():
    return create_autospec(Session)

@pytest.fixture
def repo(mock_db):
    return DiaHabitoMesRepository(db=mock_db)


# ----- TESTE: buscar_todos -----
def test_buscar_todos(repo, mock_db):
    dias = [DiaHabitoMes(id=1, habito_id=1, dia=10)]
    mock_db.query().all.return_value = dias
    resultado = repo.buscar_todos()
    assert resultado == dias

def test_buscar_todos_vazio(repo, mock_db):
    mock_db.query().all.return_value = []
    with pytest.raises(Exception, match="Nenhum dia de hábito mensal encontrado"):
        repo.buscar_todos()

# ----- TESTE: buscar_por_habito -----
def test_buscar_por_habito(repo, mock_db):
    dias = [DiaHabitoMes(id=1, habito_id=2, dia=15)]
    mock_db.query().filter_by().all.return_value = dias
    resultado = repo.buscar_por_habito(2)
    assert resultado == dias

def test_buscar_por_habito_vazio(repo, mock_db):
    mock_db.query().filter_by().all.return_value = []
    with pytest.raises(Exception, match="Nenhum dia encontrado para o hábito informado"):
        repo.buscar_por_habito(99)

# ----- TESTE: adicionar_dia -----
def test_adicionar_dia(repo, mock_db):
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    resultado = repo.adicionar_dia(habito_id=1, dia=5)
    assert isinstance(resultado, DiaHabitoMes)
    assert resultado.habito_id == 1
    assert resultado.dia == 5
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

def test_adicionar_dia_erro(repo, mock_db):
    mock_db.commit.side_effect = SQLAlchemyError("Erro")
    with pytest.raises(Exception, match="Erro ao adicionar dia ao hábito mensal"):
        repo.adicionar_dia(habito_id=1, dia=5)
    mock_db.rollback.assert_called_once()

# ----- TESTE: remover_por_usuario -----
def test_remover_por_usuario(repo, mock_db):
    dias = [
        DiaHabitoMes(id=1, habito_id=1, dia=1),
        DiaHabitoMes(id=2, habito_id=1, dia=2)
    ]
    mock_query = mock_db.query().join().filter_by()
    mock_query.all.return_value = dias

    resultado = repo.remover_por_usuario(usuario_id=1)
    assert resultado == 2
    assert mock_db.delete.call_count == 2
    mock_db.commit.assert_called_once()

def test_remover_por_usuario_vazio(repo, mock_db):
    mock_db.query().join().filter_by().all.return_value = []
    with pytest.raises(Exception, match="Nenhum dia de hábito mensal encontrado para este usuário"):
        repo.remover_por_usuario(usuario_id=1)
