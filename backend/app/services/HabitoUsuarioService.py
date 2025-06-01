from app.repositories.HabitoUsuarioRepository import HabitoUsuarioRepository
from app.repositories.HabitoBaseRepository import HabitoBaseRepository
from app.repositories.UsuarioRepositories import UserRepository
from app.repositories.DiaHabitoMesRepository import DiaHabitoMesRepository
from app.repositories.DiaHabitoSemanaRepository import DiaHabitoSemanaRepository
from app.repositories.CategoriaRepository import CategoriaRepository
from app.models.HabitoUsuario import HabitoUsuario
from app.models.HabitoBase import HabitoBase
from app.models.Usuario import Usuario
from app.models.DiaHabitoSemana import DiaHabitoSemana
from app.models.DiaHabitoMes import DiaHabitoMes
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from datetime import datetime
from app.utils.validar_frequencia import validar_frequencia
from app.utils.verificar_data import validar_formato_data
from app.utils.dia_semana_to_num import converter_numero_para_dia_semana  
from typing import List
from app.exceptions.service_exceptions import ConflictError, AuthError, ServiceError

class HabitoUsuarioService:
    _instance = None

    def __new__(cls, db: Session):
        if cls._instance is None:
            cls._instance = super(HabitoUsuarioService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db: Session):
        if self._initialized:
            return
        self.habito_usuario_repository = HabitoUsuarioRepository(db)
        self.habito_base_repository = HabitoBaseRepository(db)
        self.usuario_repository = UserRepository(db)
        self.categoria_repository = CategoriaRepository(db)
        self.dia_habito_semana_repository = DiaHabitoSemanaRepository(db)
        self.dia_habito_mes_repository = DiaHabitoMesRepository(db)
        self._initialized = True

    def buscar_habitos_usuario(self, usuario_email: str):
        try:
            usuario = self.usuario_repository.buscar_por_email(usuario_email)
            if not usuario:
                raise AuthError("Usuário não encontrado.")
            
            habitos_usuario = self.habito_usuario_repository.buscar_por_email(usuario_email)
            return habitos_usuario
        except AuthError as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro ao buscar hábitos do usuário: {str(e)}")

    def adicionar_habito_usuario(self, descricao: str, habito_base_id: int, usuario_id: int, frequencia: str, data_inicio: datetime = None, vezes_na_semana: int = None, dias_da_semana: list[int] = None, dias_do_mes: list[int] = None):
        try:
            usuario = self.usuario_repository.buscar_por_id(usuario_id)
            if not usuario:
                raise AuthError(f"Usuário com ID {usuario_id} não encontrado.")
            
            habito_base = self.habito_base_repository.buscar_por_id(habito_base_id)
            if not habito_base:
                raise ConflictError(f"Hábito base com ID {habito_base_id} não encontrado.")
            
            if not validar_frequencia(frequencia):
                raise ConflictError(f"Frequência inválida. Opções válidas: 'diario', 'semanal', 'mensal'")
            
            if data_inicio is None:
                raise ConflictError("A data de início é obrigatória")
            
            data_inicio = validar_formato_data(data_inicio)

            novo_habito_usuario = self.habito_usuario_repository.criar_habito_usuario(
                descricao=descricao, 
                habito_base_id=habito_base_id, 
                usuario_id=usuario_id, 
                frequencia=frequencia,  
                data_inicio=data_inicio
            )
            
            if frequencia.lower() in ['semanal', 'diaria'] and dias_da_semana:
                if not isinstance(dias_da_semana, list):
                    raise ConflictError("dias_da_semana deve ser uma lista de números")
                
                for dia_num in dias_da_semana:
                    try:
                        dia_enum = converter_numero_para_dia_semana(dia_num)
                        self.dia_habito_semana_repository.adicionar_dia(
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
                    
                    self.dia_habito_mes_repository.adicionar_dia(
                        habito_id=novo_habito_usuario.id,
                        dia=dia
                    )
            
            return novo_habito_usuario

        except (AuthError, ConflictError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro ao adicionar hábito de usuário: {str(e)}")
    
    def atualizar_habito_usuario(self, habito_usuario_id: int, nova_descricao: str, 
                                novo_habito_base_id: int, novo_usuario_id: int, 
                                nova_frequencia: str, nova_data_inicio: datetime, 
                                nova_vezes_na_semana: int = None, 
                                novos_dias_da_semana: List[int] = None, 
                                novos_dias_do_mes: List[int] = None):
        try:
            habito = self.habito_usuario_repository.buscar_por_id(habito_usuario_id)
            if not habito:
                raise ConflictError("Hábito não encontrado")

            habito.descricao = nova_descricao
            habito.habito_base_id = novo_habito_base_id
            habito.usuario_id = novo_usuario_id
            habito.frequencia = nova_frequencia
            habito.data_inicio = nova_data_inicio

            if nova_frequencia.lower() in ['semanal', 'diaria']:
                habito.vezes_na_semana = nova_vezes_na_semana
                self.dia_habito_semana_repository.remover_por_usuario(novo_usuario_id)
                
                if novos_dias_da_semana:
                    for dia_num in novos_dias_da_semana:
                        dia_enum = converter_numero_para_dia_semana(dia_num)
                        self.dia_habito_semana_repository.adicionar_dia(habito.id, dia_enum)

            if nova_frequencia.lower() == 'mensal':
                self.dia_habito_mes_repository.remover_por_usuario(novo_usuario_id)
                
                if novos_dias_do_mes:
                    for dia in novos_dias_do_mes:
                        if dia < 1 or dia > 31:
                            raise ConflictError(f"Dia do mês inválido: {dia}")
                        self.dia_habito_mes_repository.adicionar_dia(habito.id, dia)

            self.habito_usuario_repository.atualizar_habito_usuario(habito)
            return habito

        except (AuthError, ConflictError) as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro ao atualizar hábito de usuário: {str(e)}")

    def remover_habito_usuario(self, habito_usuario_id: int):
        try:
            habito_usuario = self.habito_usuario_repository.buscar_por_id(habito_usuario_id)
            if not habito_usuario:
                raise ConflictError("Hábito de usuário não encontrado.")
            
            self.habito_usuario_repository.remover_habito_usuario(habito_usuario_id)
        except ConflictError as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro ao remover hábito de usuário: {str(e)}")
        
    def buscar_categorias_usuario(self, usuario_id:int):
        try:
            categorias_usuario = self.categoria_repository.buscar_categorias_por_usuario(usuario_id=usuario_id)
            if not categorias_usuario:
                raise ConflictError("Categorias de hábito não encontradas.")
            return categorias_usuario
        except ConflictError as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro ao buscar categorias de usuário: {str(e)}")
            



