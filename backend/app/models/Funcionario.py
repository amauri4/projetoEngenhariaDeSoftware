from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.models.Ator import Ator

class Funcionario(Ator):
    __tablename__ = 'funcionarios'
    id = Column(Integer, ForeignKey('atores.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'funcionario'}

    chefe_id = Column(Integer, ForeignKey('atores.id'), nullable=True)
    chefe = relationship("Gerente", back_populates="equipe", remote_side=[id])

    # relacionamento para ver as tarefas atribuídas a este funcionário
    tarefas_atribuidas = relationship("InstanciaDeTarefa", foreign_keys="[InstanciaDeTarefa.id_funcionario_responsavel]", back_populates="responsavel")