from datetime import date, timedelta
from typing import List, Dict, Any
from app.models.Aplicacao3.InstanciaDeTreino import InstanciaDeTreino
from app.repositories.Framework.RegistroDeOcorrenciaRepository import RegistroDeOcorrenciaRepository
from app.repositories.Aplicacao3.TreinoRepository import TreinoRepository
from app.models.Framework.RegistroDeOcorrencia import RegistroDeOcorrencia
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
            "data_inicio": item.data_inicio,
            "data_entrega": item.data_entrega
        }

    def _calcular_ocorrencias(self, item_id: int, config: Dict[str, Any], periodo_em_dias: int) -> List[RegistroDeOcorrencia]:
        ocorrencias = []
        data_inicio = config.get("data_inicio")
        data_entrega = config.get("data_entrega")

        if data_inicio and data_entrega:
            delta = data_entrega - data_inicio
            for i in range(delta.days + 1):
                dia_do_treino = data_inicio + timedelta(days=i)
                nova_ocorrencia = RegistroDeOcorrencia(
                    item_rastreavel_id=item_id,
                    data=dia_do_treino,
                    concluido=False
                )
                ocorrencias.append(nova_ocorrencia)
        
        return ocorrencias

    def criar_ocorrencia_unica(self, item_id: int, data_str: str, status: bool) -> RegistroDeOcorrencia:
        item_repo = self._get_repositorio_item()
        ocorrencia_repo = self._get_repositorio_ocorrencia()

        treino = item_repo.buscar_por_id(item_id)
        if not treino:
            raise NotFoundError(f"Treino com ID {item_id} não encontrado.")

        data_ocorrencia = self._validar_formato_data(data_str)

        nova_ocorrencia = ocorrencia_repo.criar_registro(
            data=data_ocorrencia, 
            habito_id=item_id, 
            concluido=status
        )
        return nova_ocorrencia