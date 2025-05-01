from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from app.models.DiaHabitoSemana import DiaHabitoSemana, DiaSemanaEnum

class DiaHabitoSemanaRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_todos(self):
        try:
            dias = self.db.query(DiaHabitoSemana).all()
            if not dias:
                raise NoResultFound("Nenhum dia de hábito semanal encontrado.")
            return dias
        except NoResultFound as e:
            raise Exception(f"Erro ao buscar dias de hábito semanal: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar dias de hábito semanal: {str(e)}")

    def buscar_por_habito(self, habito_id: int):
        try:
            dias = self.db.query(DiaHabitoSemana).filter_by(habito_id=habito_id).all()
            if not dias:
                raise NoResultFound("Nenhum dia encontrado para o hábito informado.")
            return dias
        except NoResultFound as e:
            raise Exception(f"Erro ao buscar dias do hábito: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar dias do hábito: {str(e)}")

    def adicionar_dia(self, habito_id: int, dia: DiaSemanaEnum):
        try:
            novo_dia = DiaHabitoSemana(habito_id=habito_id, dia=dia)
            self.db.add(novo_dia)
            self.db.commit()
            return novo_dia
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao adicionar dia ao hábito semanal: {str(e)}")

    def remover_dia(self, dia_id: int):
        try:
            dia = self.db.query(DiaHabitoSemana).filter_by(id=dia_id).first()
            if not dia:
                raise NoResultFound("Dia não encontrado.")
            self.db.delete(dia)
            self.db.commit()
        except NoResultFound as e:
            raise Exception(f"Erro ao remover dia: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao remover dia: {str(e)}")
