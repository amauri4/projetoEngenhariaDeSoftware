from datetime import datetime
from app.repositories.RegistroRepository import RegistroDiarioRepository
from app.repositories.HabitoUsuarioRepository import HabitoUsuarioRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.utils.verificar_data import validar_formato_data

class RegistroDiarioService:
    _instance = None

    def __new__(cls, db: Session):
        if cls._instance is None:
            cls._instance = super(RegistroDiarioService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db: Session):
        if self._initialized:
            return
        self.registro_diario_repository = RegistroDiarioRepository(db)
        self.habito_usuario_repository = HabitoUsuarioRepository(db)
        self._initialized = True

    def buscar_registros_usuario(self, usuario_id: int):
        try:
            registros = self.registro_diario_repository.buscar_por_usuario(usuario_id)
            return registros
        except Exception as e:
            raise Exception(f"Erro ao buscar registros diários do usuário {usuario_id}: {str(e)}")

    def buscar_registros_concluidos_usuario(self, usuario_id: int):
        try:
            registros_concluidos = self.registro_diario_repository.buscar_concluidos_por_usuario(usuario_id)
            return registros_concluidos
        except Exception as e:
            raise Exception(f"Erro ao buscar registros diários concluídos do usuário {usuario_id}: {str(e)}")

    def criar_registro_diario(self, data: str, habito_id: int, concluido: bool = False):
        try:
            habito_usuario = self.habito_usuario_repository.buscar_por_id(habito_id)
            if not habito_usuario:
                raise NoResultFound("Hábito não encontrado.")
            data = validar_formato_data(data)
            novo_registro = self.registro_diario_repository.criar_registro(data, habito_id, concluido)
            return novo_registro
        except NoResultFound as e:
            raise Exception(f"Erro ao criar registro diário: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro ao criar registro diário: {str(e)}")

    def atualizar_registro_diario(self, registro_id: int, concluido: bool):
        try:
            registro_atualizado = self.registro_diario_repository.atualizar_registro(registro_id, concluido)
            return registro_atualizado
        except Exception as e:
            raise Exception(f"Erro ao atualizar o registro diário {registro_id}: {str(e)}")

    def remover_registro_diario(self, registro_id: int):
        try:
            self.registro_diario_repository.remover_registro(registro_id)
        except Exception as e:
            raise Exception(f"Erro ao remover o registro diário {registro_id}: {str(e)}")

    def buscar_registros_por_data(self, usuario_id: int, data_inicio: datetime = None, data_fim: datetime = None):
        try:
            data_inicio = validar_formato_data(data_inicio)
            data_fim = validar_formato_data(data_fim)
            registros = self.registro_diario_repository.buscar_por_data(usuario_id, data_inicio, data_fim)
            return registros
        except Exception as e:
            raise Exception(f"Erro ao buscar registros por data para o usuário {usuario_id}: {str(e)}")

    def buscar_registros_por_data_especifica(self, usuario_id: int, data_especifica: datetime):
        try:
            data_especifica = validar_formato_data(data_especifica)
            print(f"DATA VALIDADA E AJEITADA: {data_especifica}")
            registros = self.registro_diario_repository.buscar_por_data_especifica(usuario_id, data_especifica)
            return registros
        except Exception as e:
            raise Exception(f"Erro ao buscar registros na data específica para o usuário {usuario_id}: {str(e)}")
