from sqlalchemy.orm import Session
from app.models.Aplicacao2.Gerente import Gerente
from app.models.Aplicacao2.Funcionario import Funcionario
from app.repositories.Aplicacao2.GerenteRepository import GerenteRepository
from app.repositories.Aplicacao2.FuncionarioRepository import FuncionarioRepository
from app.repositories.UsuarioRepositories import UserRepository 
from app.utils.gerar_verificar_hash import gerar_hash_senha, verificar_senha
from app.exceptions.service_exceptions import ConflictError, AuthError, ServiceError
from app.exceptions.repository_exceptions import NotFoundError

class GerenteService:
    _instance = None

    def __new__(cls, db: Session):
        if cls._instance is None:
            cls._instance = super(GerenteService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db: Session):
        if self._initialized:
            return
        self.gerente_repository = GerenteRepository(db)
        self.ator_repository = UserRepository(db) 
        self._initialized = True

    def criar_gerente(self, nome: str, email: str, senha: str) -> Gerente:
        try:
            ator_existente = self.ator_repository.buscar_por_email(email)
            if ator_existente:
                raise ConflictError("Já existe um usuário com este e-mail.")

            senha_hash = gerar_hash_senha(senha)
            
            novo_gerente = self.gerente_repository.criar_gerente(
                nome=nome,
                email=email,
                senha_hash=senha_hash
            )
            return novo_gerente
        except ConflictError:
            raise
        except Exception as e:
            raise ServiceError(f"Erro inesperado ao criar gerente: {str(e)}")

    def autenticar_gerente(self, email: str, senha: str) -> Gerente:
        try:
            ator = self.ator_repository.buscar_por_email(email)
            
            if not ator or not verificar_senha(senha, ator.senha_hash) or not isinstance(ator, Gerente):
                raise AuthError("Credenciais de gerente inválidas ou usuário não é um gerente.")
                
            return ator
        except AuthError:
            raise
        except Exception as e:
            raise ServiceError(f"Erro inesperado ao autenticar gerente: {str(e)}")