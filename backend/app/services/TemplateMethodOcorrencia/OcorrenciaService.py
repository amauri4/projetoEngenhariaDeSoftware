from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from app.models.RegistroDeOcorrencia import RegistroDeOcorrencia
from app.exceptions.service_exceptions import ServiceError
from typing import List, Dict, Any
from datetime import date
from app.exceptions.repository_exceptions import NotFoundError

class ServicoDeGeracaoDeOcorrencias(ABC):
    def __init__(self, db: Session):
        self.db = db
        self.ocorrencia_repo = self._get_repositorio_ocorrencia()

    @abstractmethod
    def _get_repositorio_item(self) -> Any:
        pass
    
    @abstractmethod
    def _get_repositorio_ocorrencia(self) -> Any:
        pass

    @abstractmethod
    def _validar_formato_data(self, data:Any) -> Any:
        pass

    @abstractmethod
    def _extrair_configuracao_agendamento(self, item: Any) -> Dict[str, Any]:
        pass

    @abstractmethod
    def _calcular_ocorrencias(self, item_id: int, config: Dict[str, Any], periodo_em_dias: int) -> List[RegistroDeOcorrencia]:
        pass

    def gerar_proximas_ocorrencias(self, item_id: int, periodo_em_dias: int = 30):
        try:
            item = self.item_repo.buscar_por_id(item_id)
            if not item:
                raise NotFoundError(f"Item com ID {item_id} não encontrado.")

            config = self._extrair_configuracao_agendamento(item)
            novas_ocorrencias = self._calcular_ocorrencias(item.id, config, periodo_em_dias)
            
            for ocorrencia in novas_ocorrencias:
                self.ocorrencia_repo.salvar_se_nao_existir(ocorrencia)

            return novas_ocorrencias
        except Exception as e:
            raise ServiceError(f"Erro ao gerar ocorrências para o item {item_id}.") from e

    def criar_ocorrencia_unica(self, item_id: int, data_str: str, status: bool):
        pass

    def buscar_ocorrencias_por_ator(self, ator_id: int) -> List[RegistroDeOcorrencia]:
        try:
            return self.ocorrencia_repo.buscar_por_usuario(ator_id)
        except Exception as e:
            raise ServiceError(f"Erro ao buscar ocorrências do ator {ator_id}.") from e

    def buscar_ocorrencias_concluidas_por_ator(self, ator_id: int) -> List[RegistroDeOcorrencia]:
        try:
            return self.ocorrencia_repo.buscar_concluidos_por_usuario(ator_id)
        except Exception as e:
            raise ServiceError(f"Erro ao buscar ocorrências concluídas do ator {ator_id}.") from e

    def atualizar_status_ocorrencia(self, ocorrencia_id: int, novo_status: bool):
        try:
            ocorrencia = self.ocorrencia_repo.atualizar_registro(ocorrencia_id, novo_status)
            return ocorrencia
        except Exception as e:
            raise ServiceError(f"Erro ao atualizar ocorrência {ocorrencia_id}.") from e
            
    def remover_ocorrencia(self, ocorrencia_id: int):
        try:
            self.ocorrencia_repo.remover_registro(ocorrencia_id)
        except Exception as e:
            raise ServiceError(f"Erro ao remover ocorrência {ocorrencia_id}.") from e

    def buscar_ocorrencias_por_data(self, ator_id: int, data_inicio_str: str = None, data_fim_str: str = None) -> List[RegistroDeOcorrencia]:
        try:
            data_inicio = self._validar_formato_data(data_inicio_str) if data_inicio_str else None
            data_fim = self._validar_formato_data(data_fim_str) if data_fim_str else None
            return self.ocorrencia_repo.buscar_por_data(ator_id, data_inicio, data_fim)
            
        except (ValueError) as e:
            raise ServiceError(f"Formato de data inválido: {e}")
        except Exception as e:
            raise ServiceError(f"Erro ao buscar registros por data para o ator {ator_id}: {e}") from e

    def buscar_ocorrencias_por_data_especifica(self, ator_id: int, data_especifica_str: str) -> List[RegistroDeOcorrencia]:

        try:
            data_especifica = self._validar_formato_data(data_especifica_str)
            return self.ocorrencia_repo.buscar_por_data_especifica(ator_id, data_especifica)

        except (ValueError) as e:
            raise ServiceError(f"Formato de data inválido: {e}")
        except Exception as e:
            raise ServiceError(f"Erro ao buscar registros na data específica para o ator {ator_id}: {e}") from e