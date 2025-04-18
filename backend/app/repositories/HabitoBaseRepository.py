from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from models.HabitoBase import HabitoBase
from models.CategoriasHabito import CategoriaHabito

class HabitoBaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_todos(self):
        try:
            habitos = self.db.query(HabitoBase).all()
            if not habitos:
                raise NoResultFound("Nenhum hábito encontrado.")
            return habitos
        except NoResultFound as e:
            raise Exception(f"Erro ao buscar hábitos: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar hábitos: {str(e)}")

    def criar_habito(self, nome: str, categoria_id: int):
        try:
            categoria = self.db.query(CategoriaHabito).filter_by(id=categoria_id).first()
            if not categoria:
                raise NoResultFound("Categoria não encontrada.")
            novo_habito = HabitoBase(nome=nome, categoria_id=categoria_id)
            self.db.add(novo_habito)
            self.db.commit()
            return novo_habito
        except NoResultFound as e:
            raise Exception(f"Erro ao criar hábito: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao criar hábito: {str(e)}")

    def atualizar_habito(self, habito_id: int, novo_nome: str, nova_categoria_id: int):
        try:
            habito = self.db.query(HabitoBase).filter_by(id=habito_id).first()
            if not habito:
                raise NoResultFound("Hábito não encontrado.")
            categoria = self.db.query(CategoriaHabito).filter_by(id=nova_categoria_id).first()
            if not categoria:
                raise NoResultFound("Categoria não encontrada.")
            habito.nome = novo_nome
            habito.categoria_id = nova_categoria_id
            self.db.commit()
            return habito
        except NoResultFound as e:
            raise Exception(f"Erro ao atualizar hábito: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao atualizar hábito: {str(e)}")

    def remover_habito(self, habito_id: int):
        try:
            habito = self.db.query(HabitoBase).filter_by(id=habito_id).first()
            if not habito:
                raise NoResultFound("Hábito não encontrado.")
            self.db.delete(habito)
            self.db.commit()
        except NoResultFound as e:
            raise Exception(f"Erro ao remover hábito: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao remover hábito: {str(e)}")
