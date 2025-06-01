import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from app.services.CorrelacaoHabitoService import CorrelacaoHabitoService

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

@pytest.fixture
def correlacao_service(mock_db):
    return CorrelacaoHabitoService(mock_db)

def test_processar_correlacoes_basico(correlacao_service):
    # Dados simulados de registros
    registros = [
        MagicMock(id=1, data="2024-06-01", concluido=True, habito_id=0),
        MagicMock(id=2, data="2024-06-01", concluido=False, habito_id=1),
        MagicMock(id=3, data="2024-06-02", concluido=True, habito_id=1),
        MagicMock(id=4, data="2024-06-02", concluido=True, habito_id=0),
    ]
    habitos_base_names = ["Habito0", "Habito1"]

    resultado = correlacao_service._processar_correlacoes(registros, habitos_base_names)
    assert isinstance(resultado, str)
    # Deve conter nomes dos hábitos na saída, pois são as variáveis correlacionadas
    assert "Habito0" in resultado or "Habito1" in resultado

def test_buscar_correlacoes_habitos_sucesso(correlacao_service, mock_db):
    # Mock dos repositórios internos do serviço
    habito_base_mock = MagicMock()
    habito_base_mock.nome = "HabitoTest"

    registro_mock = MagicMock()
    
    # Substituir métodos dos repositórios por mocks que retornam listas simuladas
    correlacao_service.registro_repository.buscar_por_usuario = MagicMock(return_value=[registro_mock])
    correlacao_service.habito_base_repository.buscar_todos = MagicMock(return_value=[habito_base_mock])
    
    # Mock do método privado para retornar um texto fixo, isolando o teste
    correlacao_service._processar_correlacoes = MagicMock(return_value="resultado esperado")

    resultado = correlacao_service.buscar_correlacoes_habitos(usuario_id=123)
    assert resultado == "resultado esperado"
    correlacao_service.registro_repository.buscar_por_usuario.assert_called_once_with(123)
    correlacao_service.habito_base_repository.buscar_todos.assert_called_once()

def test_buscar_correlacoes_habitos_sem_registros(correlacao_service):
    correlacao_service.registro_repository.buscar_por_usuario = MagicMock(return_value=[])
    correlacao_service.habito_base_repository.buscar_todos = MagicMock(return_value=[MagicMock()])
    
    with pytest.raises(NoResultFound):
        correlacao_service.buscar_correlacoes_habitos(usuario_id=1)

def test_buscar_correlacoes_habitos_sem_habitos(correlacao_service):
    correlacao_service.registro_repository.buscar_por_usuario = MagicMock(return_value=[MagicMock()])
    correlacao_service.habito_base_repository.buscar_todos = MagicMock(return_value=[])
    
    with pytest.raises(NoResultFound):
        correlacao_service.buscar_correlacoes_habitos(usuario_id=1)

def test_buscar_correlacoes_habitos_erro_banco(correlacao_service, mock_db):
    correlacao_service.registro_repository.buscar_por_usuario = MagicMock(side_effect=SQLAlchemyError("Erro BD"))
    correlacao_service.habito_base_repository.buscar_todos = MagicMock(return_value=[MagicMock()])

    with pytest.raises(Exception) as e:
        correlacao_service.buscar_correlacoes_habitos(usuario_id=1)
    assert "Erro no banco de dados" in str(e.value)

def test_processar_correlacoes_erro(correlacao_service):
    # Forçar um erro passando dados errados para o método privado
    with pytest.raises(Exception) as e:
        correlacao_service._processar_correlacoes(registros=None, habitos_base_names=None)
    assert "Erro ao processar correlações" in str(e.value)
