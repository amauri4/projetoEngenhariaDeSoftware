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

def test_criar_habito(repo, popular_dados):
    usuario = popular_dados["usuario"]
    categoria = popular_dados["categoria"]

    novo_habito = repo.criar_habito(
        nome="Meditar",
        descricao="10 minutos ao acordar",
        categoria_id=categoria.id,
        usuario_id=usuario.id
    )

    assert novo_habito.id is not None
    assert novo_habito.nome == "Meditar"
    assert novo_habito.descricao == "10 minutos ao acordar"
    assert novo_habito.usuario_id == usuario.id
    assert novo_habito.categoria_id == categoria.id

def test_atualizar_habito(repo, popular_dados):
    habito = popular_dados["habito"]

    habito_atualizado = repo.atualizar_habito(
        habito_id=habito.id,
        nome="Beber mais água",
        descricao="Beber 3L por dia"
    )

    assert habito_atualizado.nome == "Beber mais água"
    assert habito_atualizado.descricao == "Beber 3L por dia"

def test_deletar_habito(repo, popular_dados):
    habito = popular_dados["habito"]

    deletado = repo.deletar_habito(habito.id)
    assert deletado is True

    habito_checado = repo.buscar_por_id(habito.id)
    assert habito_checado is None

def test_deletar_registro_por_data(repo, db_session, popular_dados):
    habito = popular_dados["habito"]
    data = date(2025, 4, 15)

    resultado = repo.deletar_registro_por_data(habito.id, data)
    assert resultado is True

    registro = db_session.query(RegistroDiario).filter_by(habito_id=habito.id, data=data).first()
    assert registro is None

