from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class HabitoBase(Base):
    __tablename__ = "habitos"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)

    categoria_id = Column(Integer, ForeignKey('categorias_habitos.id'), nullable=False)
    categoria = relationship("CategoriaHabito", back_populates="habitos")
    registros = relationship("RegistroDiario", back_populates="habito")
    
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)  # <- adicionado
    usuario = relationship("Usuario", back_populates="habitos")  # <- adicionado

    def __repr__(self):
        return f"<HabitoBase(id={self.id}, nome={self.nome}, categoria={self.categoria.nome})>"
