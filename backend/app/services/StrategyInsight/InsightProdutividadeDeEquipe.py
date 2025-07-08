
from sqlalchemy.orm import Session
from datetime import date
from app.services.StrategyInsight.IstrategyInsight import IEstrategiaDeInsight
from app.repositories.Aplicacao2.TarefaRepository import TarefaRepository
from app.models.Aplicacao2.InstanciaDeTarefa import InstanciaDeTarefa
from app.models.RegistroDeOcorrencia import RegistroDeOcorrencia
from app.exceptions.service_exceptions import ServiceError

class EstrategiaProdutividadeDeEquipe(IEstrategiaDeInsight):
    def __init__(self, db: Session):
        self.db = db
        self.tarefa_repository = TarefaRepository(db)

    def _buscar_dados_usuairo_insight(self, usuario_id: int):
        tarefas = self.db.query(InstanciaDeTarefa).filter(InstanciaDeTarefa.ator_id == usuario_id).all()
        if tarefas is None:
            raise ServiceError("Nenhuma tarefa encontrada para o gerente.")
        return tarefas

    def _processar_dados_insight(self, tarefas):
        hoje = date.today()
        em_aberto = 0
        finalizadas_antes_do_prazo = 0
        atrasadas = 0
        for tarefa in tarefas:
            prazo = tarefa.prazo_final
            ocorrencias = tarefa.ocorrencias if hasattr(tarefa, 'ocorrencias') else []
            if not ocorrencias:
                if prazo and prazo >= hoje:
                    em_aberto += 1
                elif prazo and prazo < hoje:
                    atrasadas += 1
                continue
            ocorrencia = sorted(ocorrencias, key=lambda o: o.data)[-1]
            if ocorrencia.concluido:
                if prazo and ocorrencia.data <= prazo:
                    finalizadas_antes_do_prazo += 1
                elif prazo and ocorrencia.data > prazo:
                    atrasadas += 1
            else:
                if prazo and prazo < hoje:
                    atrasadas += 1
                else:
                    em_aberto += 1
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
