from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class DiaHabitoMes(Base):
    __tablename__ = "dias_habito_mes"

    id = Column(Integer, primary_key=True)
    habito_id = Column(Integer, ForeignKey('habitos.id'), nullable=False)
    dia = Column(Integer, nullable=False)  # 1 a 31 (dia do mes)

    habito = relationship("HabitoUsuario", back_populates="dias_mes")
