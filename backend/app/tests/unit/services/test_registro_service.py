import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from sqlalchemy.exc import NoResultFound

from app.services.RegistroDiarioService import RegistroDiarioService

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def service(mock_db):
    # Criando uma nova instância do service com db mockado
    # Reset singleton para cada teste
    RegistroDiarioService._instance = None
    return RegistroDiarioService(mock_db)

def test_buscar_registros_usuario(service):
    # Mock do método do repositório
    service.registro_diario_repository.buscar_por_usuario = MagicMock(return_value=["registro1", "registro2"])
    
    resultado = service.buscar_registros_usuario(1)
    assert resultado == ["registro1", "registro2"]
    service.registro_diario_repository.buscar_por_usuario.assert_called_once_with(1)

def test_buscar_registros_usuario_erro(service):
    service.registro_diario_repository.buscar_por_usuario = MagicMock(side_effect=Exception("Erro banco"))
    with pytest.raises(Exception) as excinfo:
        service.buscar_registros_usuario(1)
    assert "Erro ao buscar registros diários do usuário" in str(excinfo.value)

def test_buscar_registros_concluidos_usuario(service):
    service.registro_diario_repository.buscar_concluidos_por_usuario = MagicMock(return_value=["registro_concluido"])
    resultado = service.buscar_registros_concluidos_usuario(1)
    assert resultado == ["registro_concluido"]
    service.registro_diario_repository.buscar_concluidos_por_usuario.assert_called_once_with(1)

def test_criar_registro_diario_sucesso(service):
    habito_mock = MagicMock()
    service.habito_usuario_repository.buscar_por_id = MagicMock(return_value=habito_mock)
    service.registro_diario_repository.criar_registro = MagicMock(return_value="novo_registro")
    
    data_teste = "2025-06-01"
    resultado = service.criar_registro_diario(data_teste, habito_id=1, concluido=False)
    assert resultado == "novo_registro"
    service.habito_usuario_repository.buscar_por_id.assert_called_once_with(1)
    service.registro_diario_repository.criar_registro.assert_called_once()

def test_criar_registro_diario_habito_nao_encontrado(service):
    service.habito_usuario_repository.buscar_por_id = MagicMock(return_value=None)
    with pytest.raises(Exception) as excinfo:
        service.criar_registro_diario("2025-06-01", habito_id=999)
    assert "Hábito não encontrado" in str(excinfo.value)

def test_atualizar_registro_diario_sucesso(service):
    service.registro_diario_repository.atualizar_registro = MagicMock(return_value="registro_atualizado")
    resultado = service.atualizar_registro_diario(1, True)
    assert resultado == "registro_atualizado"
    service.registro_diario_repository.atualizar_registro.assert_called_once_with(1, True)

def test_atualizar_registro_diario_erro(service):
    service.registro_diario_repository.atualizar_registro = MagicMock(side_effect=Exception("Erro update"))
    with pytest.raises(Exception) as excinfo:
        service.atualizar_registro_diario(1, True)
    assert "Erro ao atualizar o registro diário" in str(excinfo.value)

def test_remover_registro_diario_sucesso(service):
    service.registro_diario_repository.remover_registro = MagicMock()
    service.remover_registro_diario(1)
    service.registro_diario_repository.remover_registro.assert_called_once_with(1)

def test_remover_registro_diario_erro(service):
    service.registro_diario_repository.remover_registro = MagicMock(side_effect=Exception("Erro remoção"))
    with pytest.raises(Exception) as excinfo:
        service.remover_registro_diario(1)
    assert "Erro ao remover o registro diário" in str(excinfo.value)

def test_buscar_registros_por_data(service):
    service.registro_diario_repository.buscar_por_data = MagicMock(return_value=["registro1"])
    resultado = service.buscar_registros_por_data(1, datetime(2025,6,1), datetime(2025,6,30))
    assert resultado == ["registro1"]
    service.registro_diario_repository.buscar_por_data.assert_called_once()

def test_buscar_registros_por_data_erro(service):
    service.registro_diario_repository.buscar_por_data = MagicMock(side_effect=Exception("Erro data"))
    with pytest.raises(Exception) as excinfo:
        service.buscar_registros_por_data(1, datetime(2025,6,1), datetime(2025,6,30))
    assert "Erro ao buscar registros por data" in str(excinfo.value)

def test_buscar_registros_por_data_especifica(service):
    service.registro_diario_repository.buscar_por_data_especifica = MagicMock(return_value=["registro_especifico"])
    resultado = service.buscar_registros_por_data_especifica(1, datetime(2025,6,15))
    assert resultado == ["registro_especifico"]
    service.registro_diario_repository.buscar_por_data_especifica.assert_called_once()

def test_buscar_registros_por_data_especifica_erro(service):
    service.registro_diario_repository.buscar_por_data_especifica = MagicMock(side_effect=Exception("Erro data específica"))
    with pytest.raises(Exception) as excinfo:
        service.buscar_registros_por_data_especifica(1, datetime(2025,6,15))
    assert "Erro ao buscar registros na data específica" in str(excinfo.value)
