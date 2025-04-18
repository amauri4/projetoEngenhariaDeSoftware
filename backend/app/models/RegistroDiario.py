from sqlalchemy import Column, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class RegistroDiario(Base):
    __tablename__ = 'registros_diarios'

    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False)
    concluido = Column(Boolean, default=False)
    habito_id = Column(Integer, ForeignKey("habitos.id"), nullable=False)
    
    habito = relationship("HabitoUsuario", back_populates="registros")

    def __repr__(self):
        return f"<Registro(data={self.data}, concluido={self.concluido})>"
