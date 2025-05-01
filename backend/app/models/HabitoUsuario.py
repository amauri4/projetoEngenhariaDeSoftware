from sqlalchemy import Column, Integer, ForeignKey, String, Enum, Date
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.models.enums.frequencia_enums import FrequenciaEnum

class HabitoUsuario(Base):
    __tablename__ = "habitos"

    id = Column(Integer, primary_key=True)
    descricao = Column(String(255))
    frequencia = Column(Enum(FrequenciaEnum), nullable=False)
    data_inicio = Column(Date, nullable=False)
    vezes_na_semana = Column(Integer, nullable=True)  
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    habito_base_id = Column(Integer, ForeignKey('habitos_base.id'), nullable=False)

    usuario = relationship("Usuario", back_populates="habitos")
    habito_base = relationship("HabitoBase")
    registros = relationship("RegistroDiario", back_populates="habito", cascade="all, delete-orphan")
    dias_semana = relationship("DiaHabitoSemana", back_populates="habito", cascade="all, delete-orphan")
    dias_mes = relationship("DiaHabitoMes", back_populates="habito", cascade="all, delete-orphan")

