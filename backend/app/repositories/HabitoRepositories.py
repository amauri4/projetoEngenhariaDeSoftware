from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.HabitoBase import HabitoBase  
from models.Usuario import Usuario
from models.RegistroDiario import RegistroDiario
from models.CategoriasHabito import CategoriaHabito
from datetime import date

class HabitoRepository:

    def __init__(self, db: Session):
        self.db = db

    def buscar_por_email(self, email: str):
        try:
            return (
                self.db.query(HabitoBase)
                .join(HabitoBase.usuario)
                .filter(Usuario.email == email)
                .all()
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar hábitos por e-mail: {str(e)}")

    def buscar_por_categoria(self, categoria_nome: str):
        try:
            return (
                self.db.query(HabitoBase)
                .join(HabitoBase.categoria)
                .filter(CategoriaHabito.nome == categoria_nome)
                .all()
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar hábitos por categoria: {str(e)}")

    def buscar_por_data(self, data_alvo: date):
        try:
            return (
                self.db.query(HabitoBase)
                .join(HabitoBase.registros)
                .filter(RegistroDiario.data == data_alvo)
                .all()
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar hábitos por data: {str(e)}")

    def buscar_por_email_e_data(self, email: str, data_alvo: date):
        try:
            return (
                self.db.query(HabitoBase)
                .join(HabitoBase.usuario)
                .join(HabitoBase.registros)
                .filter(Usuario.email == email, RegistroDiario.data == data_alvo)
                .all()
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar hábitos por email e data: {str(e)}")

    def buscar_por_email_e_categoria(self, email: str, categoria_nome: str):
        try:
            return (
                self.db.query(HabitoBase)
                .join(HabitoBase.usuario)
                .join(HabitoBase.categoria)
                .filter(Usuario.email == email, CategoriaHabito.nome == categoria_nome)
                .all()
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar hábitos por email e categoria: {str(e)}")

    def buscar_completo(self, email: str, categoria_nome: str, data_alvo: date):
        try:
            return (
                self.db.query(HabitoBase)
                .join(HabitoBase.usuario)
                .join(HabitoBase.categoria)
                .join(HabitoBase.registros)
                .filter(
                    Usuario.email == email,
                    CategoriaHabito.nome == categoria_nome,
                    RegistroDiario.data == data_alvo
                )
                .all()
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar hábitos com todos os filtros: {str(e)}")
    def buscar_todos(self):
        try:
            return self.db.query(HabitoBase).all()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar hábitos: {str(e)}")

    def buscar_por_id(self, habito_id: int):
        try:
            return self.db.query(HabitoBase).filter_by(id=habito_id).first()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar hábito por ID: {str(e)}")

    def criar_habito(self, nome: str, descricao: str, categoria_id: int, usuario_id: int):
        try:
            habito = HabitoBase(
                nome=nome,
                descricao=descricao,
                categoria_id=categoria_id,
                usuario_id=usuario_id
            )
            self.db.add(habito)
            self.db.commit()
            self.db.refresh(habito)
            return habito
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao criar hábito: {str(e)}")

    def atualizar_habito(self, habito_id: int, nome: str = None, descricao: str = None, categoria_id: int = None):
        try:
            habito = self.buscar_por_id(habito_id)
            if not habito:
                raise Exception("Hábito não encontrado.")

            if nome:
                habito.nome = nome
            if descricao:
                habito.descricao = descricao
            if categoria_id:
                habito.categoria_id = categoria_id

            self.db.commit()
            self.db.refresh(habito)
            return habito
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao atualizar hábito: {str(e)}")

    def deletar_habito(self, habito_id: int):
        try:
            habito = self.buscar_por_id(habito_id)
            if not habito:
                raise Exception("Hábito não encontrado.")

            self.db.delete(habito)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao deletar hábito: {str(e)}")

    def deletar_registro_por_data(self, habito_id: int, data: date):
        try:
            registro = (
                self.db.query(RegistroDiario)
                .filter_by(habito_id=habito_id, data=data)
                .first()
            )
            if registro:
                self.db.delete(registro)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao deletar registro por data: {str(e)}")
