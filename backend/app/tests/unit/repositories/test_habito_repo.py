import pytest
from datetime import date
from repositories.HabitoRepositories import HabitoRepository
from models.HabitoBase import HabitoBase
from models.Usuario import Usuario
from models.RegistroDiario import RegistroDiario
from models.CategoriasHabito import CategoriaHabito

@pytest.fixture
def popular_dados(db_session):
    usuario = Usuario(nome="Usuário Teste", email="teste@email.com", senha_hash="123")
    categoria = CategoriaHabito(nome="Saúde")
    habito = HabitoBase(
        nome="Beber Água",
        descricao="Beber 2L por dia",
        categoria=categoria,
        usuario=usuario
    )
    registro = RegistroDiario(data=date(2025, 4, 15), concluido=True, habito=habito)

    db_session.add_all([usuario, categoria, habito, registro])
    db_session.commit()
    return {
        "usuario": usuario,
        "categoria": categoria,
        "habito": habito,
        "registro": registro
    }

@pytest.fixture
def repo(db_session):
    return HabitoRepository(db_session)

def test_buscar_por_email(repo, popular_dados):
    resultados = repo.buscar_por_email("teste@email.com")
    assert len(resultados) == 1
    assert resultados[0].nome == "Beber Água"

def test_buscar_por_categoria(repo, popular_dados):
    resultados = repo.buscar_por_categoria("Saúde")
    assert len(resultados) == 1
    assert resultados[0].categoria.nome == "Saúde"

def test_buscar_por_data(repo, popular_dados):
    resultados = repo.buscar_por_data(date(2025, 4, 15))
    assert len(resultados) == 1
    assert resultados[0].nome == "Beber Água"

def test_buscar_por_email_e_data(repo, popular_dados):
    resultados = repo.buscar_por_email_e_data("teste@email.com", date(2025, 4, 15))
    assert len(resultados) == 1
    assert resultados[0].nome == "Beber Água"

def test_buscar_por_email_e_categoria(repo, popular_dados):
    resultados = repo.buscar_por_email_e_categoria("teste@email.com", "Saúde")
    assert len(resultados) == 1
    assert resultados[0].nome == "Beber Água"

def test_buscar_completo(repo, popular_dados):
    resultados = repo.buscar_completo("teste@email.com", "Saúde", date(2025, 4, 15))
    assert len(resultados) == 1
    assert resultados[0].nome == "Beber Água"
