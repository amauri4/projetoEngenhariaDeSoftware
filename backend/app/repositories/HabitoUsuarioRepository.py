from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from models.HabitoUsuario import HabitoUsuario
from models.HabitoBase import HabitoBase
from models.Usuario import Usuario

class HabitoUsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_todos(self):
        try:
            habitos_usuario = self.db.query(HabitoUsuario).all()
            if not habitos_usuario:
                raise NoResultFound("Nenhum hábito de usuário encontrado.")
            return habitos_usuario
        except NoResultFound as e:
            raise Exception(f"Erro ao buscar hábitos de usuário: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar hábitos de usuário: {str(e)}")

    def criar_habito_usuario(self, descricao: str, habito_base_id: int, usuario_id: int):
        try:
            habito_base = self.db.query(HabitoBase).filter_by(id=habito_base_id).first()
            if not habito_base:
                raise NoResultFound("Hábito base não encontrado.")
            usuario = self.db.query(Usuario).filter_by(id=usuario_id).first()
            if not usuario:
                raise NoResultFound("Usuário não encontrado.")
            novo_habito_usuario = HabitoUsuario(descricao=descricao, habito_base_id=habito_base_id, usuario_id=usuario_id)
            self.db.add(novo_habito_usuario)
            self.db.commit()
            return novo_habito_usuario
        except NoResultFound as e:
            raise Exception(f"Erro ao criar hábito de usuário: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao criar hábito de usuário: {str(e)}")

    def atualizar_habito_usuario(self, habito_usuario_id: int, nova_descricao: str, novo_habito_base_id: int, novo_usuario_id: int):
        try:
            habito_usuario = self.db.query(HabitoUsuario).filter_by(id=habito_usuario_id).first()
            if not habito_usuario:
                raise NoResultFound("Hábito de usuário não encontrado.")
            habito_base = self.db.query(HabitoBase).filter_by(id=novo_habito_base_id).first()
            if not habito_base:
                raise NoResultFound("Hábito base não encontrado.")
            usuario = self.db.query(Usuario).filter_by(id=novo_usuario_id).first()
            if not usuario:
                raise NoResultFound("Usuário não encontrado.")
            habito_usuario.descricao = nova_descricao
            habito_usuario.habito_base_id = novo_habito_base_id
            habito_usuario.usuario_id = novo_usuario_id
            self.db.commit()
            return habito_usuario
        except NoResultFound as e:
            raise Exception(f"Erro ao atualizar hábito de usuário: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao atualizar hábito de usuário: {str(e)}")

    def remover_habito_usuario(self, habito_usuario_id: int):
        try:
            habito_usuario = self.db.query(HabitoUsuario).filter_by(id=habito_usuario_id).first()
            if not habito_usuario:
                raise NoResultFound("Hábito de usuário não encontrado.")
            self.db.delete(habito_usuario)
            self.db.commit()
        except NoResultFound as e:
            raise Exception(f"Erro ao remover hábito de usuário: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao remover hábito de usuário: {str(e)}")

    def buscar_por_email(self, email: str):
        try:
            usuario = self.db.query(Usuario).filter_by(email=email).first()
            if not usuario:
                raise NoResultFound("Usuário não encontrado.")
            
            habitos_usuario = self.db.query(HabitoUsuario).filter_by(usuario_id=usuario.id).all()
            if not habitos_usuario:
                raise NoResultFound("Nenhum hábito encontrado para o usuário.")
            
            return habitos_usuario
        except NoResultFound as e:
            raise Exception(f"Erro ao buscar hábitos por e-mail: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar hábitos por e-mail: {str(e)}")
import pytest
from repositories.HabitoUsuarioRepository import HabitoUsuarioRepository
from models.HabitoUsuario import HabitoUsuario
from models.HabitoBase import HabitoBase
from models.Usuario import Usuario

@pytest.fixture
def popular_usuario(db_session):
    usuario = Usuario(nome="João", email="joao@example.com")
    db_session.add(usuario)
    db_session.commit()
    return usuario

@pytest.fixture
def popular_habito_base(db_session):
    habito_base = HabitoBase(nome="Exercício")
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
        repo.buscar_por_email("nao_existe@example.com")  # E-mail inexistente

def test_buscar_por_email_sem_habitos(repo, db_session, popular_usuario):
    db_session.query(HabitoUsuario).delete()
    db_session.commit()

    with pytest.raises(Exception, match="Erro ao buscar hábitos por e-mail: Nenhum hábito encontrado para o usuário."):
        repo.buscar_por_email("joao@example.com")
