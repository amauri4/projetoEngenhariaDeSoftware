from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from app.exceptions.service_exceptions import ServiceError
from app.exceptions.repository_exceptions import RepositoryError, NotFoundError

class ServicoDeItem(ABC):
    def __init__(self, db: Session):
        self.db = db

    def adicionar_item(self, ator_id: int, dados: Dict[str, Any]) -> Any:
        try:
            dados_preparados = self._preparar_dados_adicionar(ator_id, dados)
            novo_item = self._executar_adicao(dados_preparados)
            self._logica_pos_adicionar(novo_item, dados)
            
            return novo_item
        except (NotFoundError, RepositoryError, ServiceError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro inesperado no framework ao adicionar item: {e}") from e

    def atualizar_item(self, item_id: int, dados: Dict[str, Any]) -> Any:
        try:
            dados_preparados = self._preparar_dados_atualizar(item_id, dados)
            item_atualizado = self._executar_atualizacao(item_id, dados_preparados)
            return item_atualizado
        except (NotFoundError, RepositoryError, ServiceError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro inesperado no framework ao atualizar item {item_id}: {e}") from e

    def remover_item(self, item_id: int) -> None:
        try:
            self._executar_remocao(item_id)
        except (NotFoundError, RepositoryError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro inesperado no framework ao remover item {item_id}: {e}") from e

    @abstractmethod
    def _preparar_dados_adicionar(self, ator_id: int, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Hook para validar dados de entrada e prepará-los para o repositório."""
        pass

    @abstractmethod
    def _executar_adicao(self, dados_preparados: Dict[str, Any]) -> Any:
        """Hook que efetivamente chama o método de criação do repositório específico."""
        pass

    def _logica_pos_adicionar(self, novo_item: Any, dados_originais: Dict[str, Any]) -> None:
        """Hook opcional para ações após a criação do item principal."""
        pass

    @abstractmethod
    def _preparar_dados_atualizar(self, item_id: int, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Hook para validar e preparar dados para atualização."""
        pass

    @abstractmethod
    def _executar_atualizacao(self, item_id: int, dados_preparados: Dict[str, Any]) -> Any:
        """Hook que efetivamente chama o método de atualização do repositório."""
        pass

    @abstractmethod
    def _executar_remocao(self, item_id: int) -> None:
        """Hook que efetivamente chama o método de remoção do repositório."""
        pass

    @abstractmethod
    def buscar_por_ator(self, ator_id: int) -> List[Any]:
        """
        Busca por Ator (varia de acordo com a implementacao)
        """
        pass

