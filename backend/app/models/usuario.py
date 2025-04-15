from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.base import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)

    habitos = relationship("HabitoBase", back_populates="usuario", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Usuario(nome={self.nome}, email={self.email})>"
    

