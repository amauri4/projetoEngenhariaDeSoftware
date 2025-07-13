from sqlalchemy.orm import Session
from app.models.Ator import Ator
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.repository_exceptions  import RepositoryError, NotFoundError

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_email(self, email):
        try:
            return self.db.query(Ator).filter_by(email=email).first()
        
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar usuário por e-mail.") from e

    def buscar_por_id(self, usuario_id: int):
        try:
            usuario = self.db.query(Ator).filter_by(id=usuario_id).first()
            if not usuario:
                raise NotFoundError(f"Usuário com ID '{usuario_id}' não encontrado.")
            return usuario
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar usuário por ID.") from e

    def salvar(self, user):
        try:
            self.db.add(user)
            self.db.commit()
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao salvar usuário.") from e

    def atualizar(self, user: Ator):
        try:
            self.db.merge(user)  
            self.db.commit()
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao atualizar usuário.") from e

    def deletar(self, user: Ator):
        try:
            self.db.delete(user)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao deletar usuário.") from e

    def __del__(self):
        self.db.close()
