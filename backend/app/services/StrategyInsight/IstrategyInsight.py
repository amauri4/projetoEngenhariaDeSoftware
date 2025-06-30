from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from typing import Dict, Any, List

class IEstrategiaDeInsight(ABC):
    @abstractmethod
    def _buscar_dados_usuairo_insight(self,db:Session, usuario_id: int):
        pass
    
    @abstractmethod
    def _processar_dados_insight(self, dados: List[Dict]):
        pass

    @abstractmethod
    def gerar_insight(self, db: Session, usuairo_id: int):
        pass