import pytest
from unittest.mock import MagicMock, create_autospec
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from app.repositories.CategoriaRepository import CategoriaRepository
from app.models.CategoriasHabito import CategoriaHabito
from app.models.HabitoUsuario import HabitoUsuario
from app.models.HabitoBase import HabitoBase

# ----- FIXTURE: Cria uma instância com mock do banco -----
@pytest.fixture
def mock_db():
    return create_autospec(Session)

@pytest.fixture
def repo(mock_db):
    return CategoriaRepository(db=mock_db)

# ----- TESTE: buscar_todas -----
def test_buscar_todas_categorias(repo, mock_db):
    mock_db.query().all.return_value = [CategoriaHabito(nome="Saúde")]
    categorias = repo.buscar_todas()
    assert len(categorias) == 1
    assert categorias[0].nome == "Saúde"

def test_buscar_todas_sem_resultado(repo, mock_db):
    mock_db.query().all.return_value = []
    with pytest.raises(Exception, match="Nenhuma categoria de hábito encontrada"):
        repo.buscar_todas()

# ----- TESTE: criar_categoria -----
def test_criar_categoria(repo, mock_db):
    mock_db.commit.return_value = None
    nome = "Educação"
    categoria = repo.criar_categoria(nome)
    assert categoria.nome == nome
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

def test_criar_categoria_erro_commit(repo, mock_db):
    mock_db.commit.side_effect = SQLAlchemyError("Erro de commit")
    with pytest.raises(Exception, match="Erro ao criar categoria de hábito"):
        repo.criar_categoria("Financeiro")
    mock_db.rollback.assert_called_once()

# ----- TESTE: atualizar_categoria -----
def test_atualizar_categoria(repo, mock_db):
    categoria_mock = CategoriaHabito(id=1, nome="Antigo")
    mock_db.query().filter_by().first.return_value = categoria_mock

    categoria_atualizada = repo.atualizar_categoria(1, "Novo")
    assert categoria_atualizada.nome == "Novo"
    mock_db.commit.assert_called_once()

def test_atualizar_categoria_nao_encontrada(repo, mock_db):
    mock_db.query().filter_by().first.return_value = None
    with pytest.raises(Exception, match="Categoria não encontrada"):
        repo.atualizar_categoria(99, "Teste")

# ----- TESTE: remover_categoria -----
def test_remover_categoria(repo, mock_db):
    categoria_mock = CategoriaHabito(id=1, nome="Remover")
    mock_db.query().filter_by().first.return_value = categoria_mock

    repo.remover_categoria(1)
    mock_db.delete.assert_called_once_with(categoria_mock)
    mock_db.commit.assert_called_once()

def test_remover_categoria_nao_encontrada(repo, mock_db):
    mock_db.query().filter_by().first.return_value = None
    with pytest.raises(Exception, match="Categoria não encontrada"):
        repo.remover_categoria(42)

# ----- TESTE: buscar_categorias_por_usuario -----
def test_buscar_categorias_por_usuario(repo, mock_db):
    mock_db.query().filter().group_by().all.return_value = [('Saúde', 3)]
    # encadeamento de chamadas no SQLAlchemy precisa ser simulado:
    mock_db.query().select_from().join().join().filter().group_by().all.return_value = [('Saúde', 3)]
    resultado = repo.buscar_categorias_por_usuario(1)
    assert resultado == {'Saúde': 3}

def test_buscar_categorias_usuario_id_invalido(repo):
    with pytest.raises(Exception, match="ID do usuário inválido"):
        repo.buscar_categorias_por_usuario(-5)
