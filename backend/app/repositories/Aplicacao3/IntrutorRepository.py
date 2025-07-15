from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.Aplicacao3.Instrutor import Instrutor
from app.models.Aplicacao3.Aluno import Aluno
from app.models.Aplicacao3.InstanciaDeTreino import InstanciaDeTreino
from app.exceptions.repository_exceptions import NotFoundError, RepositoryError
from typing import Optional


class InstrutorRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar_instrutor(self, nome: str, email: str, senha_hash: str) -> Instrutor:
        try:
            novo_instrutor = Instrutor(nome=nome, email=email, senha_hash=senha_hash)
            self.db.add(novo_instrutor)
            self.db.commit()
            self.db.refresh(novo_instrutor)
            return novo_instrutor
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao criar instrutor.") from e

    def atualizar_instrutor(self, instrutor_id: int, nome: Optional[str] = None, email: Optional[str] = None) -> Instrutor:
        try:
            instrutor = self.db.query(Instrutor).filter(Instrutor.id == instrutor_id).first()
            if not instrutor:
                raise NotFoundError(f"Instrutor com ID {instrutor_id} não encontrado.")
            
            if nome is not None:
                instrutor.nome = nome
            if email is not None:
                instrutor.email = email

            self.db.commit()
            self.db.refresh(instrutor)
            return instrutor
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao atualizar instrutor.") from e

    def remover_instrutor(self, instrutor_id: int) -> None:
        try:
            instrutor = self.db.query(Instrutor).filter(Instrutor.id == instrutor_id).first()
            if not instrutor:
                raise NotFoundError(f"Instrutor com ID {instrutor_id} não encontrado.")
            
            self.db.delete(instrutor)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao remover instrutor.") from e

    def buscar_alunos_por_instrutor(self, instrutor_id: int) -> list[Aluno]:
        try:
            instrutor = self.db.query(Instrutor).filter(Instrutor.id == instrutor_id).first()
            if not instrutor:
                raise NotFoundError(f"Instrutor com ID {instrutor_id} não encontrado.")
            return instrutor.alunos
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar alunos do instrutor.") from e

    def buscar_treinos_criados_por_instrutor(self, instrutor_id: int) -> list[InstanciaDeTreino]:
        try:
            instrutor = self.db.query(Instrutor).filter(Instrutor.id == instrutor_id).first()
            if not instrutor:
                raise NotFoundError(f"Instrutor com ID {instrutor_id} não encontrado.")
            return instrutor.treinos_criados
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar treinos criados pelo instrutor.") from e

    def buscar_por_id(self, instrutor_id: int) -> Optional[Instrutor]:
        try:
            return self.db.query(Instrutor).filter(Instrutor.id == instrutor_id).first()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar instrutor por ID.") from e
