from typing import Dict, Any, List
from app.repositories.HabitoUsuarioRepository import HabitoUsuarioRepository
from app.repositories.HabitoBaseRepository import HabitoBaseRepository
from app.repositories.UsuarioRepositories import UserRepository
from app.repositories.DiaHabitoMesRepository import DiaHabitoMesRepository 
from app.repositories.DiaHabitoSemanaRepository import DiaHabitoSemanaRepository 
from app.models.InstanciaDeHabito import InstanciaDeHabito
from app.models.DiaHabitoSemana import DiaHabitoSemana
from app.models.DiaHabitoMes import DiaHabitoMes
from app.exceptions.service_exceptions import ConflictError, AuthError, ServiceError
from app.services.TemplateMethodItem.ServicoDeItem import ServicoDeItem
from app.database import session
from app.utils.validar_frequencia import validar_frequencia
from app.utils.verificar_data import validar_formato_data
from app.utils.dia_semana_to_num import converter_numero_para_dia_semana
from app.exceptions.service_exceptions import ServiceError, ConflictError, AuthError
from app.exceptions.repository_exceptions import RepositoryError, NotFoundError
from app.models.enums.frequencia_enums import FrequenciaEnum

class EstrategiaDeHabito(ServicoDeItem):

    def _preparar_dados_adicionar(self, ator_id: int, dados: Dict[str, Any]) -> Dict[str, Any]:
        ator_repo = UserRepository(self.db)
        habito_base_repo = HabitoBaseRepository(self.db)

        if not ator_repo.buscar_por_id(ator_id):
            raise AuthError(f"Ator com ID {ator_id} não encontrado.")
        
        habito_base_id = dados.get('habito_base_id')
        if not habito_base_repo.buscar_por_id(habito_base_id):
            raise ConflictError(f"Hábito base com ID {habito_base_id} não encontrado.")
        
        frequencia = dados.get('frequencia')
        if not validar_frequencia(frequencia):
            raise ConflictError(f"Frequência inválida. Opções válidas: 'diario', 'semanal', 'mensal'")
        
        data_inicio_str = dados.get('data_inicio')
        if data_inicio_str is None:
            raise ConflictError("A data de início é obrigatória")
        data_inicio = validar_formato_data(data_inicio_str)

        return {
            "descricao": dados.get('descricao'),
            "habito_base_id": habito_base_id,
            "usuario_id": ator_id,
            "frequencia": frequencia,
            "data_inicio": data_inicio,
            "quantidade_semanal": dados.get('vezes_na_semana')
        }

    def _executar_adicao(self, dados_preparados: Dict[str, Any]) -> InstanciaDeHabito:
        habito_repo = HabitoUsuarioRepository(self.db)
        return habito_repo.criar_habito_usuario(**dados_preparados)

    def _logica_pos_adicionar(self, novo_habito: InstanciaDeHabito, dados_originais: Dict[str, Any]) -> None:
        frequencia = dados_originais.get('frequencia', '').lower()
        
        if frequencia in [FrequenciaEnum.SEMANAL, FrequenciaEnum.DIARIA] and 'dias_da_semana' in dados_originais:
            self._adicionar_dias_semana(novo_habito.id, dados_originais['dias_da_semana'])
        
        if frequencia == FrequenciaEnum.MENSAL and 'dias_do_mes' in dados_originais:
            self._adicionar_dias_mes(novo_habito.id, dados_originais['dias_do_mes'])

    def _preparar_dados_atualizar(self, item_id: int, dados: Dict[str, Any]) -> Dict[str, Any]:
        if 'frequencia' in dados and not validar_frequencia(dados['frequencia']):
            raise ConflictError("Frequência de atualização inválida.")
        return dados

    def _executar_atualizacao(self, item_id: int, dados_preparados: Dict[str, Any]) -> InstanciaDeHabito:
        habito_repo = HabitoUsuarioRepository(self.db)
        dia_mes_repo = DiaHabitoMesRepository(self.db)

        habito = habito_repo.buscar_por_id(item_id)
        if not habito:
            raise NotFoundError(f"Hábito com ID {item_id} não encontrado.")

        habito.descricao = dados_preparados.get('descricao', habito.descricao)
        habito.habito_base_id = dados_preparados.get('habito_base_id', habito.habito_base_id)
        
        if 'data_inicio' in dados_preparados:
            habito.data_inicio = validar_formato_data(dados_preparados['data_inicio'])
        
        if 'frequencia' in dados_preparados:
            habito.frequencia = FrequenciaEnum[dados_preparados['frequencia'].upper()]

        if habito.frequencia in [FrequenciaEnum.SEMANAL, FrequenciaEnum.DIARIA]:
            habito.vezes_na_semana = dados_preparados.get('vezes_na_semana', habito.vezes_na_semana)
            if 'dias_da_semana' in dados_preparados:
                habito_repo.atualizar_dias_semana(habito_id=habito.id, novos_dias=dados_preparados['dias_da_semana'])

        if habito.frequencia == FrequenciaEnum.MENSAL and 'dias_do_mes' in dados_preparados:
            dia_mes_repo.atualizar_dias(habito.id, dados_preparados['dias_do_mes'])
        
        return habito

    def _executar_remocao(self, item_id: int) -> None:
        habito_repo = HabitoUsuarioRepository(self.db)
        habito_repo.remover_habito_usuario(item_id)

    def buscar_por_ator(self, ator_id: int) -> List[InstanciaDeHabito]:
        try:
            habito_repo = HabitoUsuarioRepository(self.db)
            return habito_repo.buscar_todos_por_id(ator_id)
        except (NotFoundError, RepositoryError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro ao buscar hábitos para o ator {ator_id}.") from e

    def _adicionar_dias_semana(self, habito_id: int, dias_da_semana: List[int]):
        dia_semana_repo = DiaHabitoSemanaRepository(self.db)
        if not isinstance(dias_da_semana, list):
            raise ConflictError("dias_da_semana deve ser uma lista de números.")
        
        for dia_num in dias_da_semana:
            try:
                dia_enum = converter_numero_para_dia_semana(dia_num)
                dia_semana_repo.adicionar_dia(habito_id=habito_id, dia=dia_enum)
            except ValueError as e:
                raise ServiceError(f"Erro no dia da semana {dia_num}: {e}")

    def _adicionar_dias_mes(self, habito_id: int, dias_do_mes: List[int]):
        dia_mes_repo = DiaHabitoMesRepository(self.db)
        if not isinstance(dias_do_mes, list):
            raise ConflictError("dias_do_mes deve ser uma lista de números.")
            
        for dia in dias_do_mes:
            if not (1 <= dia <= 31):
                raise ConflictError(f"Dia do mês inválido: {dia}. Deve ser entre 1 e 31.")
            dia_mes_repo.adicionar_dia(habito_id=habito_id, dia=dia)
