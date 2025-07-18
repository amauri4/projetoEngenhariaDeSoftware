from typing import List, Dict, Any
from sqlalchemy.orm import joinedload
from app.models.Aplicacao3.InstanciaDeTreino import InstanciaDeTreino
from app.repositories.Aplicacao3.TreinoRepository import TreinoRepository
from app.repositories.Aplicacao3.IntrutorRepository import InstrutorRepository
from app.repositories.Aplicacao3.AlunoRepository import AlunoRepository
from app.services.Framework.ItemTemplate import ItemTemplate
from app.repositories.Framework.AtorRepository import AtorRepository
from app.exceptions.service_exceptions import ServiceError
from app.exceptions.repository_exceptions import RepositoryError, NotFoundError
from app.utils.verificar_data import validar_formato_data

class ItemTreino(ItemTemplate):
    def _preparar_dados_adicionar(self, ator_id: int, dados: Dict[str, Any]) -> Dict[str, Any]:
        descricao = dados.get('descricao')
        data_inicio_str = dados.get('data_inicio')
        responsavel_id = dados.get('id_aluno_responsavel')
        data_entrega_str = dados.get('data_entrega')

        if not all([descricao, data_inicio_str, responsavel_id]):
            raise ServiceError("Dados insuficientes. 'descricao', 'data_inicio' e 'id_aluno_responsavel' são obrigatórios.")
        
        try:
            data_inicio_obj = validar_formato_data(data_inicio_str)
            data_entrega_obj = None
            if data_entrega_str:
                data_entrega_obj = validar_formato_data(data_entrega_str)
        except ValueError:
            raise ServiceError("Formato de data inválido. Use 'YYYY-MM-DD'.")

        return {
            "descricao": descricao,
            "data_inicio": data_inicio_obj, 
            "criador_id": ator_id, 
            "responsavel_id": responsavel_id, 
            "data_entrega": data_entrega_obj 
        }

    def _executar_adicao(self, dados_preparados: Dict[str, Any]) -> InstanciaDeTreino:
        treino_repo = TreinoRepository(self.db)
        return treino_repo.criar_treino(**dados_preparados)

    def _preparar_dados_atualizar(self, item_id: int, dados: Dict[str, Any]) -> Dict[str, Any]:
        dados_atualizados = {
            "descricao": dados.get('descricao'),
            "responsavel_id": dados.get('id_aluno_responsavel')
        }
        if 'data_entrega' in dados and dados['data_entrega'] is not None:
            try:
                dados_atualizados['data_entrega'] = validar_formato_data(dados['data_entrega'])
            except ValueError:
                raise ServiceError("Formato de data inválido para 'data_entrega'. Use 'YYYY-MM-DD'.")
        
        return dados_atualizados

    def _executar_atualizacao(self, item_id: int, dados_preparados: Dict[str, Any]) -> InstanciaDeTreino:
        treino_repo = TreinoRepository(self.db)
        return treino_repo.atualizar_treino(treino_id=item_id, **dados_preparados)

    def _executar_remocao(self, item_id: int) -> None:
        treino_repo = TreinoRepository(self.db)
        treino_repo.remover_treino(item_id)

    def buscar_por_ator(self, ator_id: int) -> List[InstanciaDeTreino]:

        try:
            ator_repo = AtorRepository(self.db)
            ator = ator_repo.buscar_por_id(ator_id)
            if not ator:
                raise NotFoundError(f"Ator com ID {ator_id} não encontrado.")

            query = self.db.query(InstanciaDeTreino).options(
                joinedload(InstanciaDeTreino.criador),
                joinedload(InstanciaDeTreino.responsavel)
            )

            if ator.tipo_ator == 'instrutor':
                return query.filter(InstanciaDeTreino.ator_id == ator_id).all()
            elif ator.tipo_ator == 'aluno':
                return query.filter(InstanciaDeTreino.id_aluno_responsavel == ator_id).all()
            else:
                return []
        except (NotFoundError, RepositoryError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro ao buscar treinos para o ator {ator_id}.") from e
