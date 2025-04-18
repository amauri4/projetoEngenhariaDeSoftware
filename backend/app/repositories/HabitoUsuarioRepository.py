from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from app.models.HabitoUsuario import HabitoUsuario
from app.models.HabitoBase import HabitoBase
from app.models.Usuario import Usuario

class HabitoUsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_todos(self):
        try:
            habitos_usuario = self.db.query(HabitoUsuario).all()
            if not habitos_usuario:
                raise NoResultFound("Nenhum hábito de usuário encontrado.")
            return habitos_usuario
        except NoResultFound as e:
            raise Exception(f"Erro ao buscar hábitos de usuário: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar hábitos de usuário: {str(e)}")

    def criar_habito_usuario(self, descricao: str, habito_base_id: int, usuario_id: int):
        try:
            habito_base = self.db.query(HabitoBase).filter_by(id=habito_base_id).first()
            if not habito_base:
                raise NoResultFound("Hábito base não encontrado.")
            usuario = self.db.query(Usuario).filter_by(id=usuario_id).first()
            if not usuario:
                raise NoResultFound("Usuário não encontrado.")
            novo_habito_usuario = HabitoUsuario(descricao=descricao, habito_base_id=habito_base_id, usuario_id=usuario_id)
            self.db.add(novo_habito_usuario)
            self.db.commit()
            return novo_habito_usuario
        except NoResultFound as e:
            raise Exception(f"Erro ao criar hábito de usuário: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao criar hábito de usuário: {str(e)}")

    def atualizar_habito_usuario(self, habito_usuario_id: int, nova_descricao: str, novo_habito_base_id: int, novo_usuario_id: int):
        try:
            habito_usuario = self.db.query(HabitoUsuario).filter_by(id=habito_usuario_id).first()
            if not habito_usuario:
                raise NoResultFound("Hábito de usuário não encontrado.")
            habito_base = self.db.query(HabitoBase).filter_by(id=novo_habito_base_id).first()
            if not habito_base:
                raise NoResultFound("Hábito base não encontrado.")
            usuario = self.db.query(Usuario).filter_by(id=novo_usuario_id).first()
            if not usuario:
                raise NoResultFound("Usuário não encontrado.")
            habito_usuario.descricao = nova_descricao
            habito_usuario.habito_base_id = novo_habito_base_id
            habito_usuario.usuario_id = novo_usuario_id
            self.db.commit()
            return habito_usuario
        except NoResultFound as e:
            raise Exception(f"Erro ao atualizar hábito de usuário: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao atualizar hábito de usuário: {str(e)}")

    def remover_habito_usuario(self, habito_usuario_id: int):
        try:
            habito_usuario = self.db.query(HabitoUsuario).filter_by(id=habito_usuario_id).first()
            if not habito_usuario:
                raise NoResultFound("Hábito de usuário não encontrado.")
            self.db.delete(habito_usuario)
            self.db.commit()
        except NoResultFound as e:
            raise Exception(f"Erro ao remover hábito de usuário: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao remover hábito de usuário: {str(e)}")

    def buscar_por_email(self, email: str):
        try:
            usuario = self.db.query(Usuario).filter_by(email=email).first()
            if not usuario:
                raise NoResultFound("Usuário não encontrado.")
            
            habitos_usuario = self.db.query(HabitoUsuario).filter_by(usuario_id=usuario.id).all()
            if not habitos_usuario:
                raise NoResultFound("Nenhum hábito encontrado para o usuário.")
            
            return habitos_usuario
        except NoResultFound as e:
            raise Exception(f"Erro ao buscar hábitos por e-mail: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar hábitos por e-mail: {str(e)}")
