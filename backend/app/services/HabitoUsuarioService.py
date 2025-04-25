from app.repositories.HabitoUsuarioRepository import HabitoUsuarioRepository
from app.repositories.HabitoBaseRepository import HabitoBaseRepository
from app.repositories.UsuarioRepositories import UserRepository
from app.models.HabitoUsuario import HabitoUsuario
from app.models.HabitoBase import HabitoBase
from app.models.Usuario import Usuario
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

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

    def adicionar_habito_usuario(self, descricao: str, habito_base_id: int, usuario_id: int):
        try:
            usuario = self.usuario_repository.buscar_por_id(usuario_id)
            if not usuario:
                raise NoResultFound("Usuário não encontrado.")
            
            habito_base = self.habito_base_repository.buscar_por_id(habito_base_id)
            if not habito_base:
                raise NoResultFound("Hábito base não encontrado.")
            
            novo_habito_usuario = self.habito_usuario_repository.criar_habito_usuario(descricao, habito_base_id, usuario_id)
            return novo_habito_usuario
        except NoResultFound as e:
            raise Exception(f"Erro no serviço ao adicionar hábito ao usuário: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro no serviço ao adicionar hábito: {str(e)}")

    def atualizar_habito_usuario(self, habito_usuario_id: int, nova_descricao: str, novo_habito_base_id: int, novo_usuario_id: int):
        try:
            habito_usuario = self.habito_usuario_repository.buscar_por_id(habito_usuario_id)
            if not habito_usuario:
                raise NoResultFound("Hábito de usuário não encontrado.")
            
            usuario = self.usuario_repository.buscar_por_id(novo_usuario_id)
            if not usuario:
                raise NoResultFound("Usuário não encontrado.")
            
            habito_base = self.habito_base_repository.buscar_por_id(novo_habito_base_id)
            if not habito_base:
                raise NoResultFound("Hábito base não encontrado.")
            
            habito_usuario.descricao = nova_descricao
            habito_usuario.habito_base_id = novo_habito_base_id
            habito_usuario.usuario_id = novo_usuario_id
            self.habito_usuario_repository.atualizar_habito_usuario(habito_usuario)
            return habito_usuario
        except NoResultFound as e:
            raise Exception(f"Erro no serviço ao atualizar hábito de usuário: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro no serviço ao atualizar hábito: {str(e)}")

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
