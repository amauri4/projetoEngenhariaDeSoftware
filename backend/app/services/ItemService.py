from sqlalchemy.orm import Session
from typing import Dict, Any, Type
from app.services.TemplateMethodItem.ServicoDeItem import ServicoDeItem
from app.exceptions.service_exceptions import ServiceError
from app.exceptions.repository_exceptions import RepositoryError, NotFoundError

class ServicoDeItem:
    def __init__(self, db: Session):
        self.db = db

    def adicionar(self, ator_id: int, dados: Dict[str, Any], implementacao: Type[ServicoDeItem]) -> Any:
        try:
            implementacao_instancia = implementacao(self.db)
            novo_item = implementacao_instancia.adicionar_item(ator_id, dados)
    
            return novo_item
        except (NotFoundError, RepositoryError, ServiceError) as e:
            raise e 
        except Exception as e:
            raise ServiceError(f"Erro geral no serviço de item ao adicionar: {e}") from e

    def atualizar(self, item_id: int, dados: Dict[str, Any], implementacao: Type[ServicoDeItem]) -> Any:
        try:
            implementacao_instancia = implementacao(self.db)
            item_atualizado = implementacao_instancia.atualizar_item(item_id, dados)
            return item_atualizado
        except (NotFoundError, RepositoryError, ServiceError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro geral no serviço de item ao atualizar: {e}") from e

    def remover(self, item_id: int, implementacao: Type[ServicoDeItem]) -> None:
        try:
            implementacao_instancia = implementacao(self.db)
            implementacao_instancia.remover_item(item_id)
        except (NotFoundError, RepositoryError, ServiceError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro geral no serviço de item ao remover: {e}") from e
            
    def buscar_por_ator(self, ator_id: int, implementacao: Type[ServicoDeItem]) -> Any:
        try:
            implementacao_instancia = implementacao(self.db)
            return implementacao_instancia.buscar_por_ator(ator_id)
        except (NotFoundError, RepositoryError, ServiceError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro geral no serviço de item ao buscar: {e}") from e

