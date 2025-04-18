from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class HabitoBase(Base):
    __tablename__ = "habitos_base"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    categoria_id = Column(Integer, ForeignKey('categorias_habitos.id'), nullable=False)

    categoria = relationship("CategoriaHabito", back_populates="habitos")

    def __repr__(self):
        categoria_nome = self.categoria.nome if self.categoria else "Sem categoria"
        return f"<HabitoBase(id={self.id}, nome={self.nome}, categoria={categoria_nome})>"
