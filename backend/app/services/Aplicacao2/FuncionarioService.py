from sqlalchemy.orm import Session
from app.models.Aplicacao2.Gerente import Gerente
from app.models.Aplicacao2.Funcionario import Funcionario
from app.repositories.Aplicacao2.GerenteRepository import GerenteRepository
from app.repositories.Aplicacao2.FuncionarioRepository import FuncionarioRepository
from app.repositories.Framework.AtorRepository import AtorRepository 
from app.utils.gerar_verificar_hash import gerar_hash_senha, verificar_senha
from app.exceptions.service_exceptions import ConflictError, AuthError, ServiceError
from app.exceptions.repository_exceptions import NotFoundError

class FuncionarioService:
    _instance = None

    def __new__(cls, db: Session):
        if cls._instance is None:
            cls._instance = super(FuncionarioService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db: Session):
        if self._initialized:
            return
        self.funcionario_repository = FuncionarioRepository(db)
        self.ator_repository = AtorRepository(db)
        self._initialized = True

    def criar_funcionario(self, nome: str, email: str, senha: str, chefe_id: int = None) -> Funcionario:
        try:
            ator_existente = self.ator_repository.buscar_por_email(email)
            if ator_existente:
                raise ConflictError("Já existe um usuário com este e-mail.")

            senha_hash = gerar_hash_senha(senha)
            
            novo_funcionario = self.funcionario_repository.criar_funcionario(
                nome=nome,
                email=email,
                senha_hash=senha_hash,
                chefe_id=chefe_id
            )
            return novo_funcionario
        except (ConflictError, NotFoundError):
            raise
        except Exception as e:
            raise ServiceError(f"Erro inesperado ao criar funcionário: {str(e)}")

    def autenticar_funcionario(self, email: str, senha: str) -> Funcionario:
        try:
            ator = self.ator_repository.buscar_por_email(email)

            if not ator or not verificar_senha(senha, ator.senha_hash) or not isinstance(ator, Funcionario):
                raise AuthError("Credenciais de funcionário inválidas ou usuário não é um funcionário.")
                
            return ator
        except AuthError:
            raise
        except Exception as e:
            raise ServiceError(f"Erro inesperado ao autenticar funcionário: {str(e)}")
