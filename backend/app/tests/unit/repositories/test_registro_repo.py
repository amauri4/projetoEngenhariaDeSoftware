import pytest
from datetime import date
from sqlalchemy.orm import Session

from models.Usuario import Usuario
from models.HabitoBase import HabitoBase
from models.HabitoUsuario import HabitoUsuario
from models.RegistroDiario import RegistroDiario
from repositories.RegistroRepository import RegistroDiarioRepository

@pytest.fixture
def repo(db_session: Session):
    return RegistroDiarioRepository(db=db_session)

@pytest.fixture
def usuario(db_session):
    user = Usuario(nome="João", email="joao@example.com", senha_hash="senha123")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def habito_base(db_session):
    habito = HabitoBase(nome="Dormir cedo", categoria_id=1)
    db_session.add(habito)
    db_session.commit()
    return habito

@pytest.fixture
def usuario_com_registros(db_session, usuario, habito_base):
    habito_usuario = HabitoUsuario(
        descricao="Dormir cedo",
        habito_base_id=habito_base.id,
        usuario_id=usuario.id
    )
    db_session.add(habito_usuario)
    db_session.commit()

    registro1 = RegistroDiario(data=date.today(), concluido=True, habito_id=habito_usuario.id)
    registro2 = RegistroDiario(data=date.today(), concluido=False, habito_id=habito_usuario.id)
    db_session.add_all([registro1, registro2])
    db_session.commit()

    return habito_usuario

def test_buscar_por_usuario(repo, usuario_com_registros):
    registros = repo.buscar_por_usuario(usuario_com_registros.usuario_id)

    assert len(registros) == 2
    assert all(r.habito.usuario_id == usuario_com_registros.usuario_id for r in registros)

def test_buscar_concluidos_por_usuario(repo, usuario_com_registros):
    registros = repo.buscar_concluidos_por_usuario(usuario_com_registros.usuario_id)

    assert len(registros) == 1
    assert registros[0].concluido is True
    assert registros[0].habito.usuario_id == usuario_com_registros.usuario_id

def test_buscar_por_usuario_sem_registros(repo, usuario):
    with pytest.raises(Exception, match="Erro ao buscar registros do usuário: Nenhum registro encontrado para o usuário."):
        repo.buscar_por_usuario(usuario_id=usuario.id)

def test_buscar_concluidos_por_usuario_sem_resultado(repo, db_session, usuario, habito_base):
    habito_usuario = HabitoUsuario(
        descricao="Exercício",
        habito_base_id=habito_base.id,
        usuario_id=usuario.id
    )
    db_session.add(habito_usuario)
    db_session.commit()

    registro = RegistroDiario(data=date.today(), concluido=False, habito_id=habito_usuario.id)
    db_session.add(registro)
    db_session.commit()

    with pytest.raises(Exception, match="Erro ao buscar registros concluídos do usuário: Nenhum registro concluído encontrado para o usuário."):
        repo.buscar_concluidos_por_usuario(usuario_id=usuario.id)
