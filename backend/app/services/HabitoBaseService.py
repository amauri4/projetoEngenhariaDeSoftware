from app.repositories.HabitoBaseRepository import HabitoBaseRepository
from sqlalchemy.orm import Session

class HabitoBaseService:
    def __init__(self, db: Session):
        self.habito_repository = HabitoBaseRepository(db)

    def buscar_habitos_disponiveis(self):
        try:
            habitos_disponiveis = self.habito_repository.buscar_todos()
            return habitos_disponiveis
        except Exception as e:
            raise Exception(f"Erro no serviço ao buscar hábitos: {str(e)}")
