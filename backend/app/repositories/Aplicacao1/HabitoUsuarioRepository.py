from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from app.models.Aplicacao1.InstanciaDeHabito import InstanciaDeHabito
from app.models.Aplicacao1.HabitoBase import HabitoBase
from app.models.Aplicacao1.UsuarioPessoal import UsuarioPessoal
from app.models.Aplicacao1.DiaHabitoSemana import DiaHabitoSemana, DiaSemanaEnum
from app.models.Aplicacao1.InstanciaDeHabito import FrequenciaEnum
from app.exceptions.repository_exceptions  import RepositoryError, NotFoundError

class HabitoUsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_todos(self):
        try:
            habitos_usuario = self.db.query(InstanciaDeHabito).all()
            if not habitos_usuario:
                raise NotFoundError("Nenhum hábito de usuário encontrado.")
            return habitos_usuario
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar hábitos de usuário.") from e

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
            usuario = self.db.query(UsuarioPessoal).filter_by(id=usuario_id).first()

            if not habito_base:
                raise NotFoundError(f"Hábito base com ID {habito_base_id} não encontrado.")

            novo_habito = InstanciaDeHabito(
                descricao=descricao,
                habito_base_id=habito_base_id,
                ator_id=usuario_id,
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
        except SQLAlchemyError as e:
            print(f'\n\n{str(e)}\n\n')
            self.db.rollback()
            raise RepositoryError("Erro ao criar hábito de usuário.") from e

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
            habito = self.db.query(InstanciaDeHabito).filter_by(id=habito_usuario_id).first()
            if not habito:
                raise NotFoundError(f"Hábito de usuário com ID {habito_usuario_id} não encontrado.")

            habito.descricao = nova_descricao
            habito.habito_base_id = novo_habito_base_id
            habito.ator_id = novo_usuario_id
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
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao atualizar hábito de usuário.") from e
        
    def remover_habito_usuario(self, habito_usuario_id: int):
        try:
            habito = self.db.query(InstanciaDeHabito).filter_by(id=habito_usuario_id).first()
            if not habito:
                raise NotFoundError(f"Hábito de usuário com ID {habito_usuario_id} não encontrado.")
            self.db.delete(habito)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao remover hábito de usuário.") from e

    def buscar_por_email(self, email: str):
        try:
            usuario = self.db.query(UsuarioPessoal).filter_by(email=email).first()
            if not usuario:
                raise NotFoundError(f"Usuário com e-mail {email} não encontrado.")
            habitos = self.db.query(InstanciaDeHabito).filter_by(ator_id=usuario.id).all()
            if not habitos:
                raise NotFoundError(f"Nenhum hábito encontrado para o usuário com e-mail {email}.")
            return habitos
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar hábitos por e-mail.") from e

    def buscar_por_id(self, habito_usuario_id: int):
        try:
            habito = self.db.query(InstanciaDeHabito).filter_by(id=habito_usuario_id).all()
            if not habito:
                raise NotFoundError(f"Hábito de usuário com ID {habito_usuario_id} não encontrado.")
            return habito
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError(f"Erro no banco ao buscar hábito de usuário por ID {habito_usuario_id}.") from e
        
    def buscar_todos_por_id(self, usuario_id: int):
        try:
            habitos = self.db.query(InstanciaDeHabito).filter_by(ator_id=usuario_id).all()
            if not habitos:
                raise NotFoundError(f"Hábito de usuário com ID {usuario_id} não encontrado.")
            return habitos
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError(f"Erro no banco ao buscar hábito de usuário por ID {usuario_id}.") from e
    
    def buscar_por_usuario(self, user_id: int) -> list[InstanciaDeHabito]:
        try:
            usuario = self.db.query(UsuarioPessoal).filter_by(id=user_id).first()
            if not usuario:
                raise NotFoundError(f"Usuário com ID {user_id} não encontrado.")
            return self.db.query(InstanciaDeHabito).filter(InstanciaDeHabito.ator_id == user_id).all()
        except (NoResultFound, SQLAlchemyError) as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar hábitos por usuário.") from e
