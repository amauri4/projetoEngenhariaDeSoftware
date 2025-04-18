from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from database.base import Base

class HabitoUsuario(Base):
    __tablename__ = "habitos"

    id = Column(Integer, primary_key=True)
    descricao = Column(String(255))
    habito_base_id = Column(Integer, ForeignKey('habitos_base.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)  
    
    usuario = relationship("Usuario", back_populates="habitos")
    habito_base = relationship("HabitoBase")
    registros = relationship("RegistroDiario", back_populates="habito", cascade="all, delete-orphan")

    def __repr__(self):
        habito_nome = self.habito_base.nome if self.habito_base else "Desconhecido"
        return f"<HabitoUsuario(id={self.id}, habito_base={habito_nome}, usuario_id={self.usuario_id})>"
