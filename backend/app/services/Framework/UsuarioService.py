from app.repositories.Framework.AtorRepository import UserRepository
from app.models.Aplicacao1.UsuarioPessoal import UsuarioPessoal
from sqlalchemy.orm import Session
from app.utils.gerar_verificar_hash import gerar_hash_senha, verificar_senha
from app.exceptions.service_exceptions import ConflictError, AuthError, ServiceError

class UserService:
    _instance = None

    def __new__(cls, db: Session):
        if cls._instance is None:
            cls._instance = super(UserService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db: Session):
        if self._initialized:
            return
        self.user_repository = UserRepository(db)
        self._initialized = True

    def criar_usuario(self, usuario: UsuarioPessoal):
        try:
            usuario_existente = self.user_repository.buscar_por_email(usuario.email)
            if usuario_existente:
                raise ConflictError("Já existe um usuário com este e-mail.")

            senha_hash = gerar_hash_senha(usuario.senha_hash)
            novo_usuario = UsuarioPessoal(
                nome=usuario.nome,
                email=usuario.email,
                senha_hash=senha_hash
            )
            return self.user_repository.salvar(novo_usuario)

        except ConflictError:
            raise
        except Exception as e:
            raise ServiceError(f"Erro inesperado ao criar usuário: {str(e)}")



    def autenticar_usuario(self, email: str, senha: str):
        try:
            usuario = self.user_repository.buscar_por_email(email)
            if not usuario or not verificar_senha(senha, usuario.senha_hash):
                raise AuthError("Credenciais inválidas.")
            return usuario
        except AuthError:
            raise
        except Exception as e:
            raise ServiceError(f"Erro inesperado ao autenticar usuário: {str(e)}")
