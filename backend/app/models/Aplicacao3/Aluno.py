from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.Framework.Ator import Ator

class Aluno(Ator):
    __tablename__ = 'alunos'

    id = Column(Integer, ForeignKey('atores.id'), primary_key=True)
    instrutor_id = Column(Integer, ForeignKey('instrutores.id'), nullable=True)

    instrutor = relationship("Instrutor", back_populates="alunos", foreign_keys=[instrutor_id])

    __mapper_args__ = {
        'polymorphic_identity': 'aluno',
        'inherit_condition': id == Ator.id
    }

    treinos_recebidos = relationship("InstanciaDeTreino",foreign_keys="[InstanciaDeTreino.id_aluno_responsavel]",back_populates="responsavel")