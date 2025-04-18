import pytest
from repositories.CategoriaRepository import CategoriaRepository
from models.CategoriasHabito import CategoriaHabito
from sqlalchemy.orm import Session

@pytest.fixture
def popular_categoria(db_session):
    categoria = CategoriaHabito(nome="Saúde")
    db_session.add(categoria)
    db_session.commit()
    return categoria

@pytest.fixture
def repo(db_session):
    return CategoriaRepository(db=db_session)

def test_buscar_todas(repo, db_session, popular_categoria):
    categorias = repo.buscar_todas()

    assert len(categorias) > 0
    assert categorias[0].nome == "Saúde"

def test_criar_categoria(repo, db_session):
    nova_categoria = repo.criar_categoria("Bem-estar")

    assert nova_categoria.id is not None
    assert nova_categoria.nome == "Bem-estar"

    persistida = db_session.query(CategoriaHabito).filter_by(nome="Bem-estar").first()
    assert persistida is not None
    assert persistida.nome == "Bem-estar"

def test_atualizar_categoria(repo, db_session, popular_categoria):
    novo_nome = "Saúde Mental"
    categoria_atualizada = repo.atualizar_categoria(popular_categoria.id, novo_nome)

    assert categoria_atualizada.nome == novo_nome

    atualizado = db_session.query(CategoriaHabito).filter_by(id=popular_categoria.id).first()
    assert atualizado.nome == novo_nome

def test_remover_categoria(repo, db_session, popular_categoria):
    repo.remover_categoria(popular_categoria.id)

    removida = db_session.query(CategoriaHabito).filter_by(id=popular_categoria.id).first()
    assert removida is None

def test_buscar_todas_sem_categorias(repo, db_session):
    db_session.query(CategoriaHabito).delete()
    db_session.commit()

    with pytest.raises(Exception, match="Erro ao buscar categorias de hábito: Nenhuma categoria de hábito encontrada."):
        repo.buscar_todas()

def test_atualizar_categoria_nao_encontrada(repo, db_session):
    with pytest.raises(Exception, match="Erro ao atualizar categoria de hábito: Categoria não encontrada."):
        repo.atualizar_categoria(999, "Categoria Não Encontrada")

def test_remover_categoria_nao_encontrada(repo):
    with pytest.raises(Exception, match="Erro ao remover categoria de hábito: Categoria não encontrada."):
        repo.remover_categoria(999)
