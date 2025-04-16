from models.Usuario import Usuario
from database.session import get_db  

class UserRepository:
    def __init__(self):
        self.db = next(get_db())  

    def find_by_email(self, email):
        return self.db.query(Usuario).filter_by(email=email).first()

    def save(self, user):
        self.db.add(user)
        self.db.commit()
        return user

    def __del__(self):
        self.db.close()
