from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from app.models.Framework.Ator import Ator
from app.models.Aplicacao2.Gerente import Gerente
from app.models.Aplicacao2.Funcionario import Funcionario
from app.models.Aplicacao2.InstanciaDeTarefa import InstanciaDeTarefa
from app.exceptions.repository_exceptions import NotFoundError, RepositoryError
from typing import Optional
from datetime import date

class TarefaRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar_tarefa(self, descricao: str, data_inicio: date, criador_id: int, responsavel_id: int, prazo_final: Optional[date] = None) -> InstanciaDeTarefa:
        try:
            criador = self.db.query(Gerente).filter(Gerente.id == criador_id).first()
            if not criador:
                raise NotFoundError(f"Gerente criador com ID {criador_id} não encontrado.")
            
            responsavel = self.db.query(Funcionario).filter(Funcionario.id == responsavel_id).first()
            if not responsavel:
                raise NotFoundError(f"Funcionário responsável com ID {responsavel_id} não encontrado.")

            nova_tarefa = InstanciaDeTarefa(
                descricao=descricao,
                data_inicio=data_inicio,
                ator_id=criador_id,
                id_funcionario_responsavel=responsavel_id,
                prazo_final=prazo_final
            )
            self.db.add(nova_tarefa)
            self.db.commit()
            self.db.refresh(nova_tarefa)
            return nova_tarefa
        except SQLAlchemyError as e:
            print(e)
            self.db.rollback()
            raise RepositoryError("Erro ao criar a tarefa.") from e

    def atualizar_tarefa(self, tarefa_id: int, descricao: Optional[str] = None, responsavel_id: Optional[int] = None, prazo_final: Optional[date] = None) -> InstanciaDeTarefa:
        try:
            tarefa = self.db.query(InstanciaDeTarefa).filter(InstanciaDeTarefa.id == tarefa_id).first()
            if not tarefa:
                raise NotFoundError(f"Tarefa com ID {tarefa_id} não encontrada.")
            
            if descricao is not None:
                tarefa.descricao = descricao
            if prazo_final is not None:
                tarefa.prazo_final = prazo_final
            if responsavel_id is not None:
                responsavel = self.db.query(Funcionario).filter(Funcionario.id == responsavel_id).first()
                if not responsavel:
                    raise NotFoundError(f"Funcionário responsável com ID {responsavel_id} não encontrado.")
                tarefa.id_funcionario_responsavel = responsavel_id

            self.db.commit()
            self.db.refresh(tarefa)
            return tarefa
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao atualizar a tarefa.") from e

    def remover_tarefa(self, tarefa_id: int) -> None:
        try:
            tarefa = self.db.query(InstanciaDeTarefa).filter(InstanciaDeTarefa.id == tarefa_id).first()
            if not tarefa:
                raise NotFoundError(f"Tarefa com ID {tarefa_id} não encontrada.")
            
            self.db.delete(tarefa)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao remover a tarefa.") from e

    def buscar_por_id(self, tarefa_id: int) -> InstanciaDeTarefa:
        try:
            tarefa = self.db.query(InstanciaDeTarefa).filter(InstanciaDeTarefa.id == tarefa_id).first()
            if not tarefa:
                raise NotFoundError(f"Tarefa com ID {tarefa_id} não encontrada.")
            return tarefa
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar tarefa por ID.") from e