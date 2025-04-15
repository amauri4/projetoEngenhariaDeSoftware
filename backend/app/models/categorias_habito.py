from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.base import Base

class CategoriaHabito(Base):
    __tablename__ = 'categorias_habitos'

    id = Column(Integer, primary_key=True)
    nome = Column(String, unique=True, nullable=False)

    habitos = relationship("HabitoBase", back_populates="categoria")

    def __repr__(self):
        return f"<CategoriaHabito(id={self.id}, nome={self.nome})>"
