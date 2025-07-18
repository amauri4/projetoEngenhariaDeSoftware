from datetime import date
from typing import List, Dict, Any
from app.models.Aplicacao2.InstanciaDeTarefa import InstanciaDeTarefa
from app.repositories.Framework.RegistroDeOcorrenciaRepository import RegistroDeOcorrenciaRepository
from app.repositories.Aplicacao2.TarefaRepository import TarefaRepository 
from app.repositories.Framework.RegistroDeOcorrenciaRepository import RegistroDeOcorrencia 
from app.services.Framework.OcorrenciaTemplate import OcorrenciaTemplate
from app.utils.verificar_data import validar_formato_data
from app.exceptions.repository_exceptions import NotFoundError

class OcorrenciaTarefa(OcorrenciaTemplate):
    def _get_repositorio_item(self) -> TarefaRepository:
        return TarefaRepository(self.db)

    def _get_repositorio_ocorrencia(self) -> RegistroDeOcorrenciaRepository:
        return RegistroDeOcorrenciaRepository(self.db)

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
        Uma tarefa gera uma única ocorrência em sua data de prazo final.
        """
        ocorrencias = []
        prazo_final = config.get("prazo_final")

        if prazo_final:
            nova_ocorrencia = RegistroDeOcorrencia(
                item_rastreavel_id=item_id,
                data=prazo_final,
                concluido=False 
            )
            ocorrencias.append(nova_ocorrencia)

        return ocorrencias

    def criar_ocorrencia_unica(self, item_id: int, data_str: str, status: bool) -> RegistroDeOcorrencia:
        item_repo = self._get_repositorio_item()
        ocorrencia_repo = self._get_repositorio_ocorrencia()

        tarefa = item_repo.buscar_por_id(item_id)
        if not tarefa:
            raise NotFoundError(f"Tarefa com ID {item_id} não encontrada.")

        data_prevista = self._validar_formato_data(data_str)

        nova_ocorrencia = ocorrencia_repo.criar_registro(data_prevista, item_id, status)

        return nova_ocorrencia
