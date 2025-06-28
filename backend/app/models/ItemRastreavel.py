from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base
from .Ator import Ator

class ItemRastreavel(Base):
    __tablename__ = 'itens_rastreaveis'

    id = Column(Integer, primary_key=True)
    descricao = Column(String(255), nullable=True)
    data_inicio = Column(Date, nullable=False)
    ator_id = Column(Integer, ForeignKey('atores.id'), nullable=False)
    tipo_item = Column(String(50))

    ator = relationship("Ator", back_populates="itens_rastreaveis")
    ocorrencias = relationship("RegistroDeOcorrencia", back_populates="item", cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'item_rastreavel',
        'polymorphic_on': tipo_item
    }