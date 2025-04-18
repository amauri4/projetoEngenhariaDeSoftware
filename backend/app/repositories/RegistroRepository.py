from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from models.RegistroDiario import RegistroDiario
from models.HabitoUsuario import HabitoUsuario

class RegistroDiarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_todos(self):
        try:
            registros = self.db.query(RegistroDiario).all()
            if not registros:
                raise NoResultFound("Nenhum registro encontrado.")
            return registros
        except NoResultFound as e:
            raise Exception(f"Erro ao buscar registros: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar registros: {str(e)}")

    def buscar_por_usuario(self, usuario_id: int):
        try:
            registros = (
                self.db.query(RegistroDiario)
                .join(HabitoUsuario)
                .filter(HabitoUsuario.usuario_id == usuario_id)
                .all()
            )
            if not registros:
                raise NoResultFound("Nenhum registro encontrado para o usuário.")
            return registros
        except NoResultFound as e:
            raise Exception(f"Erro ao buscar registros do usuário: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar registros do usuário: {str(e)}")

    def buscar_concluidos_por_usuario(self, usuario_id: int):
        try:
            registros = (
                self.db.query(RegistroDiario)
                .join(HabitoUsuario)
                .filter(HabitoUsuario.usuario_id == usuario_id, RegistroDiario.concluido == True)
                .all()
            )
            if not registros:
                raise NoResultFound("Nenhum registro concluído encontrado para o usuário.")
            return registros
        except NoResultFound as e:
            raise Exception(f"Erro ao buscar registros concluídos do usuário: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar registros concluídos do usuário: {str(e)}")

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
                raise NoResultFound("Registro não encontrado.")
            registro.concluido = concluido
            self.db.commit()
            return registro
        except NoResultFound as e:
            raise Exception(f"Erro ao atualizar registro: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao atualizar registro: {str(e)}")

    def remover_registro(self, registro_id: int):
        try:
            registro = self.db.query(RegistroDiario).filter_by(id=registro_id).first()
            if not registro:
                raise NoResultFound("Registro não encontrado.")
            self.db.delete(registro)
            self.db.commit()
        except NoResultFound as e:
            raise Exception(f"Erro ao remover registro: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao remover registro: {str(e)}")
