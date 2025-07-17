import pytest
from unittest.mock import MagicMock, create_autospec
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from app.repositories.Framework.ChatRepository import ChatRepository
from app.models.Framework.HistoricoChat import HistoricoChat


@pytest.fixture
def mock_db():
    return create_autospec(Session)

@pytest.fixture
def repo(mock_db):
    return ChatRepository(db=mock_db)

def test_salvar_mensagem(repo, mock_db):
    mensagem = HistoricoChat(id=1, usuario_id=1, conteudo="Olá")
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    resultado = repo.salvar_mensagem(mensagem)
    assert resultado == mensagem
    mock_db.add.assert_called_once_with(mensagem)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mensagem)

def test_salvar_mensagem_erro(repo, mock_db):
    mensagem = HistoricoChat(id=1, usuario_id=1, conteudo="Olá")
    mock_db.commit.side_effect = SQLAlchemyError("Erro")
    with pytest.raises(Exception, match="Erro ao salvar mensagem"):
        repo.salvar_mensagem(mensagem)
    mock_db.rollback.assert_called_once()

def test_buscar_historico_por_usuario(repo, mock_db):
    mensagem = HistoricoChat(id=1, usuario_id=1, conteudo="Teste")
    mock_db.query().filter().order_by().all.return_value = [mensagem]
    resultado = repo.buscar_historico_por_usuario(1)
    assert resultado == [mensagem]

def test_buscar_historico_vazio(repo, mock_db):
    mock_db.query().filter().order_by().all.return_value = []
    with pytest.raises(Exception, match="Nenhum histórico encontrado"):
        repo.buscar_historico_por_usuario(1)
    mock_db.rollback.assert_called_once()

def test_buscar_ultimas_mensagens(repo, mock_db):
    mensagens = [HistoricoChat(id=i, usuario_id=1, conteudo=f"msg{i}") for i in range(3)]
    mock_db.query().filter().order_by().limit().all.return_value = mensagens[::-1]  # inverte depois
    resultado = repo.buscar_ultimas_mensagens(1, limite=3)
    assert resultado == mensagens

def test_buscar_ultimas_mensagens_vazio(repo, mock_db):
    mock_db.query().filter().order_by().limit().all.return_value = []
    with pytest.raises(Exception, match="Nenhuma mensagem encontrada"):
        repo.buscar_ultimas_mensagens(1)
    mock_db.rollback.assert_called_once()

def test_deletar_historico(repo, mock_db):
    mock_db.query().filter().delete.return_value = 1
    repo.deletar_historico(1)
    mock_db.commit.assert_called_once()

def test_deletar_historico_vazio(repo, mock_db):
    mock_db.query().filter().delete.return_value = 0
    with pytest.raises(Exception, match="Nenhum histórico encontrado para deletar"):
        repo.deletar_historico(1)
    mock_db.rollback.assert_called_once()
