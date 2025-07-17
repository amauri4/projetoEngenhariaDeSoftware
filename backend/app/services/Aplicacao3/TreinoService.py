from sqlalchemy.orm import Session
from app.models.Aplicacao3.InstanciaDeTreino import InstanciaDeTreino
from app.repositories.Aplicacao3.TreinoRepository import TreinoRepository
from app.exceptions.service_exceptions import ServiceError
from app.exceptions.repository_exceptions import NotFoundError
from typing import Optional
from datetime import date

class TreinoService:
    _instance = None

    def __new__(cls, db: Session):
        if cls._instance is None:
            cls._instance = super(TreinoService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db: Session):
        if self._initialized:
            return
        self.treino_repository = TreinoRepository(db)
        self._initialized = True

    def criar_treino(self, descricao: str, data_inicio: date, criador_id: int, responsavel_id: int, data_entrega: Optional[date] = None) -> InstanciaDeTreino:
        try:
            novo_treino = self.treino_repository.criar_treino(
                descricao=descricao,
                data_inicio=data_inicio,
                criador_id=criador_id,
                responsavel_id=responsavel_id,
                data_entrega=data_entrega
            )
            return novo_treino
        except Exception as e:
            raise ServiceError(f"Erro inesperado ao criar treino: {str(e)}")

    def atualizar_treino(self, treino_id: int, descricao: Optional[str] = None, responsavel_id: Optional[int] = None, data_entrega: Optional[date] = None) -> InstanciaDeTreino:
        try:
            treino = self.treino_repository.atualizar_treino(
                treino_id=treino_id,
                descricao=descricao,
                responsavel_id=responsavel_id,
                data_entrega=data_entrega
            )
            return treino
        except (NotFoundError, ServiceError):
            raise
        except Exception as e:
            raise ServiceError(f"Erro inesperado ao atualizar treino: {str(e)}")
