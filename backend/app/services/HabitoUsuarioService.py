from app.repositories.HabitoUsuarioRepository import HabitoUsuarioRepository
from app.repositories.HabitoBaseRepository import HabitoBaseRepository
from app.repositories.UsuarioRepositories import UserRepository
from app.models.HabitoUsuario import HabitoUsuario
from app.models.HabitoBase import HabitoBase
from app.models.Usuario import Usuario
from app.models.DiaHabitoSemana import DiaHabitoSemana
from app.models.DiaHabitoMes import DiaHabitoMes
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from datetime import datetime
from app.utils.validar_frequencia import validar_frequencia

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
        self.dia_habito_semana_repository = DiaHabitoSemana(db)
        self.dia_habito_mes_repository = DiaHabitoMes(db)
        self._initialized = True

    def buscar_habitos_usuario(self, usuario_email: str):
        try:
            usuario = self.usuario_repository.buscar_por_email(usuario_email)
            if not usuario:
                raise NoResultFound("Usuário não encontrado.")
            
            habitos_usuario = self.habito_usuario_repository.buscar_por_email(usuario_email)
            return habitos_usuario
        except NoResultFound as e:
            raise Exception(f"Erro no serviço ao buscar hábitos do usuário: {str(e)}")

    def adicionar_habito_usuario(self, descricao: str, habito_base_id: int, usuario_id: int, frequencia: str, data_inicio: datetime = None, vezes_na_semana: int = None, dias_da_semana: list = None, dias_do_mes: list = None):
        try:
            usuario = self.usuario_repository.buscar_por_id(usuario_id)
            if not usuario:
                raise NoResultFound(f"Usuário com ID {usuario_id} não encontrado.")
            
            habito_base = self.habito_base_repository.buscar_por_id(habito_base_id)
            if not habito_base:
                raise NoResultFound(f"Hábito base com ID {habito_base_id} não encontrado.")
            
            if not validar_frequencia(frequencia):
                raise ValueError(f"Frequência inválida. As opções válidas são: 'diario', 'semanal', 'mensal'.")
            
            if data_inicio is None:
                data_inicio = datetime.now()

            novo_habito_usuario = self.habito_usuario_repository.criar_habito_usuario(
                descricao=descricao, 
                habito_base_id=habito_base_id, 
                usuario_id=usuario_id, 
                frequencia=frequencia,  
                data_inicio=data_inicio
            )
            
            if frequencia.lower() == 'semanal':
                if vezes_na_semana is None:
                    raise ValueError("O número de vezes por semana deve ser especificado quando a frequência for 'semanal'.")
                
                novo_habito_usuario.vezes_na_semana = vezes_na_semana
                if dias_da_semana:
                    for dia in dias_da_semana:
                        dia_habito_semana = DiaHabitoSemana(habito_usuario_id=novo_habito_usuario.id, dia_semana=dia)
                        self.dia_habito_semana_repository.criar(dia_habito_semana)

            elif frequencia.lower() == 'diario':
                if dias_da_semana:
                    for dia in dias_da_semana:
                        dia_habito_semana = DiaHabitoSemana(habito_usuario_id=novo_habito_usuario.id, dia_semana=dia)
                        self.dia_habito_semana_repository.criar(dia_habito_semana)

            elif frequencia.lower() == 'mensal':
                if dias_do_mes:
                    for dia in dias_do_mes:
                        dia_habito_mes = DiaHabitoMes(habito_usuario_id=novo_habito_usuario.id, dia_mes=dia)
                        self.dia_habito_mes_repository.criar(dia_habito_mes)
            
            return novo_habito_usuario

        except NoResultFound as e:
            raise Exception(f"Erro ao adicionar hábito de usuário: {str(e)}")
        except ValueError as e:
            raise Exception(f"Erro de validação: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro ao adicionar hábito de usuário: {str(e)}")
    
    def atualizar_habito_usuario(self, habito_usuario_id: int, nova_descricao: str, novo_habito_base_id: int, novo_usuario_id: int, nova_frequencia: str, nova_data_inicio: datetime, nova_vezes_na_semana: int = None, novos_dias_da_semana: list = None, novos_dias_do_mes: list = None):
        try:
            habito_usuario = self.habito_usuario_repository.buscar_por_id(habito_usuario_id)
            if not habito_usuario:
                raise NoResultFound(f"Hábito de usuário com ID {habito_usuario_id} não encontrado.")
            
            usuario = self.usuario_repository.buscar_por_id(novo_usuario_id)
            if not usuario:
                raise NoResultFound(f"Usuário com ID {novo_usuario_id} não encontrado.")
            
            habito_base = self.habito_base_repository.buscar_por_id(novo_habito_base_id)
            if not habito_base:
                raise NoResultFound(f"Hábito base com ID {novo_habito_base_id} não encontrado.")
            
            if not self.validar_frequencia(nova_frequencia):
                raise ValueError(f"Frequência inválida. As opções válidas são: 'diario', 'semanal', 'mensal'.")
            
            habito_usuario.descricao = nova_descricao
            habito_usuario.habito_base_id = novo_habito_base_id
            habito_usuario.usuario_id = novo_usuario_id
            habito_usuario.frequencia = nova_frequencia
            habito_usuario.data_inicio = nova_data_inicio

            if nova_frequencia.lower() == 'semanal':
                habito_usuario.vezes_na_semana = nova_vezes_na_semana
                if novos_dias_da_semana:
                    self.dia_habito_semana_repository.remover_por_habito_usuario_id(habito_usuario_id)
                    for dia in novos_dias_da_semana:
                        dia_habito_semana = DiaHabitoSemana(habito_usuario_id=habito_usuario.id, dia_semana=dia)
                        self.dia_habito_semana_repository.criar(dia_habito_semana)

            elif nova_frequencia.lower() == 'diario':
                if novos_dias_da_semana:
                    self.dia_habito_semana_repository.remover_por_habito_usuario_id(habito_usuario_id)
                    for dia in novos_dias_da_semana:
                        dia_habito_semana = DiaHabitoSemana(habito_usuario_id=habito_usuario.id, dia_semana=dia)
                        self.dia_habito_semana_repository.criar(dia_habito_semana)

            elif nova_frequencia.lower() == 'mensal':
                if novos_dias_do_mes:
                    self.dia_habito_mes_repository.remover_por_habito_usuario_id(habito_usuario_id)
                    for dia in novos_dias_do_mes:
                        dia_habito_mes = DiaHabitoMes(habito_usuario_id=habito_usuario.id, dia_mes=dia)
                        self.dia_habito_mes_repository.criar(dia_habito_mes)

            self.habito_usuario_repository.atualizar_habito_usuario(habito_usuario)
            return habito_usuario

        except NoResultFound as e:
            raise Exception(f"Erro ao atualizar hábito de usuário: {str(e)}")
        except ValueError as e:
            raise Exception(f"Erro de validação: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro ao atualizar hábito de usuário: {str(e)}")

    def remover_habito_usuario(self, habito_usuario_id: int):
        try:
            habito_usuario = self.habito_usuario_repository.buscar_por_id(habito_usuario_id)
            if not habito_usuario:
                raise NoResultFound("Hábito de usuário não encontrado.")
            
            self.habito_usuario_repository.remover_habito_usuario(habito_usuario_id)
        except NoResultFound as e:
            raise Exception(f"Erro no serviço ao remover hábito de usuário: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro no serviço ao remover hábito: {str(e)}")


