
from sqlalchemy.orm import Session
from datetime import date
from app.services.StrategyInsight.IstrategyInsight import IEstrategiaDeInsight
from app.repositories.Aplicacao2.TarefaRepository import TarefaRepository
from app.models.Aplicacao2.InstanciaDeTarefa import InstanciaDeTarefa
from app.models.RegistroDeOcorrencia import RegistroDeOcorrencia
from app.exceptions.service_exceptions import ServiceError
from app.services.StrategyItem.Tarefa import TarefaEstrategiaService
from app.repositories.RegistroRepository import RegistroDiarioRepository


class EstrategiaProdutividadeDeEquipe(IEstrategiaDeInsight):
    def __init__(self, db: Session):
        self.db = db
        self.tarefa_repo = TarefaEstrategiaService(db)
        self.ocorrencia_tarefa_repo = RegistroDiarioRepository(db)

    def _buscar_dados_usuairo_insight(self, usuario_id: int):
        # TODO: ainda falta filtrar por intervalo de tempo para pegar tarefas com no intervalo de um ou dois meses
        tarefas  = self.tarefa_repo.buscar_por_ator(usuario_id)
        if tarefas is None:
            raise ServiceError("Nenhuma tarefa encontrada para o gerente.")
        # obter id das tarefas
        ids_tarefas = [tarefa.id for tarefa in tarefas]
        # buscar ocorrências das tarefas por usuario
        ocorrencias = self.ocorrencia_tarefa_repo.buscar_por_usuario(usuario_id)
        # filtrar ocorrencias por id de tarefa
        ocorrencias = [ocorrencia for ocorrencia in ocorrencias if ocorrencia.item_id in ids_tarefas]
        return [tarefas, ocorrencias]

    def _processar_dados_insight(self, dados):
        tarefas,ocorrencias = dados
        hoje = date.today()
        ocs_id = [ocorrencia.item_id for ocorrencia in ocorrencias]
        em_aberto = len([tarefa for tarefa in tarefas if tarefa.id not in ocs_id])
        finalizadas_antes_do_prazo = len([tarefa for tarefa in tarefas if tarefa.id in ocs_id and tarefa.prazo_final and tarefa.prazo_final >= hoje])
        atrasadas = len([tarefa for tarefa in tarefas if tarefa.id not in ocs_id and tarefa.prazo_final and tarefa.prazo_final < hoje])
        insight = f"- Sua equipe tem {em_aberto} tarefas em aberto.\n"
        insight += f"- {finalizadas_antes_do_prazo} tarefas foram finalizadas antes do prazo.\n"
        insight += f"- {atrasadas} tarefas estão atrasadas."
        return insight

    def gerar_insight(self, usuario_id: int):
        try:
            tarefas = self._buscar_dados_usuairo_insight(usuario_id)
            return self._processar_dados_insight(tarefas)
        except Exception as e:
            raise ServiceError(f"Erro ao gerar insight de produtividade da equipe: {str(e)}")
