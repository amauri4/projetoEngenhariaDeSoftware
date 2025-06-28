from sqlalchemy import Boolean, Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base
from .Ator import Ator

class RegistroDeOcorrencia(Base):
    __tablename__ = 'registros_ocorrencias'

    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False)
    concluido = Column(Boolean, default=False)
    
    item_id = Column(Integer, ForeignKey("itens_rastreaveis.id"), nullable=False)

    item = relationship("ItemRastreavel", back_populates="ocorrencias")

    def __repr__(self):
        return f"<RegistroDeOcorrencia(data={self.data}, status={self.status})>"