from sqlalchemy.orm import Session
from app.models.Aplicacao3.Instrutor import Instrutor
from app.repositories.Aplicacao3.IntrutorRepository import InstrutorRepository
from app.repositories.Framework.AtorRepository import AtorRepository
from app.utils.gerar_verificar_hash import gerar_hash_senha, verificar_senha
from app.exceptions.service_exceptions import ConflictError, AuthError, ServiceError
from app.exceptions.repository_exceptions import NotFoundError

class InstrutorService:
    _instance = None

    def __new__(cls, db: Session):
        if cls._instance is None:
            cls._instance = super(InstrutorService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db: Session):
        if self._initialized:
            return
        self.instrutor_repository = InstrutorRepository(db)
        self.ator_repository = AtorRepository(db)
        self._initialized = True

    def criar_instrutor(self, nome: str, email: str, senha: str) -> Instrutor:
        try:
            ator_existente = self.ator_repository.buscar_por_email(email)
            if ator_existente:
                raise ConflictError("Já existe um usuário com este e-mail.")
            senha_hash = gerar_hash_senha(senha)
            novo_instrutor = self.instrutor_repository.criar_instrutor(
                nome=nome,
                email=email,
                senha_hash=senha_hash
            )
            return novo_instrutor
        except ConflictError:
            raise
        except Exception as e:
            raise ServiceError(f"Erro inesperado ao criar instrutor: {str(e)}")

    def autenticar_instrutor(self, email: str, senha: str) -> Instrutor:
        try:
            ator = self.ator_repository.buscar_por_email(email)
            if not ator or not verificar_senha(senha, ator.senha_hash) or not isinstance(ator, Instrutor):
                raise AuthError("Credenciais de instrutor inválidas ou usuário não é um instrutor.")
            return ator
        except AuthError:
            raise
        except Exception as e:
            raise ServiceError(f"Erro inesperado ao autenticar instrutor: {str(e)}")
