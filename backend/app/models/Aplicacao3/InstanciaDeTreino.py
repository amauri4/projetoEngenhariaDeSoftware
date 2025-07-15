from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.models.ItemRastreavel import ItemRastreavel
from app.models.Aplicacao3.Aluno import Aluno
from app.models.Aplicacao3.Instrutor import Instrutor

class InstanciaDeTreino(ItemRastreavel):
    __tablename__ = "instancias_de_treinos"

    id = Column(Integer, ForeignKey('itens_rastreaveis.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'instancia_de_treino'}

    # aluno que deve realizar o treino
    id_aluno_responsavel = Column(Integer, ForeignKey('atores.id'), nullable=False)
    
    # data opcional de entrega, avaliação ou vencimento
    data_entrega = Column(Date, nullable=True)

    # relacionamento de volta para o criador (Instrutor)
    criador = relationship(
        "Instrutor",
        foreign_keys=[ItemRastreavel.ator_id],
        back_populates="treinos_criados",
        overlaps="ator,itens_rastreaveis"
    )

    # relacionamento com o aluno responsável
    responsavel = relationship(
        "Aluno",
        foreign_keys=[id_aluno_responsavel],
        back_populates="treinos_recebidos"
    )
