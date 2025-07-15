from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.Aplicacao3.Instrutor import Instrutor
from app.models.Aplicacao3.Aluno import Aluno
from app.models.Aplicacao3.InstanciaDeTreino import InstanciaDeTreino
from app.exceptions.repository_exceptions import NotFoundError, RepositoryError
from typing import Optional


class AlunoRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar_aluno(self, nome: str, email: str, senha_hash: str, instrutor_id: int = None) -> Aluno:
        try:
            if instrutor_id:
                instrutor = self.db.query(Instrutor).filter(Instrutor.id == instrutor_id).first()
                if not instrutor:
                    raise NotFoundError(f"Instrutor com ID {instrutor_id} não encontrado.")

            novo_aluno = Aluno(
                nome=nome,
                email=email,
                senha_hash=senha_hash,
                instrutor_id=instrutor_id
            )
            self.db.add(novo_aluno)
            self.db.commit()
            self.db.refresh(novo_aluno)
            return novo_aluno
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao criar aluno.") from e

    def atualizar_aluno(self, aluno_id: int, nome: Optional[str] = None, email: Optional[str] = None, instrutor_id: Optional[int] = None) -> Aluno:
        try:
            aluno = self.db.query(Aluno).filter(Aluno.id == aluno_id).first()
            if not aluno:
                raise NotFoundError(f"Aluno com ID {aluno_id} não encontrado.")

            if nome is not None:
                aluno.nome = nome
            if email is not None:
                aluno.email = email
            if instrutor_id is not None:
                instrutor = self.db.query(Instrutor).filter(Instrutor.id == instrutor_id).first()
                if not instrutor:
                    raise NotFoundError(f"Instrutor com ID {instrutor_id} não encontrado para atribuição.")
                aluno.instrutor_id = instrutor_id

            self.db.commit()
            self.db.refresh(aluno)
            return aluno
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao atualizar aluno.") from e

    def remover_aluno(self, aluno_id: int) -> None:
        try:
            aluno = self.db.query(Aluno).filter(Aluno.id == aluno_id).first()
            if not aluno:
                raise NotFoundError(f"Aluno com ID {aluno_id} não encontrado.")
            
            self.db.delete(aluno)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao remover aluno.") from e

    def buscar_treinos_atribuidos_ao_aluno(self, aluno_id: int) -> list[InstanciaDeTreino]:
        try:
            aluno = self.db.query(Aluno).filter(Aluno.id == aluno_id).first()
            if not aluno:
                raise NotFoundError(f"Aluno com ID {aluno_id} não encontrado.")
            return aluno.treinos_atribuidos
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar treinos do aluno.") from e
