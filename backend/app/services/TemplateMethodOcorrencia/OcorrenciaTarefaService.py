from datetime import date
from typing import List, Dict, Any
from app.models.Aplicacao2.InstanciaDeTarefa import InstanciaDeTarefa
from app.models.RegistroDeOcorrencia import RegistroDeOcorrencia
from app.repositories.Aplicacao2.TarefaRepository import TarefaRepository 
from app.repositories.RegistroRepository import RegistroDeOcorrencia 
from app.services.TemplateMethodOcorrencia.OcorrenciaService import ServicoDeGeracaoDeOcorrencias
from app.utils.verificar_data import validar_formato_data
from app.exceptions.repository_exceptions import NotFoundError

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
        Uma tarefa gera uma única ocorrência em sua data de prazo final.
        """
        ocorrencias = []
        prazo_final = config.get("prazo_final")

        if prazo_final:
            nova_ocorrencia = RegistroDeOcorrencia(
                item_rastreavel_id=item_id,
                data_prevista=prazo_final,
                status=False 
            )
            ocorrencias.append(nova_ocorrencia)

        return ocorrencias

    # --- MÉTODO ADICIONADO ---
    def criar_ocorrencia_unica(self, item_id: int, data_str: str, status: bool) -> RegistroDeOcorrencia:
        """
        Implementação para criar uma ocorrência única para uma tarefa.
        Útil para adicionar marcos ou registros manuais a uma tarefa.
        """
        # 1. Valida se a tarefa existe
        item_repo = self._get_repositorio_item()
        tarefa = item_repo.buscar_por_id(item_id)
        if not tarefa:
            raise NotFoundError(f"Tarefa com ID {item_id} não encontrada.")

        # 2. Valida o formato da data
        data_prevista = self._validar_formato_data(data_str)

        # 3. Cria a nova ocorrência
        nova_ocorrencia = RegistroDeOcorrencia(
            item_id=item_id,
            data_prevista=data_prevista,
            status=status
        )

        # 4. Salva no banco de dados, evitando duplicatas
        # (Assumindo que o repositório tem este método)
        self.ocorrencia_repo.salvar_se_nao_existir(nova_ocorrencia)

        return nova_ocorrencia
