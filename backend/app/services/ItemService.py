from sqlalchemy.orm import Session
from app.services.StrategyItem.Iitem import IEstrategiaDeItem
from app.exceptions.service_exceptions import ServiceError
from typing import Dict, Any

class ServicoDeItem:
    def __init__(self, db: Session):
        self.db = db

    def adicionar(self, ator_id: int, dados: Dict[str, Any], estrategia: IEstrategiaDeItem):
        try:
            novo_item = estrategia.adicionar(ator_id, dados)
            return novo_item
        except Exception as e:
            raise ServiceError(f"Erro ao adicionar item: {e}") from e

    def atualizar(self, item_id: int, dados: Dict[str, Any], estrategia: IEstrategiaDeItem):
        try:
            item_atualizado = estrategia.atualizar(item_id, dados)
            return item_atualizado
        except Exception as e:
            raise ServiceError(f"Erro ao atualizar item: {e}") from e

    def remover(self, item_id: int, estrategia: IEstrategiaDeItem):
        try:
            estrategia.remover(item_id)
            self.db.commit()
            return True
        except Exception as e:
            raise ServiceError(f"Erro ao remover item: {e}") from e
            
    def buscar_por_ator(self, ator_id: int, estrategia: IEstrategiaDeItem):
        try:
            return estrategia.buscar_por_ator(ator_id)
        except Exception as e:
            raise ServiceError(f"Erro ao buscar itens: {e}") from e