from sqlalchemy.orm import Session
from models.Usuario import Usuario
from sqlalchemy.exc import SQLAlchemyError

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_email(self, email):
        try:
            return self.db.query(Usuario).filter_by(email=email).first()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar usuário por e-mail: {str(e)}")

    def salvar(self, user):
        try:
            self.db.add(user)
            self.db.commit()
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao salvar usuário: {str(e)}")

    def __del__(self):
        self.db.close()
