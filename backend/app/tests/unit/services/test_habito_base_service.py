import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from app.services.Aplicacao1.HabitoBaseService import HabitoBaseService

@pytest.fixture(autouse=True)
def reset_singleton():
    # Resetar a instância singleton antes de cada teste
    HabitoBaseService._instance = None
    yield
    HabitoBaseService._instance = None

def test_buscar_habitos_disponiveis_sucesso():
    mock_repo = MagicMock()
    mock_repo.buscar_todos.return_value = ["habito1", "habito2"]

    with patch("app.services.HabitoBaseService.HabitoBaseRepository", return_value=mock_repo):
        service = HabitoBaseService(db=MagicMock(spec=Session))
        resultado = service.buscar_habitos_disponiveis()
        assert resultado == ["habito1", "habito2"]
        mock_repo.buscar_todos.assert_called_once()

def test_buscar_habitos_disponiveis_erro():
    mock_repo = MagicMock()
    mock_repo.buscar_todos.side_effect = Exception("Erro do repositório")

    with patch("app.services.HabitoBaseService.HabitoBaseRepository", return_value=mock_repo):
        service = HabitoBaseService(db=MagicMock(spec=Session))
        with pytest.raises(Exception) as excinfo:
            service.buscar_habitos_disponiveis()
        assert "Erro no serviço ao buscar hábitos: Erro do repositório" in str(excinfo.value)

def test_singleton_mesma_instancia():
    with patch("app.services.HabitoBaseService.HabitoBaseRepository") as mock_repo:
        service1 = HabitoBaseService(db=MagicMock(spec=Session))
        service2 = HabitoBaseService(db=MagicMock(spec=Session))
        assert service1 is service2
