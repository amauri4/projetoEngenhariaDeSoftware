from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.base import Base
import enum

class DiaSemanaEnum(enum.Enum):
    segunda = "segunda"
    terca = "terca"
    quarta = "quarta"
    quinta = "quinta"
    sexta = "sexta"
    sabado = "sabado"
    domingo = "domingo"

class DiaHabitoSemana(Base):
    __tablename__ = "dias_habito_semana"

    id = Column(Integer, primary_key=True)
    habito_id = Column(Integer, ForeignKey('instancias_de_habitos.id'), nullable=False)
    dia = Column(Enum(DiaSemanaEnum), nullable=False)  

    habito = relationship("InstanciaDeHabito", back_populates="dias_semana")
