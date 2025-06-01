from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from app.models.DiaHabitoMes import DiaHabitoMes
from app.exceptions.repository_exceptions  import RepositoryError, NotFoundError

class DiaHabitoMesRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_todos(self):
        try:
            dias = self.db.query(DiaHabitoMes).all()
            
            if not dias:
                raise NotFoundError("Nenhum dia de hábito mensal encontrado.")
            return dias
        
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError(f"Erro ao buscar dias de hábito mensal: {str(e)}")

    def buscar_por_habito(self, habito_id: int):
        try:
            dias = self.db.query(DiaHabitoMes).filter_by(habito_id=habito_id).all()
            if not dias:
                raise NotFoundError("Nenhum dia encontrado para o hábito informado.")
            return dias
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar dias do hábito.") from e

    def adicionar_dia(self, habito_id: int, dia: int):
        try:
            novo_dia = DiaHabitoMes(habito_id=habito_id, dia=dia)
            self.db.add(novo_dia)
            self.db.commit()
            return novo_dia
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao adicionar dia ao hábito mensal.") from e

    def remover_por_usuario(self, usuario_id: int):
        try:
            dias = self.db.query(DiaHabitoMes)\
                .join(DiaHabitoMes.habito_id)\
                .filter_by(usuario_id=usuario_id)\
                .all()
            
            if not dias:
                raise NotFoundError("Nenhum dia de hábito mensal encontrado para este usuário.")
            
            for dia in dias:
                self.db.delete(dia)
            self.db.commit()
            
            return len(dias)  
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao remover dias por usuário.") from e