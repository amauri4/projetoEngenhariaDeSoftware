from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from app.models.Ator import Ator
from app.models.Aplicacao2.Gerente import Gerente
from app.models.Aplicacao2.Funcionario import Funcionario
from app.models.Aplicacao2.InstanciaDeTarefa import InstanciaDeTarefa
from app.exceptions.repository_exceptions import NotFoundError, RepositoryError
from typing import Optional

class FuncionarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar_funcionario(self, nome: str, email: str, senha_hash: str, chefe_id: int = None) -> Funcionario:
        try:
            if chefe_id:
                chefe = self.db.query(Gerente).filter(Gerente.id == chefe_id).first()
                if not chefe:
                    raise NotFoundError(f"Gerente (chefe) com ID {chefe_id} não encontrado.")

            novo_funcionario = Funcionario(
                nome=nome,
                email=email,
                senha_hash=senha_hash,
                chefe_id=chefe_id
            )
            self.db.add(novo_funcionario)
            self.db.commit()
            self.db.refresh(novo_funcionario)
            return novo_funcionario
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao criar funcionário.") from e

    def atualizar_funcionario(self, funcionario_id: int, nome: Optional[str] = None, email: Optional[str] = None, chefe_id: Optional[int] = None) -> Funcionario:
        try:
            funcionario = self.db.query(Funcionario).filter(Funcionario.id == funcionario_id).first()
            if not funcionario:
                raise NotFoundError(f"Funcionário com ID {funcionario_id} não encontrado.")

            if nome is not None:
                funcionario.nome = nome
            if email is not None:
                funcionario.email = email
            if chefe_id is not None:
                chefe = self.db.query(Gerente).filter(Gerente.id == chefe_id).first()
                if not chefe:
                    raise NotFoundError(f"Gerente (chefe) com ID {chefe_id} não encontrado para atribuição.")
                funcionario.chefe_id = chefe_id

            self.db.commit()
            self.db.refresh(funcionario)
            return funcionario
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao atualizar funcionário.") from e

    def remover_funcionario(self, funcionario_id: int) -> None:
        try:
            funcionario = self.db.query(Funcionario).filter(Funcionario.id == funcionario_id).first()
            if not funcionario:
                raise NotFoundError(f"Funcionário com ID {funcionario_id} não encontrado.")
            
            self.db.delete(funcionario)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao remover funcionário.") from e

    def buscar_tarefas_atribuidas_ao_funcionario(self, funcionario_id: int) -> list[InstanciaDeTarefa]:
        try:
            funcionario = self.db.query(Funcionario).filter(Funcionario.id == funcionario_id).first()
            if not funcionario:
                raise NotFoundError(f"Funcionário com ID {funcionario_id} não encontrado.")
            return funcionario.tarefas_atribuidas
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar tarefas do funcionário.") from e