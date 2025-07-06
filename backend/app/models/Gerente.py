from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.models.Ator import Ator

class Gerente(Ator):
    __tablename__ = 'gerentes'
    id = Column(Integer, ForeignKey('atores.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'gerente'}

    equipe = relationship("Funcionario", back_populates="chefe", foreign_keys="[Funcionario.chefe_id]")

    # relacionamento para ver as tarefas criadas por este gerente
    tarefas_criadas = relationship("InstanciaDeTarefa", foreign_keys="[InstanciaDeTarefa.ator_id]", back_populates="criador")