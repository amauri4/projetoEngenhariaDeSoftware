from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base
from .InstanciaDeHabito import InstanciaDeHabito
from .Ator import Ator 

class UsuarioPessoal(Ator):
    __tablename__ = 'usuarios_pessoais' 

    # achave primária também é uma chave estrangeira para a tabela atores
    id = Column(Integer, ForeignKey('atores.id'), primary_key=True)

    @property
    def habitos(self):
        return [item for item in self.itens_rastreaveis if isinstance(item, InstanciaDeHabito)]

    # mapeamento para esta subclasse específica
    __mapper_args__ = {
        'polymorphic_identity': 'usuario_pessoal', 
    }

    def __repr__(self):
        return f"<UsuarioPessoal(nome={self.nome}, email={self.email})>"