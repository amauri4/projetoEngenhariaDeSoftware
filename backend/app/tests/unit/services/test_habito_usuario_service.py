import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from datetime import datetime
from app.services.HabitoUsuarioService import HabitoUsuarioService

@pytest.fixture(autouse=True)
def reset_singleton():
    HabitoUsuarioService._instance = None
    yield
    HabitoUsuarioService._instance = None

def mock_usuario():
    mock = MagicMock()
    mock.id = 1
    mock.email = "teste@teste.com"
    return mock

def mock_habito_base():
    mock = MagicMock()
    mock.id = 10
    return mock

def mock_habito_usuario():
    mock = MagicMock()
    mock.id = 100
    mock.vezes_na_semana = None
    return mock

def test_buscar_habitos_usuario_sucesso():
    with patch("app.services.HabitoUsuarioService.UserRepository") as mock_user_repo, \
         patch("app.services.HabitoUsuarioService.HabitoUsuarioRepository") as mock_habito_usuario_repo:

        mock_user_repo.return_value.buscar_por_email.return_value = mock_usuario()
        mock_habito_usuario_repo.return_value.buscar_por_email.return_value = ["habito1", "habito2"]

        service = HabitoUsuarioService(db=MagicMock(spec=Session))
        resultado = service.buscar_habitos_usuario("teste@teste.com")

        assert resultado == ["habito1", "habito2"]
        mock_user_repo.return_value.buscar_por_email.assert_called_once_with("teste@teste.com")
        mock_habito_usuario_repo.return_value.buscar_por_email.assert_called_once_with("teste@teste.com")

def test_buscar_habitos_usuario_usuario_nao_encontrado():
    with patch("app.services.HabitoUsuarioService.UserRepository") as mock_user_repo:
        mock_user_repo.return_value.buscar_por_email.return_value = None

        service = HabitoUsuarioService(db=MagicMock(spec=Session))
        with pytest.raises(Exception) as e:
            service.buscar_habitos_usuario("email@naoexiste.com")

        assert "Usuário não encontrado" in str(e.value)

@patch("app.services.HabitoUsuarioService.validar_frequencia", return_value=True)
@patch("app.services.HabitoUsuarioService.validar_formato_data", side_effect=lambda x: x)
@patch("app.services.HabitoUsuarioService.converter_numero_para_dia_semana", side_effect=lambda x: x)
def test_adicionar_habito_usuario_semanal(mock_converter, mock_validar_data, mock_validar_freq):
    with patch("app.services.HabitoUsuarioService.UserRepository") as mock_user_repo, \
         patch("app.services.HabitoUsuarioService.HabitoBaseRepository") as mock_habito_base_repo, \
         patch("app.services.HabitoUsuarioService.HabitoUsuarioRepository") as mock_habito_usuario_repo, \
         patch("app.services.HabitoUsuarioService.DiaHabitoSemanaRepository") as mock_dia_semana_repo, \
         patch("app.services.HabitoUsuarioService.DiaHabitoMesRepository") as mock_dia_mes_repo:

        mock_user_repo.return_value.buscar_por_id.return_value = mock_usuario()
        mock_habito_base_repo.return_value.buscar_por_id.return_value = mock_habito_base()
        habito_usuario_mock = mock_habito_usuario()
        mock_habito_usuario_repo.return_value.criar_habito_usuario.return_value = habito_usuario_mock

        service = HabitoUsuarioService(db=MagicMock(spec=Session))

        resultado = service.adicionar_habito_usuario(
            descricao="Descricao Teste",
            habito_base_id=10,
            usuario_id=1,
            frequencia="semanal",
            data_inicio=datetime.now(),
            vezes_na_semana=3,
            dias_da_semana=[1, 3, 5]
        )

        assert resultado == habito_usuario_mock
        mock_habito_usuario_repo.return_value.criar_habito_usuario.assert_called_once()
        assert resultado.vezes_na_semana == 3
        assert mock_dia_semana_repo.return_value.adicionar_dia.call_count == 3

def test_adicionar_habito_usuario_data_inicio_obrigatoria():
    with patch("app.services.HabitoUsuarioService.UserRepository") as mock_user_repo, \
         patch("app.services.HabitoUsuarioService.HabitoBaseRepository") as mock_habito_base_repo:

        mock_user_repo.return_value.buscar_por_id.return_value = mock_usuario()
        mock_habito_base_repo.return_value.buscar_por_id.return_value = mock_habito_base()

        service = HabitoUsuarioService(db=MagicMock(spec=Session))

        with pytest.raises(Exception) as e:
            service.adicionar_habito_usuario(
                descricao="Teste",
                habito_base_id=10,
                usuario_id=1,
                frequencia="diario",
                data_inicio=None
            )
        assert "data de início é obrigatória" in str(e.value)

def test_remover_habito_usuario_sucesso():
    with patch("app.services.HabitoUsuarioService.HabitoUsuarioRepository") as mock_habito_usuario_repo:
        mock_habito_usuario_repo.return_value.buscar_por_id.return_value = mock_habito_usuario()

        service = HabitoUsuarioService(db=MagicMock(spec=Session))
        service.remover_habito_usuario(100)

        mock_habito_usuario_repo.return_value.remover_habito_usuario.assert_called_once_with(100)

def test_remover_habito_usuario_nao_encontrado():
    with patch("app.services.HabitoUsuarioService.HabitoUsuarioRepository") as mock_habito_usuario_repo:
        mock_habito_usuario_repo.return_value.buscar_por_id.return_value = None

        service = HabitoUsuarioService(db=MagicMock(spec=Session))

        with pytest.raises(Exception) as e:
            service.remover_habito_usuario(999)
        assert "Hábito de usuário não encontrado" in str(e.value)

def test_buscar_categorias_usuario_sucesso():
    with patch("app.services.HabitoUsuarioService.CategoriaRepository") as mock_categoria_repo:
        mock_categoria_repo.return_value.buscar_categorias_por_usuario.return_value = ["cat1", "cat2"]

        service = HabitoUsuarioService(db=MagicMock(spec=Session))
        resultado = service.buscar_categorias_usuario(1)

        assert resultado == ["cat1", "cat2"]
        mock_categoria_repo.return_value.buscar_categorias_por_usuario.assert_called_once_with(usuario_id=1)

def test_buscar_categorias_usuario_nao_encontradas():
    with patch("app.services.HabitoUsuarioService.CategoriaRepository") as mock_categoria_repo:
        mock_categoria_repo.return_value.buscar_categorias_por_usuario.return_value = None

        service = HabitoUsuarioService(db=MagicMock(spec=Session))

        with pytest.raises(Exception) as e:
            service.buscar_categorias_usuario(1)
        assert "Categorias de hábito não encontradas" in str(e.value)
