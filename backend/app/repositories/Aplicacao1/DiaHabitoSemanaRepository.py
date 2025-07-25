from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from app.models.Aplicacao1.DiaHabitoSemana import DiaHabitoSemana, DiaSemanaEnum
from app.exceptions.repository_exceptions  import RepositoryError, NotFoundError

class DiaHabitoSemanaRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_todos(self):
        try:
            dias = self.db.query(DiaHabitoSemana).all()
            if not dias:
                raise NotFoundError("Nenhum dia de hábito semanal encontrado.")
            return dias
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar dias de hábito semanal.") from e

    def buscar_por_habito(self, habito_id: int):
        try:
            dias = self.db.query(DiaHabitoSemana).filter_by(habito_id=habito_id).all()
            if not dias:
                raise NotFoundError("Nenhum dia encontrado para o hábito informado.")
            return dias
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar dias do hábito.") from e


    def adicionar_dia(self, habito_id: int, dia: DiaSemanaEnum):
        try:
            novo_dia = DiaHabitoSemana(habito_id=habito_id, dia=dia)
            self.db.add(novo_dia)
            self.db.commit()
            return novo_dia
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao adicionar dia ao hábito semanal.") from e

    def remover_dia(self, dia_id: int):
        try:
            dia = self.db.query(DiaHabitoSemana).filter_by(id=dia_id).first()
            if not dia:
                raise NotFoundError("Dia não encontrado.")
            self.db.delete(dia)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao remover dia.") from e
        
    def remover_por_usuario(self, usuario_id: int):
        try:
            dias = self.db.query(DiaHabitoSemana)\
                .join(DiaHabitoSemana.habito_id)\
                .filter_by(usuario_id=usuario_id)\
                .all()
            
            if not dias:
                raise NotFoundError("Nenhum dia de hábito semanal encontrado para este usuário.")
            
            for dia in dias:
                self.db.delete(dia)
            self.db.commit()
            
            return len(dias)  
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao remover dias por usuário.") from e
