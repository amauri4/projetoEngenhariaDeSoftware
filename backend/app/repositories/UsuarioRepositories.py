from sqlalchemy.orm import Session
from models.Usuario import Usuario
from database.session import get_db  

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_email(self, email):
        return self.db.query(Usuario).filter_by(email=email).first()

    def salvar(self, user):
        self.db.add(user)
        self.db.commit()
        return user

    def __del__(self):
        self.db.close()
