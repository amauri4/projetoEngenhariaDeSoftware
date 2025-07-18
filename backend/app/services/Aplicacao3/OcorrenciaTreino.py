from datetime import date
from typing import List, Dict, Any
from app.models.Aplicacao3.InstanciaDeTreino import InstanciaDeTreino
from app.repositories.Framework.RegistroDeOcorrenciaRepository import RegistroDeOcorrenciaRepository
from app.repositories.Aplicacao3.TreinoRepository import TreinoRepository
from app.repositories.Framework.RegistroDeOcorrenciaRepository import RegistroDeOcorrencia
from app.services.Framework.OcorrenciaTemplate import OcorrenciaTemplate
from app.utils.verificar_data import validar_formato_data
from app.exceptions.repository_exceptions import NotFoundError

class OcorrenciaTreino(OcorrenciaTemplate):
    def _get_repositorio_item(self) -> TreinoRepository:
        return TreinoRepository(self.db)

    def _get_repositorio_ocorrencia(self) -> RegistroDeOcorrenciaRepository:
        return RegistroDeOcorrenciaRepository(self.db)

    def _validar_formato_data(self, data_str: str) -> date:
        return validar_formato_data(data_str)

    def _extrair_configuracao_agendamento(self, item: InstanciaDeTreino) -> Dict[str, Any]:
        if not isinstance(item, InstanciaDeTreino):
            raise TypeError("O item fornecido não é uma InstanciaDeTreino.")
        return {
            "prazo_final": item.prazo_final
        }

    def _calcular_ocorrencias(self, item_id: int, config: Dict[str, Any], periodo_em_dias: int) -> List[RegistroDeOcorrencia]:
        """
        Um treino gera uma única ocorrência em sua data de prazo final.
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