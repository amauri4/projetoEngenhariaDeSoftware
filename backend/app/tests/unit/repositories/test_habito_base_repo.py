import pytest
from app.repositories.HabitoBaseRepository import HabitoBaseRepository
from app.models.HabitoBase import HabitoBase
from app.models.CategoriasHabito import CategoriaHabito

@pytest.fixture
def popular_categoria(db_session):
    categoria = CategoriaHabito(nome="Saúde")
    db_session.add(categoria)
    db_session.commit()
    return categoria

@pytest.fixture
def popular_habito_base(db_session, popular_categoria):
    habito = HabitoBase(nome="Exercício", categoria_id=popular_categoria.id)
    db_session.add(habito)
    db_session.commit()
    return habito

@pytest.fixture
def repo(db_session):
    return HabitoBaseRepository(db_session)

def test_buscar_todos(repo, db_session, popular_habito_base):
    habitos = repo.buscar_todos()

    assert len(habitos) > 0
    assert habitos[0].nome == "Exercício"
    assert habitos[0].categoria_id == popular_habito_base.categoria_id

def test_criar_habito(repo, db_session, popular_categoria):
    novo_habito = repo.criar_habito("Meditação", popular_categoria.id)

    assert novo_habito.id is not None
    assert novo_habito.nome == "Meditação"
    assert novo_habito.categoria_id == popular_categoria.id

    persistido = db_session.query(HabitoBase).filter_by(nome="Meditação").first()
    assert persistido is not None
    assert persistido.nome == "Meditação"

def test_atualizar_habito(repo, db_session, popular_habito_base, popular_categoria):
    novo_nome = "Caminhada"
    nova_categoria_id = popular_categoria.id
    habito_atualizado = repo.atualizar_habito(popular_habito_base.id, novo_nome, nova_categoria_id)

    assert habito_atualizado.nome == novo_nome
    assert habito_atualizado.categoria_id == nova_categoria_id

    atualizado = db_session.query(HabitoBase).filter_by(id=popular_habito_base.id).first()
    assert atualizado.nome == novo_nome
    assert atualizado.categoria_id == nova_categoria_id

def test_remover_habito(repo, db_session, popular_habito_base):
    repo.remover_habito(popular_habito_base.id)

    removido = db_session.query(HabitoBase).filter_by(id=popular_habito_base.id).first()
    assert removido is None

def test_buscar_todos_sem_habitos(repo, db_session):
    db_session.query(HabitoBase).delete()
    db_session.commit()

    with pytest.raises(Exception, match="Erro ao buscar hábitos: Nenhum hábito encontrado."):
        repo.buscar_todos()

def test_criar_habito_categoria_nao_encontrada(repo, db_session):
    with pytest.raises(Exception, match="Erro ao criar hábito: Categoria não encontrada."):
        repo.criar_habito("Leitura", 999) 

def test_atualizar_habito_habito_nao_encontrado(repo, db_session, popular_categoria):
    with pytest.raises(Exception, match="Erro ao atualizar hábito: Hábito não encontrado."):
        repo.atualizar_habito(999, "Caminhada", popular_categoria.id)

def test_atualizar_habito_categoria_nao_encontrada(repo, db_session, popular_habito_base):
    with pytest.raises(Exception, match="Erro ao atualizar hábito: Categoria não encontrada."):
        repo.atualizar_habito(popular_habito_base.id, "Caminhada", 999)  

def test_remover_habito_nao_encontrado(repo):
    with pytest.raises(Exception, match="Erro ao remover hábito: Hábito não encontrado."):
        repo.remover_habito(999)  
