from sqlalchemy.orm import Session
from typing import Dict, Any, Type, List, Optional
from app.services.TemplateMethodOcorrencia.OcorrenciaService import ServicoDeGeracaoDeOcorrencias
from app.exceptions.service_exceptions import ServiceError
from app.exceptions.repository_exceptions import RepositoryError, NotFoundError

class ServicoDeOcorrencia:
    def __init__(self, db: Session):
        self.db = db

    def gerar_proximas(self, item_id: int, periodo_em_dias: int, implementacao: Type[ServicoDeGeracaoDeOcorrencias]) -> List[Any]:
        try:
            implementacao_instancia = implementacao(self.db)
            ocorrencias = implementacao_instancia.gerar_proximas_ocorrencias(item_id, periodo_em_dias)
            return ocorrencias
        except (NotFoundError, RepositoryError, ServiceError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro geral no serviço de ocorrência ao gerar próximas: {e}") from e

    def criar_unica(self, item_id: int, data_str: str, status: bool, implementacao: Type[ServicoDeGeracaoDeOcorrencias]) -> Any:
        try:
            implementacao_instancia = implementacao(self.db)
            ocorrencia = implementacao_instancia.criar_ocorrencia_unica(item_id, data_str, status)
            return ocorrencia
        except (NotFoundError, RepositoryError, ServiceError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro geral no serviço de ocorrência ao criar única: {e}") from e

    def atualizar_status(self, ocorrencia_id: int, novo_status: bool, implementacao: Type[ServicoDeGeracaoDeOcorrencias]) -> Any:
        try:
            implementacao_instancia = implementacao(self.db)
            ocorrencia_atualizada = implementacao_instancia.atualizar_status_ocorrencia(ocorrencia_id, novo_status)
            return ocorrencia_atualizada
        except (NotFoundError, RepositoryError, ServiceError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro geral no serviço de ocorrência ao atualizar status: {e}") from e

    def remover(self, ocorrencia_id: int, implementacao: Type[ServicoDeGeracaoDeOcorrencias]) -> None:
        try:
            implementacao_instancia = implementacao(self.db)
            implementacao_instancia.remover_ocorrencia(ocorrencia_id)
        except (NotFoundError, RepositoryError, ServiceError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro geral no serviço de ocorrência ao remover: {e}") from e

    def buscar_por_ator(self, ator_id: int, implementacao: Type[ServicoDeGeracaoDeOcorrencias]) -> List[Any]:
        try:
            implementacao_instancia = implementacao(self.db)
            return implementacao_instancia.buscar_ocorrencias_por_ator(ator_id)
        except (NotFoundError, RepositoryError, ServiceError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro geral no serviço de ocorrência ao buscar por ator: {e}") from e

    def buscar_concluidas_por_ator(self, ator_id: int, implementacao: Type[ServicoDeGeracaoDeOcorrencias]) -> List[Any]:
        try:
            implementacao_instancia = implementacao(self.db)
            return implementacao_instancia.buscar_ocorrencias_concluidas_por_ator(ator_id)
        except (NotFoundError, RepositoryError, ServiceError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro geral no serviço de ocorrência ao buscar concluídas: {e}") from e

    def buscar_por_data(self, ator_id: int, data_inicio: Optional[str], data_fim: Optional[str], implementacao: Type[ServicoDeGeracaoDeOcorrencias]) -> List[Any]:
        try:
            implementacao_instancia = implementacao(self.db)
            return implementacao_instancia.buscar_ocorrencias_por_data(ator_id, data_inicio, data_fim)
        except (NotFoundError, RepositoryError, ServiceError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro geral no serviço de ocorrência ao buscar por data: {e}") from e

    def buscar_por_data_especifica(self, ator_id: int, data_especifica: str, implementacao: Type[ServicoDeGeracaoDeOcorrencias]) -> List[Any]:
        try:
            implementacao_instancia = implementacao(self.db)
            return implementacao_instancia.buscar_ocorrencias_por_data_especifica(ator_id, data_especifica)
        except (NotFoundError, RepositoryError, ServiceError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro geral no serviço de ocorrência ao buscar por data específica: {e}") from e
