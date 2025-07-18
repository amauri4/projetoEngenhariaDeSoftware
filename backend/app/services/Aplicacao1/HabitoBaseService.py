from app.repositories.Aplicacao1.HabitoBaseRepository import HabitoBaseRepository
from sqlalchemy.orm import Session
from app.exceptions.service_exceptions import ConflictError, AuthError, ServiceError

class HabitoBaseService:
    _instance = None

    def __new__(cls, db: Session):
        if cls._instance is None:
            cls._instance = super(HabitoBaseService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db: Session):
        if self._initialized:
            return
        self.habito_repository = HabitoBaseRepository(db)
        self._initialized = True

    def buscar_habitos_disponiveis(self):
        try:
            habitos_disponiveis = self.habito_repository.buscar_todos()
            return habitos_disponiveis
        except Exception as e:
             raise ServiceError(f"Erro no serviço ao buscar hábitos disponíveis: {str(e)}")

