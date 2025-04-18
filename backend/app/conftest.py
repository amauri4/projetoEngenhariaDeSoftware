import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base import Base  
from app.models.HabitoBase import HabitoBase
from app.models.HabitoUsuario import HabitoUsuario
from app.models.Usuario import Usuario
from app.models.CategoriasHabito import CategoriaHabito
from app.models.RegistroDiario import RegistroDiario

# Cria engine com SQLite em memória
@pytest.fixture(scope="function")
def db_engine():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)  
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
