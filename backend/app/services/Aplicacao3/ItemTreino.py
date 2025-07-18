from typing import List, Dict, Any
from app.models.Aplicacao3.InstanciaDeTreino import InstanciaDeTreino
from app.repositories.Aplicacao3.TreinoRepository import TreinoRepository
from app.repositories.Aplicacao3.GerenteRepository import GerenteRepository
from app.repositories.Aplicacao3.FuncionarioRepository import FuncionarioRepository
from app.exceptions.service_exceptions import ServiceError
from app.exceptions.repository_exceptions import RepositoryError, NotFoundError
from app.services.Framework.ItemTemplate import ItemTemplate
from app.repositories.Framework.AtorRepository import UserRepository
from app.utils.verificar_data import validar_formato_data

class ItemTreino(ItemTemplate):
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
