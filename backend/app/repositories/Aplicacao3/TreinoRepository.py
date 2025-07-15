from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.Aplicacao3.Instrutor import Instrutor
from app.models.Aplicacao3.Aluno import Aluno
from app.models.Aplicacao3.InstanciaDeTreino import InstanciaDeTreino
from app.exceptions.repository_exceptions import NotFoundError, RepositoryError
from typing import Optional
from datetime import date

class TreinoRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar_treino(self, descricao: str, data_inicio: date, criador_id: int, responsavel_id: int, data_entrega: Optional[date] = None) -> InstanciaDeTreino:
        try:
            criador = self.db.query(Instrutor).filter(Instrutor.id == criador_id).first()
            if not criador:
                raise NotFoundError(f"Instrutor com ID {criador_id} não encontrado.")
            
            responsavel = self.db.query(Aluno).filter(Aluno.id == responsavel_id).first()
            if not responsavel:
                raise NotFoundError(f"Aluno com ID {responsavel_id} não encontrado.")

            novo_treino = InstanciaDeTreino(
                descricao=descricao,
                data_inicio=data_inicio,
                ator_id=criador_id,
                id_aluno_responsavel=responsavel_id,
                data_entrega=data_entrega
            )
            self.db.add(novo_treino)
            self.db.commit()
            self.db.refresh(novo_treino)
            return novo_treino
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao criar o treino.") from e

    def atualizar_treino(self, treino_id: int, descricao: Optional[str] = None, responsavel_id: Optional[int] = None, data_entrega: Optional[date] = None) -> InstanciaDeTreino:
        try:
            treino = self.db.query(InstanciaDeTreino).filter(InstanciaDeTreino.id == treino_id).first()
            if not treino:
                raise NotFoundError(f"Treino com ID {treino_id} não encontrado.")
            
            if descricao is not None:
                treino.descricao = descricao
            if data_entrega is not None:
                treino.data_entrega = data_entrega
            if responsavel_id is not None:
                responsavel = self.db.query(Aluno).filter(Aluno.id == responsavel_id).first()
                if not responsavel:
                    raise NotFoundError(f"Aluno com ID {responsavel_id} não encontrado.")
                treino.id_aluno_responsavel = responsavel_id

            self.db.commit()
            self.db.refresh(treino)
            return treino
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao atualizar o treino.") from e

    def remover_treino(self, treino_id: int) -> None:
        try:
            treino = self.db.query(InstanciaDeTreino).filter(InstanciaDeTreino.id == treino_id).first()
            if not treino:
                raise NotFoundError(f"Treino com ID {treino_id} não encontrado.")
            self.db.delete(treino)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao remover o treino.") from e

    def buscar_por_id(self, treino_id: int) -> InstanciaDeTreino:
        try:
            treino = self.db.query(InstanciaDeTreino).filter(InstanciaDeTreino.id == treino_id).first()
            if not treino:
                raise NotFoundError(f"Treino com ID {treino_id} não encontrado.")
            return treino
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar treino por ID.") from e
