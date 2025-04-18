import pytest
from repositories.CategoriaRepositories import CategoriaRepository
from models.CategoriasHabito import CategoriaHabito

@pytest.fixture
def repo(db_session):
    return CategoriaRepository(db_session)

@pytest.fixture
def categoria_existente(db_session):
    categoria = CategoriaHabito(nome="Produtividade")
    db_session.add(categoria)
    db_session.commit()
    return categoria

def test_buscar_todas(repo, categoria_existente):
    categorias = repo.buscar_todas()
    assert len(categorias) == 1
    assert categorias[0].nome == "Produtividade"

def test_criar_categoria(repo, db_session):
    nova_categoria = repo.criar_categoria("Saúde")
    assert nova_categoria.id is not None
    assert nova_categoria.nome == "Saúde"

    persistida = db_session.query(CategoriaHabito).filter_by(nome="Saúde").first()
    assert persistida is not None

def test_atualizar_categoria(repo, categoria_existente):
    categoria_atualizada = repo.atualizar_categoria(categoria_existente.id, "Bem-estar")
    assert categoria_atualizada.nome == "Bem-estar"

def test_remover_categoria(repo, db_session, categoria_existente):
    repo.remover_categoria(categoria_existente.id)

    categoria = db_session.query(CategoriaHabito).filter_by(id=categoria_existente.id).first()
    assert categoria is None


