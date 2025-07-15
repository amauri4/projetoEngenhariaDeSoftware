from sqlalchemy.orm import Session
from app.models.Aplicacao3.Aluno import Aluno
from app.repositories.Aplicacao3.AlunoRepository import AlunoRepository
from app.repositories.AtorRepository import UserRepository
from app.utils.gerar_verificar_hash import gerar_hash_senha, verificar_senha
from app.exceptions.service_exceptions import ConflictError, AuthError, ServiceError
from app.exceptions.repository_exceptions import NotFoundError

class AlunoService:
    _instance = None

    def __new__(cls, db: Session):
        if cls._instance is None:
            cls._instance = super(AlunoService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db: Session):
        if self._initialized:
            return
        self.aluno_repository = AlunoRepository(db)
        self.ator_repository = UserRepository(db)
        self._initialized = True

    def criar_aluno(self, nome: str, email: str, senha: str, instrutor_id: int = None) -> Aluno:
        try:
            ator_existente = self.ator_repository.buscar_por_email(email)
            if ator_existente:
                raise ConflictError("Já existe um usuário com este e-mail.")
            senha_hash = gerar_hash_senha(senha)
            novo_aluno = self.aluno_repository.criar_aluno(
                nome=nome,
                email=email,
                senha_hash=senha_hash,
                instrutor_id=instrutor_id
            )
            return novo_aluno
        except (ConflictError, NotFoundError):
            raise
        except Exception as e:
            raise ServiceError(f"Erro inesperado ao criar aluno: {str(e)}")

    def autenticar_aluno(self, email: str, senha: str) -> Aluno:
        try:
            ator = self.ator_repository.buscar_por_email(email)
            if not ator or not verificar_senha(senha, ator.senha_hash) or not isinstance(ator, Aluno):
                raise AuthError("Credenciais de aluno inválidas ou usuário não é um aluno.")
            return ator
        except AuthError:
            raise
        except Exception as e:
            raise ServiceError(f"Erro inesperado ao autenticar aluno: {str(e)}")
