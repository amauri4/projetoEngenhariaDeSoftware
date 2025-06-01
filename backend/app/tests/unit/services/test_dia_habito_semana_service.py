import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import NoResultFound
from app.models.DiaHabitoSemana import DiaSemanaEnum
from app.services.DiaHabitoSemanaService import DiaHabitoSemanaService

@pytest.fixture
def mock_repo():
    repo = MagicMock()
    return repo

@pytest.fixture
def service(mock_repo):
    # Patcha o construtor do repository para retornar o mock
    with patch('app.services.DiaHabitoSemanaService.DiaHabitoSemanaRepository', return_value=mock_repo):
        yield DiaHabitoSemanaService(db=None)  # db é irrelevante pois é mockado

def test_buscar_todos_sucesso(service, mock_repo):
    mock_repo.buscar_todos.return_value = ['dia1', 'dia2']
    resultado = service.buscar_todos()
    assert resultado == ['dia1', 'dia2']
    mock_repo.buscar_todos.assert_called_once()

def test_buscar_todos_erro(service, mock_repo):
    mock_repo.buscar_todos.side_effect = Exception("Erro do repo")
    with pytest.raises(Exception) as excinfo:
        service.buscar_todos()
    assert "Erro ao buscar dias de hábito semanal" in str(excinfo.value)

def test_buscar_por_habito_sucesso(service, mock_repo):
    mock_repo.buscar_por_habito.return_value = ['dia1']
    resultado = service.buscar_por_habito(1)
    assert resultado == ['dia1']
    mock_repo.buscar_por_habito.assert_called_once_with(1)

def test_buscar_por_habito_erro(service, mock_repo):
    mock_repo.buscar_por_habito.side_effect = Exception("Erro repo")
    with pytest.raises(Exception) as excinfo:
        service.buscar_por_habito(1)
    assert "Erro ao buscar dias do hábito semanal" in str(excinfo.value)

def test_adicionar_dia_valido(service, mock_repo):
    mock_repo.adicionar_dia.return_value = 'dia_adicionado'
    resultado = service.adicionar_dia(1, 'segunda')
    assert resultado == 'dia_adicionado'
    mock_repo.adicionar_dia.assert_called_once_with(1, DiaSemanaEnum.segunda)

def test_adicionar_dia_invalido(service):
    with pytest.raises(ValueError) as excinfo:
        service.adicionar_dia(1, 'invalid_day')
    assert "Dia da semana inválido" in str(excinfo.value)

def test_adicionar_varios_dias_sucesso(service, mock_repo):
    mock_repo.adicionar_dia.side_effect = lambda habito_id, dia_enum: f"dia_{dia_enum.name}"
    dias = [1, 2]
    resultado = service.adicionar_varios_dias(1, dias)
    assert resultado == ['dia_segunda', 'dia_terca']
    assert mock_repo.adicionar_dia.call_count == 2

def test_adicionar_varios_dias_valor_invalido(service):
    with pytest.raises(ValueError) as excinfo:
        service.adicionar_varios_dias(1, [8])
    assert "Valor 8 inválido" in str(excinfo.value)

def test_remover_dia_por_id_sucesso(service, mock_repo):
    service.remover_dia_por_id(1)
    mock_repo.remover_dia.assert_called_once_with(1)

def test_remover_dia_por_id_erro(service, mock_repo):
    mock_repo.remover_dia.side_effect = Exception("Erro remover")
    with pytest.raises(Exception) as excinfo:
        service.remover_dia_por_id(1)
    assert "Erro ao remover dia do hábito semanal" in str(excinfo.value)

def test_remover_dia_por_habito_e_dia_sucesso(service, mock_repo):
    dia_obj = MagicMock()
    dia_obj.dia = DiaSemanaEnum.segunda
    dia_obj.id = 42
    mock_repo.buscar_por_habito.return_value = [dia_obj]

    service.remover_dia_por_habito_e_dia(1, 1)
    mock_repo.remover_dia.assert_called_once_with(42)

def test_remover_dia_por_habito_e_dia_dia_invalido(service):
    with pytest.raises(ValueError) as excinfo:
        service.remover_dia_por_habito_e_dia(1, 10)
    assert "Dia da semana inválido" in str(excinfo.value)

def test_remover_dia_por_habito_e_dia_dia_nao_encontrado(service, mock_repo):
    mock_repo.buscar_por_habito.return_value = []
    with pytest.raises(Exception) as excinfo:
        service.remover_dia_por_habito_e_dia(1, 1)
    assert "Dia não encontrado para este hábito" in str(excinfo.value)

def test_remover_todos_por_habito_sucesso(service, mock_repo):
    dia1 = MagicMock(id=1)
    dia2 = MagicMock(id=2)
    mock_repo.buscar_por_habito.return_value = [dia1, dia2]

    service.remover_todos_por_habito(1)
    assert mock_repo.remover_dia.call_count == 2
    mock_repo.remover_dia.assert_any_call(1)
    mock_repo.remover_dia.assert_any_call(2)

def test_remover_todos_por_habito_sem_dias(service, mock_repo):
    mock_repo.buscar_por_habito.return_value = []
    with pytest.raises(Exception) as excinfo:
        service.remover_todos_por_habito(1)
    assert "Nenhum dia encontrado para este hábito" in str(excinfo.value)
