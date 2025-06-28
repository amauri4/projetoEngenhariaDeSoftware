from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.base import Base
from .ItemRastreavel import ItemRastreavel 
from app.models.enums.frequencia_enums import FrequenciaEnum

class InstanciaDeHabito(ItemRastreavel):
    __tablename__ = "instancias_de_habitos" 

    # chave para a tabela base ItemRastreavel
    id = Column(Integer, ForeignKey('itens_rastreaveis.id'), primary_key=True)
    
    # Campos que são específicos de um Hábito
    frequencia = Column(Enum(FrequenciaEnum), nullable=False)
    vezes_na_semana = Column(Integer, nullable=True)  
    
    # Chave para a "definição" do hábito
    habito_base_id = Column(Integer, ForeignKey('habitos_base.id'), nullable=False)

    # Relacionamentos específicos
    habito_base = relationship("HabitoBase")
    dias_semana = relationship("DiaHabitoSemana", back_populates="habito", cascade="all, delete-orphan")
    dias_mes = relationship("DiaHabitoMes", back_populates="habito", cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'instancia_de_habito',
    }