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
from backend.app.services.StrategyItem.Iitem import IEstrategiaDeItem
from app.database import session
from app.utils.validar_frequencia import validar_frequencia
from app.utils.verificar_data import validar_formato_data
from app.utils.dia_semana_to_num import converter_numero_para_dia_semana
from app.models.enums.frequencia_enums import FrequenciaEnum

class EstrategiaDeHabito(IEstrategiaDeItem):
    def __init__(self, db: session):
        self.db = db
        self.habito_repo = HabitoUsuarioRepository(db)
        self.habito_base_repo = HabitoBaseRepository(db)
        self.ator_repo = UserRepository(db)
        self.dia_semana_repo = DiaHabitoSemanaRepository(db)
        self.dia_mes_repo = DiaHabitoMesRepository(db)

    def adicionar(self, ator_id: int, dados: Dict[str, Any]):
        try:
            print(f'\n\n{dados}\n\n')
            if not self.ator_repo.buscar_por_id(ator_id):
                raise AuthError(f"Ator com ID {ator_id} não encontrado.")
            
            habito_base_id = dados.get('habito_base_id')
            if not self.habito_base_repo.buscar_por_id(habito_base_id):
                raise ConflictError(f"Hábito base com ID {habito_base_id} não encontrado.")
            
            frequencia = dados.get('frequencia')
            if not validar_frequencia(frequencia):
                raise ConflictError(f"Frequência inválida. Opções válidas: 'diario', 'semanal', 'mensal'")
            
            data_inicio = dados.get('data_inicio')
            if data_inicio is None:
                raise ConflictError("A data de início é obrigatória")

            data_inicio = validar_formato_data(data_inicio)
            vezes_na_semana = dados.get('vezes_na_semana')

            novo_habito_usuario = self.habito_repo.criar_habito_usuario(
                descricao=dados.get('descricao'), 
                habito_base_id=dados.get('habito_base_id'), 
                usuario_id=ator_id, 
                frequencia=frequencia,  
                data_inicio=data_inicio,
                quantidade_semanal=vezes_na_semana
            )

            dias_da_semana = dados.get('dias_da_semana')
            dias_do_mes = dados.get('dias_do_mes')

            if frequencia.lower() in ['semanal', 'diaria'] and dias_da_semana:
                if not isinstance(dias_da_semana, list):
                    raise ConflictError("dias_da_semana deve ser uma lista de números")
                
                for dia_num in dias_da_semana:
                    try:
                        dia_enum = converter_numero_para_dia_semana(dia_num)
                        self.dia_semana_repo.adicionar_dia(
                            habito_id=novo_habito_usuario.id,
                            dia=dia_enum
                        )
                    except ValueError as e:
                        raise ValueError(f"Erro no dia {dia_num}: {str(e)}")
                
                if frequencia.lower() == 'semanal':
                    if vezes_na_semana is None:
                        raise ConflictError("vezes_na_semana é obrigatório para frequência semanal")
                    novo_habito_usuario.vezes_na_semana = vezes_na_semana

            if frequencia.lower() == 'mensal' and dias_do_mes:
                if not isinstance(dias_do_mes, list):
                    raise ValueError("dias_do_mes deve ser uma lista de números")
                
                for dia in dias_do_mes:
                    if dia < 1 or dia > 31:
                        raise ConflictError(f"Dia do mês inválido: {dia}. Deve ser entre 1 e 31")
                    
                    self.dia_mes_repo.adicionar_dia(
                        habito_id=novo_habito_usuario.id,
                        dia=dia
                    )
            print(novo_habito_usuario)
            return novo_habito_usuario
        except (AuthError, ConflictError) as e:
            print(str(e))
            raise e(f'{str(e)}')
        except Exception as e:
            print(str(e))
            raise ServiceError(f"Erro ao atualizar hábito de usuário: {str(e)}")

    def atualizar(self, item_id: int, dados: Dict[str, Any]):
        try:
            habito = self.habito_repo.buscar_por_id(item_id)
            if not habito:
                raise ConflictError("Hábito não encontrado")

            habito.descricao = dados.get('descricao', habito.descricao)
            habito.habito_base_id = dados.get('habito_base_id', habito.habito_base_id)
            habito.ator_id = dados.get('ator_id', habito.ator_id) 
            habito.data_inicio = dados.get('data_inicio', habito.data_inicio)
            
            nova_frequencia_str = dados.get('frequencia', habito.frequencia.value)
            habito.frequencia = FrequenciaEnum[nova_frequencia_str.upper()]

            if habito.frequencia in [FrequenciaEnum.SEMANAL, FrequenciaEnum.DIARIA]:
                habito.vezes_na_semana = dados.get('vezes_na_semana', habito.vezes_na_semana)
                
                if 'dias_da_semana' in dados:
                    novos_dias = dados.get('dias_da_semana')
                    self.habito_repo.atualizar_dias_semana(habito_id=habito.id, novos_dias=novos_dias)

            if habito.frequencia == FrequenciaEnum.MENSAL and 'dias_do_mes' in dados:
                self.dia_mes_repo.atualizar_dias(habito.id, dados.get('dias_do_mes'))

            return habito

        except (AuthError, ConflictError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro ao atualizar hábito de usuário: {str(e)}")

    def remover(self, item_id: int):
        try:
            habito_usuario = self.habito_repo.buscar_por_id(item_id)
            if not habito_usuario:
                raise ConflictError("Hábito de usuário não encontrado.")
            
            self.habito_repo.remover_habito_usuario(item_id)
        except ConflictError as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro ao remover hábito de usuário: {str(e)}")

    def buscar_por_ator(self, usuario_email: str):
        try:
            usuario = self.ator_repo.buscar_por_id(usuario_email)
            if not usuario:
                raise AuthError("Usuário não encontrado.")
            
            habitos_usuario = self.habito_repo.buscar_todos_por_id(usuario_email)
            return habitos_usuario
        except AuthError as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro ao buscar hábitos do usuário: {str(e)}")