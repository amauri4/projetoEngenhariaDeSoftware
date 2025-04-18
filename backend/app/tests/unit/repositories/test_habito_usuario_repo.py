import pytest
from repositories.HabitoUsuarioRepository import HabitoUsuarioRepository
from models.HabitoUsuario import HabitoUsuario
from models.HabitoBase import HabitoBase
from models.CategoriasHabito import CategoriaHabito
from models.Usuario import Usuario

@pytest.fixture
def popular_usuario(db_session):
    usuario = Usuario(nome="João", email="joao@example.com", senha_hash="senha123")
    db_session.add(usuario)
    db_session.commit()
    return usuario

@pytest.fixture
def popular_categoria(db_session):
    categoria = CategoriaHabito(nome="Saúde")
    db_session.add(categoria)
    db_session.commit()
    return categoria

@pytest.fixture
def popular_habito_base(db_session, popular_categoria):
    habito_base = HabitoBase(nome="Exercício", categoria_id=popular_categoria.id)
    db_session.add(habito_base)
    db_session.commit()
    return habito_base

@pytest.fixture
def popular_habito_usuario(db_session, popular_usuario, popular_habito_base):
    habito_usuario = HabitoUsuario(descricao="Caminhada diária", habito_base_id=popular_habito_base.id, usuario_id=popular_usuario.id)
    db_session.add(habito_usuario)
    db_session.commit()
    return habito_usuario

@pytest.fixture
def repo(db_session):
    return HabitoUsuarioRepository(db_session)

def test_buscar_todos(repo, db_session, popular_habito_usuario):
    habitos_usuario = repo.buscar_todos()

    assert len(habitos_usuario) > 0
    assert habitos_usuario[0].descricao == "Caminhada diária"
    assert habitos_usuario[0].usuario_id == popular_habito_usuario.usuario_id

def test_criar_habito_usuario(repo, db_session, popular_usuario, popular_habito_base):
    novo_habito_usuario = repo.criar_habito_usuario("Leitura diária", popular_habito_base.id, popular_usuario.id)

    assert novo_habito_usuario.id is not None
    assert novo_habito_usuario.descricao == "Leitura diária"
    assert novo_habito_usuario.habito_base_id == popular_habito_base.id
    assert novo_habito_usuario.usuario_id == popular_usuario.id

    persistido = db_session.query(HabitoUsuario).filter_by(descricao="Leitura diária").first()
    assert persistido is not None
    assert persistido.descricao == "Leitura diária"

def test_atualizar_habito_usuario(repo, db_session, popular_habito_usuario, popular_habito_base, popular_usuario):
    nova_descricao = "Caminhada matinal"
    novo_habito_base_id = popular_habito_base.id
    novo_usuario_id = popular_usuario.id
    habito_usuario_atualizado = repo.atualizar_habito_usuario(popular_habito_usuario.id, nova_descricao, novo_habito_base_id, novo_usuario_id)

    assert habito_usuario_atualizado.descricao == nova_descricao
    assert habito_usuario_atualizado.habito_base_id == novo_habito_base_id
    assert habito_usuario_atualizado.usuario_id == novo_usuario_id

    atualizado = db_session.query(HabitoUsuario).filter_by(id=popular_habito_usuario.id).first()
    assert atualizado.descricao == nova_descricao
    assert atualizado.habito_base_id == novo_habito_base_id
    assert atualizado.usuario_id == novo_usuario_id

def test_remover_habito_usuario(repo, db_session, popular_habito_usuario):
    repo.remover_habito_usuario(popular_habito_usuario.id)

    removido = db_session.query(HabitoUsuario).filter_by(id=popular_habito_usuario.id).first()
    assert removido is None

def test_buscar_todos_sem_habitos(repo, db_session):
    db_session.query(HabitoUsuario).delete()
    db_session.commit()

    with pytest.raises(Exception, match="Erro ao buscar hábitos de usuário: Nenhum hábito de usuário encontrado."):
        repo.buscar_todos()

def test_criar_habito_usuario_habito_base_nao_encontrado(repo, db_session, popular_usuario):
    with pytest.raises(Exception, match="Erro ao criar hábito de usuário: Hábito base não encontrado."):
        repo.criar_habito_usuario("Leitura diária", 999, popular_usuario.id)  # Hábito base ID inexistente

def test_criar_habito_usuario_usuario_nao_encontrado(repo, db_session, popular_habito_base):
    with pytest.raises(Exception, match="Erro ao criar hábito de usuário: Usuário não encontrado."):
        repo.criar_habito_usuario("Leitura diária", popular_habito_base.id, 999)  # Usuário ID inexistente

def test_atualizar_habito_usuario_habito_usuario_nao_encontrado(repo, db_session, popular_habito_base, popular_usuario):
    with pytest.raises(Exception, match="Erro ao atualizar hábito de usuário: Hábito de usuário não encontrado."):
        repo.atualizar_habito_usuario(999, "Caminhada diária", popular_habito_base.id, popular_usuario.id)

def test_atualizar_habito_usuario_habito_base_nao_encontrado(repo, db_session, popular_habito_usuario, popular_usuario):
    with pytest.raises(Exception, match="Erro ao atualizar hábito de usuário: Hábito base não encontrado."):
        repo.atualizar_habito_usuario(popular_habito_usuario.id, "Caminhada diária", 999, popular_usuario.id)

def test_atualizar_habito_usuario_usuario_nao_encontrado(repo, db_session, popular_habito_usuario, popular_habito_base):
    with pytest.raises(Exception, match="Erro ao atualizar hábito de usuário: Usuário não encontrado."):
        repo.atualizar_habito_usuario(popular_habito_usuario.id, "Caminhada diária", popular_habito_base.id, 999)

def test_remover_habito_usuario_nao_encontrado(repo):
    with pytest.raises(Exception, match="Erro ao remover hábito de usuário: Hábito de usuário não encontrado."):
        repo.remover_habito_usuario(999)  # Hábito de usuário ID inexistente

def test_buscar_por_email(repo, db_session, popular_usuario, popular_habito_usuario):
    habitos_usuario = repo.buscar_por_email("joao@example.com")

    assert len(habitos_usuario) > 0
    assert habitos_usuario[0].descricao == "Caminhada diária"
    assert habitos_usuario[0].usuario_id == popular_usuario.id

def test_buscar_por_email_usuario_nao_encontrado(repo, db_session):
    with pytest.raises(Exception, match="Erro ao buscar hábitos por e-mail: Usuário não encontrado."):
        repo.buscar_por_email("nao_existe@example.com")  

def test_buscar_por_email_sem_habitos(repo, db_session, popular_usuario):
    db_session.query(HabitoUsuario).delete()
    db_session.commit()

    with pytest.raises(Exception, match="Erro ao buscar hábitos por e-mail: Nenhum hábito encontrado para o usuário."):
        repo.buscar_por_email("joao@example.com")
