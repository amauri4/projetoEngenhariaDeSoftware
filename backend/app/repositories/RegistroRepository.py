from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from app.models.RegistroDiario import RegistroDiario
from app.models.HabitoUsuario import HabitoUsuario
from app.exceptions.repository_exceptions  import RepositoryError, NotFoundError
from datetime import datetime

class RegistroDiarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_todos(self):
        try:
            registros = self.db.query(RegistroDiario).all()

            if not registros:
                raise NotFoundError("Nenhum registro encontrado.")
            return registros
        
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar registros.") from e

    def buscar_por_usuario(self, usuario_id: int):
        try:
            registros = (
                self.db.query(RegistroDiario)
                .join(HabitoUsuario)
                .filter(HabitoUsuario.usuario_id == usuario_id)
                .all()
            )
            if not registros:
                raise NotFoundError("Nenhum registro encontrado para o usuário.")
            return registros
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar registros do usuário.") from e

    def buscar_concluidos_por_usuario(self, usuario_id: int):
        try:
            registros = (
                self.db.query(RegistroDiario)
                .join(HabitoUsuario)
                .filter(HabitoUsuario.usuario_id == usuario_id, RegistroDiario.concluido == True)
                .all()
            )
            if not registros:
                raise NotFoundError("Nenhum registro concluído encontrado para o usuário.")
            return registros
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar registros concluídos do usuário.") from e

    def criar_registro(self, data, habito_id: int, concluido=False):
        try:
            habito = self.db.query(HabitoUsuario).filter_by(id=habito_id).first()
            if not habito:
                raise NoResultFound("Hábito não encontrado.")
            novo_registro = RegistroDiario(data=data, habito_id=habito_id, concluido=concluido)
            self.db.add(novo_registro)
            self.db.commit()
            return novo_registro
        except NoResultFound as e:
            raise Exception(f"Erro ao criar registro: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao criar registro: {str(e)}")

    def atualizar_registro(self, registro_id: int, concluido: bool):
        try:
            registro = self.db.query(RegistroDiario).filter_by(id=registro_id).first()
            if not registro:
                raise NotFoundError("Registro não encontrado.")
            registro.concluido = concluido
            self.db.commit()
            return registro
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao atualizar registro.") from e

    def remover_registro(self, registro_id: int):
        try:
            registro = self.db.query(RegistroDiario).filter_by(id=registro_id).first()
            if not registro:
                raise NotFoundError("Registro não encontrado.")
            self.db.delete(registro)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao remover registro.") from e
    
    def buscar_por_data(self, usuario_id: int, data_inicio: datetime = None, data_fim: datetime = None):
        try:
            query = self.db.query(RegistroDiario).join(HabitoUsuario).filter(HabitoUsuario.usuario_id == usuario_id)
            
            if data_inicio:
                query = query.filter(RegistroDiario.data >= data_inicio)
            
            if data_fim:
                query = query.filter(RegistroDiario.data <= data_fim)
            
            registros = query.all()

            if not registros:
                raise NotFoundError("Nenhum registro encontrado para o filtro de data.")
            
            return registros
        
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar registros por data.") from e

    def buscar_por_data_especifica(self, usuario_id: int, data_especifica: datetime):
        try:
            registros = (
                self.db.query(RegistroDiario)
                .join(HabitoUsuario)
                .filter(HabitoUsuario.usuario_id == usuario_id, RegistroDiario.data == data_especifica)
                .all()
            )
            if not registros:
                raise NotFoundError(f"Nenhum registro encontrado para a data {data_especifica.strftime('%Y-%m-%d')}.")
            return registros
        
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar registros por data específica.") from e