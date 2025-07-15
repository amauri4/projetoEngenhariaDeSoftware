from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from app.exceptions.service_exceptions import ServiceError

class IEstrategiaDeInsight(ABC):
    @abstractmethod
    def _buscar_dados_usuairo_insight(self,db:Session, usuario_id: int):
        pass
    
    @abstractmethod
    def _processar_dados_insight(self, dados: List[Dict]):
        pass

    def gerar_insight(self, usuario_id: int):
        try:
            dados = self._buscar_dados_usuairo_insight(usuario_id)
            return self._processar_dados_insight(dados)
        except Exception as e:
            raise ServiceError(f"Erro ao gerar insight de produtividade da equipe: {str(e)}")