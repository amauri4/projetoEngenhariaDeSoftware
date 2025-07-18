from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.repositories.Aplicacao1.DiaHabitoMesRepository import DiaHabitoMesRepository
from app.models.Aplicacao1.DiaHabitoMes import DiaHabitoMes
from app.exceptions.service_exceptions import ConflictError, AuthError, ServiceError

class DiaHabitoMesService:
    _instance = None

    def __new__(cls, db: Session):
        if cls._instance is None:
            cls._instance = super(DiaHabitoMesService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, db: Session):
        if self._initialized:
            return
        self.repository = DiaHabitoMesRepository(db)
        self._initialized = True

    def buscar_todos(self):
        try:
            return self.repository.buscar_todos()
        except Exception as e:
            raise ServiceError(f"Erro ao buscar dias do hábito mensal: {str(e)}")

    def buscar_por_habito(self, habito_id: int):
        try:
            return self.repository.buscar_por_habito(habito_id)
        except Exception as e:
            raise ServiceError(f"Erro ao buscar dias do hábito mensal: {str(e)}")

    def adicionar_dia(self, habito_id: int, dia: int):
        try:
            if dia < 1 or dia > 31:
                raise ServiceError("Dia do mês deve estar entre 1 e 31")
                
            return self.repository.adicionar_dia(habito_id, dia)
        except ServiceError as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro ao adicionar dia ao hábito mensal: {str(e)}")

    def adicionar_varios_dias(self, habito_id: int, dias: list[int]):
        try:
            dias_adicionados = []
            for dia in dias:
                if dia < 1 or dia > 31:
                    raise ValueError(f"Dia {dia} inválido. O dia do mês deve estar entre 1 e 31")
                
                novo_dia = self.repository.adicionar_dia(habito_id, dia)
                dias_adicionados.append(novo_dia)
            
            return dias_adicionados
        except ServiceError as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro ao adicionar dias ao hábito mensal: {str(e)}")

    def remover_dia_por_id(self, dia_id: int):
        try:
            self.repository.remover_dia(dia_id)
        except Exception as e:
            raise ServiceError(f"Erro ao remover dia do hábito mensal: {str(e)}")

    def remover_dia_por_habito_e_dia(self, habito_id: int, dia: int):
        try:
            dias = self.repository.buscar_por_habito(habito_id)
            dia_para_remover = next((d for d in dias if d.dia == dia), None)
            
            if not dia_para_remover:
                raise NoResultFound("Dia não encontrado para este hábito")
                
            self.repository.remover_dia(dia_para_remover.id)
        except ServiceError as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro ao remover dia do hábito mensal: {str(e)}")

    def remover_todos_por_habito(self, habito_id: int):
        try:
            dias = self.repository.buscar_por_habito(habito_id)
            if not dias:
                raise ServiceError("Nenhum dia encontrado para este hábito")
            
            for dia in dias:
                self.repository.remover_dia(dia.id)
        except ServiceError as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Erro ao remover dias do hábito mensal: {str(e)}")