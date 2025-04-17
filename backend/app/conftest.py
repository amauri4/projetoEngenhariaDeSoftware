import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.base import Base  
from models.HabitoBase import HabitoBase
from models.Usuario import Usuario
from models.CategoriasHabito import CategoriaHabito
from models.RegistroDiario import RegistroDiario

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
