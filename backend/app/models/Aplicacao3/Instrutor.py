from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.Ator import Ator

class Instrutor(Ator):
    __tablename__ = 'instrutores'

    id = Column(Integer, ForeignKey('atores.id'), primary_key=True)

    alunos = relationship("Aluno", back_populates="instrutor", foreign_keys="[Aluno.instrutor_id]")

    __mapper_args__ = {
        'polymorphic_identity': 'instrutor',
        'inherit_condition': id == Ator.id
    }

    treinos_criados = relationship("InstanciaDeTreino",foreign_keys="[InstanciaDeTreino.ator_id]",back_populates="criador",overlaps="itens_rastreaveis,ator")