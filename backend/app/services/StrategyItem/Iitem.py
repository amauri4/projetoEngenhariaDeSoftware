from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from typing import Dict, Any, List

class IEstrategiaDeItem(ABC):
    @abstractmethod
    def adicionar(self, db: Session, ator_id: int, dados: Dict[str, Any]):
        pass

    @abstractmethod
    def atualizar(self, db: Session, item_id: int, dados: Dict[str, Any]):
        pass

    @abstractmethod
    def remover(self, db: Session, item_id: int):
        pass
        
    @abstractmethod
    def buscar_por_ator(self, db: Session, ator_id: int) -> List[Any]:
        pass