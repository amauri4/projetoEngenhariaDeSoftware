from typing import List
from app.models.Aplicacao2.InstanciaDeTarefa import InstanciaDeTarefa
from app.repositories.Aplicacao2.TarefaRepository import TarefaRepository
from app.repositories.Aplicacao2.GerenteRepository import GerenteRepository
from app.repositories.Aplicacao2.FuncionarioRepository import FuncionarioRepository
from app.exceptions.service_exceptions import ServiceError
from app.exceptions.repository_exceptions import RepositoryError, NotFoundError
from app.services.TemplateMethodItem.ServicoDeItem import ServicoDeItem
from typing import Dict, Any, List
from app.repositories.UsuarioRepositories import UserRepository
from app.exceptions.service_exceptions import ServiceError
from app.exceptions.repository_exceptions import RepositoryError, NotFoundError

class TarefaEstrategiaService(ServicoDeItem):
    def _preparar_dados_adicionar(self, ator_id: int, dados: Dict[str, Any]) -> Dict[str, Any]:
        descricao = dados.get('descricao')
        data_inicio = dados.get('data_inicio')
        responsavel_id = dados.get('responsavel_id')

        if not all([descricao, data_inicio, responsavel_id]):
            raise ServiceError("Dados insuficientes. 'descricao', 'data_inicio' e 'responsavel_id' são obrigatórios.")

        return {
            "descricao": descricao,
            "data_inicio": data_inicio,
            "criador_id": ator_id,
            "responsavel_id": responsavel_id,
            "prazo_final": dados.get('prazo_final')
        }

    def _executar_adicao(self, dados_preparados: Dict[str, Any]) -> InstanciaDeTarefa:
        tarefa_repo = TarefaRepository(self.db)
        return tarefa_repo.criar_tarefa(**dados_preparados)

    def _preparar_dados_atualizar(self, item_id: int, dados: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "descricao": dados.get('descricao'),
            "responsavel_id": dados.get('responsavel_id'),
            "prazo_final": dados.get('prazo_final')
        }

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

            if ator.tipo_ator == 'gerente':
                gerente_repo = GerenteRepository(self.db)
                return gerente_repo.buscar_tarefas_criadas_por_gerente(ator_id)
            elif ator.tipo_ator == 'funcionario':
                funcionario_repo = FuncionarioRepository(self.db)
                return funcionario_repo.buscar_tarefas_atribuidas_ao_funcionario(ator_id)
            else:
                return []
        except (NotFoundError, RepositoryError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro ao buscar tarefas para o ator {ator_id}.") from e
