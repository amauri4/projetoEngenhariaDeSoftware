from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
from app.models.Aplicacao2.InstanciaDeTarefa import InstanciaDeTarefa
from app.models.RegistroDeOcorrencia import RegistroDeOcorrencia
from app.repositories.Aplicacao2.TarefaRepository import TarefaRepository 
from app.repositories.RegistroRepository import RegistroDeOcorrencia 
from app.exceptions.service_exceptions import ServiceError
from app.exceptions.repository_exceptions import RepositoryError, NotFoundError
from app.services.TemplateMethodOcorrencia.OcorrenciaService import ServicoDeGeracaoDeOcorrencias
from app.utils.verificar_data import validar_formato_data

class ServicoDeOcorrenciaDeTarefa(ServicoDeGeracaoDeOcorrencias):
    def _get_repositorio_item(self) -> TarefaRepository:
        return TarefaRepository(self.db)

    def _get_repositorio_ocorrencia(self) -> RegistroDeOcorrencia:
        return RegistroDeOcorrencia(self.db)

    def _validar_formato_data(self, data_str: str) -> date:
        return validar_formato_data(data_str)

    def _extrair_configuracao_agendamento(self, item: InstanciaDeTarefa) -> Dict[str, Any]:
        if not isinstance(item, InstanciaDeTarefa):
            raise TypeError("O item fornecido não é uma InstanciaDeTarefa.")
            
        return {
            "prazo_final": item.prazo_final
        }

    def _calcular_ocorrencias(self, item_id: int, config: Dict[str, Any], periodo_em_dias: int) -> List[RegistroDeOcorrencia]:
        """
        uma tarefa gera uma única ocorrência em sua data de prazo final
        """
        ocorrencias = []
        prazo_final = config.get("prazo_final")

        # se a tarefa tem um prazo final, ela gera uma única ocorrência nessa data
        if prazo_final:
            # a ocorrência representa o "evento" de a tarefa precisar ser concluída.
            # o status inicial é 'False' (não concluído).
            nova_ocorrencia = RegistroDeOcorrencia(
                item_rastreavel_id=item_id,
                data_prevista=prazo_final,
                status=False 
            )
            ocorrencias.append(nova_ocorrencia)

        return ocorrencias

