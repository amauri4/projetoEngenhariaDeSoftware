from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.repositories.DiaHabitoSemanaRepository import DiaHabitoSemanaRepository
from app.models.DiaHabitoSemana import DiaHabitoSemana, DiaSemanaEnum
from app.exceptions.service_exceptions import ConflictError, AuthError, ServiceError

class DiaHabitoSemanaService:
    def __init__(self, db: Session):
        self.repository = DiaHabitoSemanaRepository(db)
        self.dia_map = {
            1: DiaSemanaEnum.segunda,
            2: DiaSemanaEnum.terca,
            3: DiaSemanaEnum.quarta,
            4: DiaSemanaEnum.quinta,
            5: DiaSemanaEnum.sexta,
            6: DiaSemanaEnum.sabado,
            7: DiaSemanaEnum.domingo
        }

    def buscar_todos(self):
        try:
            return self.repository.buscar_todos()
        except Exception as e:
            raise ServiceError(f"Erro ao buscar dias de hábito semanal: {str(e)}")

    def buscar_por_habito(self, habito_id: int):
        try:
            return self.repository.buscar_por_habito(habito_id)
        except Exception as e:
            raise ServiceError(f"Erro ao buscar dias do hábito semanal: {str(e)}")

    def adicionar_dia(self, habito_id: int, dia: str):
        try:
            dia_enum = DiaSemanaEnum[dia.upper()]
            return self.repository.adicionar_dia(habito_id, dia_enum)
        except KeyError:
            valid_days = [e.name for e in DiaSemanaEnum]
            raise ServiceError(f"Dia da semana inválido. Opções válidas: {valid_days}")
        except Exception as e:
            raise ServiceError(f"Erro ao adicionar dia ao hábito semanal: {str(e)}")

    def adicionar_varios_dias(self, habito_id: int, dias: list[int]):
        try:
            dias_adicionados = []
            for dia_num in dias:
                try:
                    dia_enum = self.dia_map.get(dia_num)
                    if not dia_enum:
                        raise ServiceError(f"Valor {dia_num} inválido. Dias válidos: {list(self.dia_map.keys())}")
                    novo_dia = self.repository.adicionar_dia(habito_id, dia_enum)
                    dias_adicionados.append(novo_dia)
                except ServiceError as ve:
                    raise ve
            return dias_adicionados
        except Exception as e:
            raise ServiceError(f"Erro ao adicionar dias ao hábito semanal: {str(e)}")
        
    def remover_dia_por_id(self, dia_id: int):
        try:
            self.repository.remover_dia(dia_id)
        except Exception as e:
            raise ServiceError(f"Erro ao remover dia do hábito semanal: {str(e)}")

    def remover_dia_por_habito_e_dia(self, habito_id: int, dia_num: int):
        try:
            dia_enum = self.dia_map.get(dia_num)
            if not dia_enum:
                raise ServiceError(f"Dia da semana inválido. Use valores inteiros de 1 a 7, onde: {list(self.dia_map.keys())}")

            dias = self.repository.buscar_por_habito(habito_id)
            dia_para_remover = next((d for d in dias if d.dia == dia_enum), None)

            if not dia_para_remover:
                raise ServiceError("Dia não encontrado para este hábito")

            self.repository.remover_dia(dia_para_remover.id)

        except ServiceError as se:
            raise se
        except Exception as e:
            raise ServiceError(f"Erro ao remover dia do hábito semanal: {str(e)}")

    def remover_todos_por_habito(self, habito_id: int):
        try:
            dias = self.repository.buscar_por_habito(habito_id)
            if not dias:
                raise ServiceError("Nenhum dia encontrado para este hábito")

            for dia in dias:
                self.repository.remover_dia(dia.id)
        except ServiceError as se:
            raise se
        except Exception as e:
            raise ServiceError(f"Erro ao remover dias do hábito semanal: {str(e)}")