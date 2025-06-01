import pytest
from unittest.mock import MagicMock
from sqlalchemy.exc import NoResultFound
from app.services.DiaHabitoMesService import DiaHabitoMesService

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(monkeypatch, mock_repo):
    # Mocka o repository dentro do serviço para evitar acesso real ao banco
    monkeypatch.setattr("app.services.DiaHabitoMesService.DiaHabitoMesRepository", lambda db: mock_repo)
    # Instancia o serviço (singleton, cuidado em testes isolados)
    return DiaHabitoMesService(db=MagicMock())

def test_singleton(service):
    s1 = service
    s2 = DiaHabitoMesService(db=MagicMock())
    assert s1 is s2  # Mesma instância (singleton)

def test_buscar_todos_chama_repo(service, mock_repo):
    mock_repo.buscar_todos.return_value = ["dia1", "dia2"]
    resultado = service.buscar_todos()
    mock_repo.buscar_todos.assert_called_once()
    assert resultado == ["dia1", "dia2"]

def test_buscar_todos_erro(service, mock_repo):
    mock_repo.buscar_todos.side_effect = Exception("Erro genérico")
    with pytest.raises(Exception) as e:
        service.buscar_todos()
    assert "Erro ao buscar dias de hábito mensal" in str(e.value)

def test_buscar_por_habito(service, mock_repo):
    mock_repo.buscar_por_habito.return_value = ["diaX"]
    resultado = service.buscar_por_habito(1)
    mock_repo.buscar_por_habito.assert_called_once_with(1)
    assert resultado == ["diaX"]

def test_buscar_por_habito_erro(service, mock_repo):
    mock_repo.buscar_por_habito.side_effect = Exception("Erro de busca")
    with pytest.raises(Exception) as e:
        service.buscar_por_habito(1)
    assert "Erro ao buscar dias do hábito mensal" in str(e.value)

def test_adicionar_dia_valido(service, mock_repo):
    mock_repo.adicionar_dia.return_value = "novo_dia"
    resultado = service.adicionar_dia(1, 15)
    mock_repo.adicionar_dia.assert_called_once_with(1, 15)
    assert resultado == "novo_dia"

@pytest.mark.parametrize("dia", [0, 32, -1, 100])
def test_adicionar_dia_invalido(service, dia):
    with pytest.raises(Exception) as e:
        service.adicionar_dia(1, dia)
    assert "Erro de validação" in str(e.value)

def test_adicionar_varios_dias_sucesso(service, mock_repo):
    mock_repo.adicionar_dia.side_effect = lambda habito_id, dia: f"dia{dia}"
    resultado = service.adicionar_varios_dias(1, [1, 2, 3])
    assert resultado == ["dia1", "dia2", "dia3"]
    assert mock_repo.adicionar_dia.call_count == 3

def test_adicionar_varios_dias_com_dia_invalido(service):
    with pytest.raises(Exception) as e:
        service.adicionar_varios_dias(1, [1, 0, 2])
    assert "Erro de validação" in str(e.value)

def test_remover_dia_por_id(service, mock_repo):
    service.remover_dia_por_id(123)
    mock_repo.remover_dia.assert_called_once_with(123)

def test_remover_dia_por_id_erro(service, mock_repo):
    mock_repo.remover_dia.side_effect = Exception("Erro remoção")
    with pytest.raises(Exception) as e:
        service.remover_dia_por_id(123)
    assert "Erro ao remover dia do hábito mensal" in str(e.value)

def test_remover_dia_por_habito_e_dia_sucesso(service, mock_repo):
    dia_mock = MagicMock(id=99, dia=5)
    mock_repo.buscar_por_habito.return_value = [dia_mock]
    service.remover_dia_por_habito_e_dia(1, 5)
    mock_repo.remover_dia.assert_called_once_with(99)

def test_remover_dia_por_habito_e_dia_nao_encontrado(service, mock_repo):
    mock_repo.buscar_por_habito.return_value = []
    with pytest.raises(Exception) as e:
        service.remover_dia_por_habito_e_dia(1, 5)
    assert "Dia não encontrado" in str(e.value)

def test_remover_dia_por_habito_e_dia_erro(service, mock_repo):
    mock_repo.buscar_por_habito.side_effect = Exception("Erro interno")
    with pytest.raises(Exception) as e:
        service.remover_dia_por_habito_e_dia(1, 5)
    assert "Erro ao remover dia do hábito mensal" in str(e.value)

def test_remover_todos_por_habito_sucesso(service, mock_repo):
    dias = [MagicMock(id=1), MagicMock(id=2)]
    mock_repo.buscar_por_habito.return_value = dias
    service.remover_todos_por_habito(10)
    assert mock_repo.remover_dia.call_count == 2

def test_remover_todos_por_habito_sem_dias(service, mock_repo):
    mock_repo.buscar_por_habito.return_value = []
    with pytest.raises(Exception) as e:
        service.remover_todos_por_habito(10)
    assert "Nenhum dia encontrado" in str(e.value)

def test_remover_todos_por_habito_erro(service, mock_repo):
    mock_repo.buscar_por_habito.side_effect = Exception("Erro na busca")
    with pytest.raises(Exception) as e:
        service.remover_todos_por_habito(10)
    assert "Erro ao remover dias do hábito mensal" in str(e.value)
