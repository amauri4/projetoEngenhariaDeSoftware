from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class Ator(Base):
    __tablename__ = 'atores'  

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    
    # diz ao SQLAlchemy qual tipo de ator cada linha é
    tipo_ator = Column(String(50))

    itens_rastreaveis = relationship("ItemRastreavel", back_populates="ator")
    conversas = relationship("HistoricoChat", back_populates="ator", cascade="all, delete-orphan")

    # herança
    __mapper_args__ = {
        'polymorphic_identity': 'ator',  
        'polymorphic_on': tipo_ator     
    }

    def __repr__(self):
        return f"<Ator(id={self.id}, nome={self.nome}, tipo={self.tipo_ator})>"