from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from app.services.TemplateMethodInsight.IstrategyInsight import IEstrategiaDeInsight
from app.exceptions.service_exceptions import ServiceError
from app.services.TemplateMethodItem.Treino import TreinoEstrategiaService
from app.repositories.RegistroRepository import RegistroDiarioRepository

class InsightRendimentoDeAlunos(IEstrategiaDeInsight):
    def __init__(self, db: Session):
        self.db = db
        self.treino_service = TreinoEstrategiaService(db)
        self.ocorrencia_treino_repo = RegistroDiarioRepository(db)

    def _buscar_dados_usuairo_insight(self, usuario_id: int):
        treinos  = self.treino_service.buscar_por_ator(usuario_id)
        if treinos is None:
            raise ServiceError("Nenhuma treino encontrado para o treinador.")
        ids_treinos = [treino.id for treino in treinos]
        # buscar ocorrências dos treinos por usuario        
        ocorrencias = self.ocorrencia_treino_repo.buscar_por_usuario(usuario_id)
        hoje = date.today()
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        fim_semana = inicio_semana + timedelta(days=6, hours=23, minutes=59, seconds=59)
        ocorrencias_semana = [o for o in ocorrencias if inicio_semana <= o.data <= fim_semana and o.item_id in ids_treinos]
        return [treinos, ocorrencias_semana]

    def _processar_dados_insight(self, dados):
        try:
            treinos,ocorrencias_semana = dados
            hoje = date.today()
            ocs_id = [ocorrencia.item_id for ocorrencia in ocorrencias_semana]
            total = len(treinos)
            total_alunos = len(set([ocorrencia.usuario_id for ocorrencia in ocorrencias_semana]))
            finalizados = len([treino for treino in treinos if treino.id in ocs_id])
            atrasados = len([treino for treino in treinos if treino.id not in ocs_id and treino.prazo_final and treino.prazo_final < hoje])
            insight = f"Esta semana você registrou {total} treinos para {total_alunos} alunos.\n"
            insight += f"- {finalizados} treinos ja foram realizados.\n"
            insight += f"- {atrasados} treinos estão atrasadas."
        except Exception as e:
            raise ServiceError(f"Erro ao processar dados de produtividade da equipe: {str(e)}")
        return insight