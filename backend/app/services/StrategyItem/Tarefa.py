from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional
from app.models.Aplicacao2.InstanciaDeTarefa import InstanciaDeTarefa
from app.repositories.Aplicacao2.TarefaRepository import TarefaRepository
from app.repositories.Aplicacao2.GerenteRepository import GerenteRepository
from app.repositories.Aplicacao2.FuncionarioRepository import FuncionarioRepository
from app.exceptions.service_exceptions import ServiceError
from app.exceptions.repository_exceptions import RepositoryError, NotFoundError
from app.services.StrategyItem.Iitem import IEstrategiaDeItem
from typing import Dict, Any, List, Optional
from app.repositories.UsuarioRepositories import UserRepository

class TarefaEstrategiaService(IEstrategiaDeItem):

    def adicionar(self, db: Session, ator_id: int, dados: Dict[str, Any]) -> InstanciaDeTarefa:
        tarefa_repo = TarefaRepository(db)
        
        try:
            descricao = dados.get('descricao')
            data_inicio = dados.get('data_inicio')
            responsavel_id = dados.get('responsavel_id')
            prazo_final = dados.get('prazo_final') 

            if not all([descricao, data_inicio, responsavel_id]):
                raise ServiceError("Dados insuficientes para criar a tarefa. 'descricao', 'data_inicio' e 'responsavel_id' são obrigatórios.")

            nova_tarefa = tarefa_repo.criar_tarefa(
                descricao=descricao,
                data_inicio=data_inicio,
                criador_id=ator_id,
                responsavel_id=responsavel_id,
                prazo_final=prazo_final
            )
            return nova_tarefa
        except (NotFoundError, RepositoryError) as e:
            raise e
        except Exception as e:
            raise ServiceError("Ocorreu um erro ao adicionar a nova tarefa.") from e

    def atualizar(self, db: Session, item_id: int, dados: Dict[str, Any]) -> InstanciaDeTarefa:
        tarefa_repo = TarefaRepository(db)
        
        try:
            tarefa_atualizada = tarefa_repo.atualizar_tarefa(
                tarefa_id=item_id,
                descricao=dados.get('descricao'),
                responsavel_id=dados.get('responsavel_id'),
                prazo_final=dados.get('prazo_final')
            )
            return tarefa_atualizada
        except (NotFoundError, RepositoryError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Ocorreu um erro ao atualizar a tarefa {item_id}.") from e

    def remover(self, db: Session, item_id: int) -> None:
        tarefa_repo = TarefaRepository(db)
        
        try:
            tarefa_repo.remover_tarefa(item_id)
        except (NotFoundError, RepositoryError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Ocorreu um erro ao remover a tarefa {item_id}.") from e

    def buscar_por_ator(self, db: Session, ator_id: int) -> List[InstanciaDeTarefa]:
        """
        Este método é polimórfico:
        - Se o ator for um Gerente, retorna as tarefas que ele criou.
        - Se o ator for um Funcionário, retorna as tarefas pelas quais ele é responsável.
        """
        ator_repo = UserRepository(db)
        gerente_repo = GerenteRepository(db)
        funcionario_repo = FuncionarioRepository(db)

        try:
            ator = ator_repo.buscar_por_id(ator_id)
            
            if ator.tipo_ator == 'gerente':
                return gerente_repo.buscar_tarefas_criadas_por_gerente(ator_id)
            elif ator.tipo_ator == 'funcionario':
                return funcionario_repo.buscar_tarefas_atribuidas_ao_funcionario(ator_id)
            else:
                return []
        except (NotFoundError, RepositoryError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Ocorreu um erro ao buscar tarefas para o ator {ator_id}.") from e
