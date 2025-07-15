from sqlalchemy.orm import Session
from datetime import date
from app.services.TemplateMethodInsight.IstrategyInsight import IEstrategiaDeInsight
from app.exceptions.service_exceptions import ServiceError
from app.services.TemplateMethodItem.Tarefa import TarefaEstrategiaService
from app.repositories.RegistroRepository import RegistroDiarioRepository

class EstrategiaProdutividadeDeEquipe(IEstrategiaDeInsight):
    def __init__(self, db: Session):
        self.db = db
        self.tarefa_service = TarefaEstrategiaService(db)
        self.ocorrencia_tarefa_repo = RegistroDiarioRepository(db)

    def _buscar_dados_usuairo_insight(self, usuario_id: int):
        tarefas  = self.tarefa_service.buscar_por_ator(usuario_id)
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
        try:
            tarefas,ocorrencias = dados
            hoje = date.today()
            ocs_id = [ocorrencia.item_id for ocorrencia in ocorrencias]
            em_aberto = len([tarefa for tarefa in tarefas if tarefa.id not in ocs_id])
            finalizadas_antes_do_prazo = len([tarefa for tarefa in tarefas if tarefa.id in ocs_id and tarefa.prazo_final and tarefa.prazo_final >= hoje])
            atrasadas = len([tarefa for tarefa in tarefas if tarefa.id not in ocs_id and tarefa.prazo_final and tarefa.prazo_final < hoje])
            insight = f"- Sua equipe tem {em_aberto} tarefas em aberto.\n"
            insight += f"- {finalizadas_antes_do_prazo} tarefas foram finalizadas antes do prazo.\n"
            insight += f"- {atrasadas} tarefas estão atrasadas."
        except Exception as e:
            raise ServiceError(f"Erro ao processar dados de produtividade da equipe: {str(e)}")
        return insight