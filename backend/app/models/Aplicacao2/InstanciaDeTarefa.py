from app.models.Framework.ItemRastreavel import ItemRastreavel
from app.models.Aplicacao2.Gerente import Gerente
from app.models.Aplicacao2.Funcionario import Funcionario
from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship

class InstanciaDeTarefa(ItemRastreavel):
    __tablename__ = "instancias_de_tarefas"
    id = Column(Integer, ForeignKey('itens_rastreaveis.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'instancia_de_tarefa'}

    # campo específico para o responsável
    id_funcionario_responsavel = Column(Integer, ForeignKey('atores.id'), nullable=False)
    prazo_final = Column(Date, nullable=True)

    # relacionamento de volta para o criador (Gerente)
    criador = relationship("Gerente", foreign_keys=[ItemRastreavel.ator_id], back_populates="tarefas_criadas", overlaps="ator,itens_rastreaveis")

    # relacionamento de volta para o responsável (Funcionário)
    responsavel = relationship("Funcionario", foreign_keys=[id_funcionario_responsavel], back_populates="tarefas_atribuidas")