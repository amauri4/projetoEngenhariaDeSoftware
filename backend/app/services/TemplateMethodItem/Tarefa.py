from typing import List
from sqlalchemy.orm import joinedload
from app.models.Aplicacao2.InstanciaDeTarefa import InstanciaDeTarefa
from app.repositories.Aplicacao2.TarefaRepository import TarefaRepository
from app.repositories.Aplicacao2.GerenteRepository import GerenteRepository
from app.repositories.Aplicacao2.FuncionarioRepository import FuncionarioRepository
from app.exceptions.service_exceptions import ServiceError
from app.exceptions.repository_exceptions import RepositoryError, NotFoundError
from app.services.TemplateMethodItem.ServicoDeItem import ServicoDeItem
from typing import Dict, Any, List
from app.repositories.AtorRepository import UserRepository
from app.exceptions.service_exceptions import ServiceError
from app.exceptions.repository_exceptions import RepositoryError, NotFoundError
from app.utils.verificar_data import validar_formato_data

class TarefaEstrategiaService(ServicoDeItem):
    def _preparar_dados_adicionar(self, ator_id: int, dados: Dict[str, Any]) -> Dict[str, Any]:
        descricao = dados.get('descricao')
        data_inicio = dados.get('data_inicio')
        responsavel_id = dados.get('responsavel_id')
        prazo_final_str = dados.get('prazo_final')

        if not all([descricao, data_inicio, responsavel_id]):
            raise ServiceError("Dados insuficientes. 'descricao', 'data_inicio' e 'responsavel_id' são obrigatórios.")
        
        try:
            data_inicio_obj = validar_formato_data(data_inicio)
            prazo_final_obj = None
            if prazo_final_str:
                prazo_final_obj = validar_formato_data(prazo_final_str)
        except ValueError:
            raise ServiceError("Formato de data inválido. Use 'YYYY-MM-DD'.")

        return {
            "descricao": descricao,
            "data_inicio": data_inicio_obj, 
            "criador_id": ator_id,
            "responsavel_id": responsavel_id,
            "prazo_final": prazo_final_obj 
        }

    def _executar_adicao(self, dados_preparados: Dict[str, Any]) -> InstanciaDeTarefa:
        tarefa_repo = TarefaRepository(self.db)
        return tarefa_repo.criar_tarefa(**dados_preparados)

    def _preparar_dados_atualizar(self, item_id: int, dados: Dict[str, Any]) -> Dict[str, Any]:
        dados_atualizados = {
            "descricao": dados.get('descricao'),
            "responsavel_id": dados.get('responsavel_id')
        }
        if 'prazo_final' in dados and dados['prazo_final'] is not None:
            try:
                dados_atualizados['prazo_final'] = validar_formato_data(dados['prazo_final'])
            except ValueError:
                raise ServiceError("Formato de data inválido para 'prazo_final'. Use 'YYYY-MM-DD'.")
        
        return dados_atualizados

    def _executar_atualizacao(self, item_id: int, dados_preparados: Dict[str, Any]) -> InstanciaDeTarefa:
        tarefa_repo = TarefaRepository(self.db)
        return tarefa_repo.atualizar_tarefa(tarefa_id=item_id, **dados_preparados)

    def _executar_remocao(self, item_id: int) -> None:
        tarefa_repo = TarefaRepository(self.db)
        tarefa_repo.remover_tarefa(item_id)

    def buscar_por_ator(self, ator_id: int) -> List[InstanciaDeTarefa]:
        try:
            ator_repo = UserRepository(self.db)
            ator = ator_repo.buscar_por_id(ator_id)
            if not ator:
                raise NotFoundError(f"Ator com ID {ator_id} não encontrado.")

            query = self.db.query(InstanciaDeTarefa).options(
                joinedload(InstanciaDeTarefa.criador),
                joinedload(InstanciaDeTarefa.responsavel)
            )
            if ator.tipo_ator == 'gerente':
                return query.filter(InstanciaDeTarefa.ator_id == ator_id).all()
            elif ator.tipo_ator == 'funcionario':
                return query.filter(InstanciaDeTarefa.id_funcionario_responsavel == ator_id).all()
            else:
                return []
        except (NotFoundError, RepositoryError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro ao buscar tarefas para o ator {ator_id}.") from e
