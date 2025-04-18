from app.repositories.UsuarioRepositories import UserRepository
from app.models.Usuario import Usuario
from sqlalchemy.orm import Session
from app.utils.gerar_verificar_hash import gerar_hash_senha, verificar_senha

class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def criar_usuario(self, nome: str, email: str, senha: str):
        usuario_existente = self.user_repository.buscar_por_email(email)
        if usuario_existente:
            raise Exception("Já existe um usuário com este e-mail.")

        senha_hash = gerar_hash_senha(senha)
        novo_usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash)
        return self.user_repository.salvar(novo_usuario)

    def autenticar_usuario(self, email: str, senha: str):
        usuario = self.user_repository.buscar_por_email(email)
        if not usuario or not verificar_senha(senha, usuario.senha_hash):
            raise Exception("Credenciais inválidas.")
        return usuario
