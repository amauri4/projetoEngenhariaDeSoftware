from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from app.models.HabitoUsuario import HabitoUsuario
from app.models.HabitoBase import HabitoBase
from app.models.Usuario import Usuario
from app.models.DiaHabitoSemana import DiaHabitoSemana, DiaSemanaEnum
from app.models.enums.frequencia_enums import FrequenciaEnum

class HabitoUsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_todos(self):
        try:
            habitos_usuario = self.db.query(HabitoUsuario).all()
            if not habitos_usuario:
                raise NoResultFound("Nenhum hábito de usuário encontrado.")
            return habitos_usuario
        except (NoResultFound, SQLAlchemyError) as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar hábitos de usuário: {str(e)}")

    def criar_habito_usuario(
        self,
        descricao: str,
        habito_base_id: int,
        usuario_id: int,
        frequencia: FrequenciaEnum,
        data_inicio: datetime,
        quantidade_semanal: int = None,
        dias_da_semana: list[str] = None  
    ):
        try:
            habito_base = self.db.query(HabitoBase).filter_by(id=habito_base_id).first()
            usuario = self.db.query(Usuario).filter_by(id=usuario_id).first()
            if not habito_base or not usuario:
                raise NoResultFound("Hábito base ou usuário não encontrado.")

            novo_habito = HabitoUsuario(
                descricao=descricao,
                habito_base_id=habito_base_id,
                usuario_id=usuario_id,
                frequencia=frequencia,
                data_inicio=data_inicio,
                vezes_na_semana=quantidade_semanal
            )

            self.db.add(novo_habito)
            self.db.flush()  

            if frequencia == FrequenciaEnum.diaria and dias_da_semana:
                for dia in dias_da_semana:
                    dia_enum = DiaSemanaEnum[dia]
                    self.db.add(DiaHabitoSemana(habito_id=novo_habito.id, dia=dia_enum))

            self.db.commit()
            return novo_habito
        except (NoResultFound, SQLAlchemyError, KeyError) as e:
            self.db.rollback()
            raise Exception(f"Erro ao criar hábito de usuário: {str(e)}")

    def atualizar_habito_usuario(
        self,
        habito_usuario_id: int,
        nova_descricao: str,
        novo_habito_base_id: int,
        novo_usuario_id: int,
        nova_data_inicio: datetime,
        nova_frequencia: FrequenciaEnum,
        nova_quantidade_semanal: int = None,
        novos_dias_da_semana: list[str] = None
    ):
        try:
            habito = self.db.query(HabitoUsuario).filter_by(id=habito_usuario_id).first()
            if not habito:
                raise NoResultFound("Hábito de usuário não encontrado.")

            habito.descricao = nova_descricao
            habito.habito_base_id = novo_habito_base_id
            habito.usuario_id = novo_usuario_id
            habito.frequencia = nova_frequencia
            habito.data_inicio = nova_data_inicio
            habito.vezes_na_semana = nova_quantidade_semanal

            if nova_frequencia == FrequenciaEnum.diaria:
                self.db.query(DiaHabitoSemana).filter_by(habito_id=habito.id).delete()
                for dia in novos_dias_da_semana or []:
                    dia_enum = DiaSemanaEnum[dia]
                    self.db.add(DiaHabitoSemana(habito_id=habito.id, dia=dia_enum))
            else:
                self.db.query(DiaHabitoSemana).filter_by(habito_id=habito.id).delete()

            self.db.commit()
            return habito
        except (NoResultFound, SQLAlchemyError, KeyError) as e:
            self.db.rollback()
            raise Exception(f"Erro ao atualizar hábito de usuário: {str(e)}")

    def remover_habito_usuario(self, habito_usuario_id: int):
        try:
            habito = self.db.query(HabitoUsuario).filter_by(id=habito_usuario_id).first()
            if not habito:
                raise NoResultFound("Hábito de usuário não encontrado.")
            self.db.delete(habito)
            self.db.commit()
        except (NoResultFound, SQLAlchemyError) as e:
            self.db.rollback()
            raise Exception(f"Erro ao remover hábito de usuário: {str(e)}")

    def buscar_por_email(self, email: str):
        try:
            usuario = self.db.query(Usuario).filter_by(email=email).first()
            if not usuario:
                raise NoResultFound("Usuário não encontrado.")
            habitos = self.db.query(HabitoUsuario).filter_by(usuario_id=usuario.id).all()
            if not habitos:
                raise NoResultFound("Nenhum hábito encontrado para o usuário.")
            return habitos
        except (NoResultFound, SQLAlchemyError) as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar hábitos por e-mail: {str(e)}")

    def buscar_por_id(self, habito_usuario_id: int):
        try:
            habito = self.db.query(HabitoUsuario).filter_by(id=habito_usuario_id).all()
            if not habito:
                raise NoResultFound("Hábito de usuário não encontrado.")
            return habito
        except (NoResultFound, SQLAlchemyError) as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar hábito de usuário por ID: {str(e)}")
    
    def buscar_por_usuario(self, user_id: int) -> list[HabitoUsuario]:
        return self.db.query(HabitoUsuario).filter(HabitoUsuario.usuario_id == user_id).all()
