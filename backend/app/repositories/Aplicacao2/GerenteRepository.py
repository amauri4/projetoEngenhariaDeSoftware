from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from app.models.Ator import Ator
from app.models.Aplicacao2.Gerente import Gerente
from app.models.Aplicacao2.Funcionario import Funcionario
from app.models.Aplicacao2.InstanciaDeTarefa import InstanciaDeTarefa
from app.exceptions.repository_exceptions import NotFoundError, RepositoryError
from typing import Optional

class GerenteRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar_gerente(self, nome: str, email: str, senha_hash: str) -> Gerente:
        try:
            novo_gerente = Gerente(nome=nome, email=email, senha_hash=senha_hash)
            self.db.add(novo_gerente)
            self.db.commit()
            self.db.refresh(novo_gerente)
            return novo_gerente
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao criar gerente.") from e

    def atualizar_gerente(self, gerente_id: int, nome: Optional[str] = None, email: Optional[str] = None) -> Gerente:
        try:
            gerente = self.db.query(Gerente).filter(Gerente.id == gerente_id).first()
            if not gerente:
                raise NotFoundError(f"Gerente com ID {gerente_id} não encontrado.")
            
            if nome is not None:
                gerente.nome = nome
            if email is not None:
                gerente.email = email

            self.db.commit()
            self.db.refresh(gerente)
            return gerente
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao atualizar gerente.") from e

    def remover_gerente(self, gerente_id: int) -> None:
        try:
            gerente = self.db.query(Gerente).filter(Gerente.id == gerente_id).first()
            if not gerente:
                raise NotFoundError(f"Gerente com ID {gerente_id} não encontrado.")
            
            self.db.delete(gerente)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao remover gerente.") from e

    def buscar_equipe_por_gerente(self, gerente_id: int) -> list[Funcionario]:
        try:
            gerente = self.db.query(Gerente).filter(Gerente.id == gerente_id).first()
            if not gerente:
                raise NotFoundError(f"Gerente com ID {gerente_id} não encontrado.")
            return gerente.equipe
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar a equipe do gerente.") from e
            
    def buscar_tarefas_criadas_por_gerente(self, gerente_id: int) -> list[InstanciaDeTarefa]:
        try:
            gerente = self.db.query(Gerente).filter(Gerente.id == gerente_id).first()
            if not gerente:
                raise NotFoundError(f"Gerente com ID {gerente_id} não encontrado.")
            return gerente.tarefas_criadas
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar tarefas criadas pelo gerente.") from e