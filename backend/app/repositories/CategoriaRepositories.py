from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.CategoriasHabito import CategoriaHabito

class CategoriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_todas(self):
        try:
            return self.db.query(CategoriaHabito).all()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao buscar categorias de hábito: {str(e)}")

    def criar_categoria(self, nome: str):
        try:
            nova_categoria = CategoriaHabito(nome=nome)
            self.db.add(nova_categoria)
            self.db.commit()
            return nova_categoria
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao criar categoria de hábito: {str(e)}")

    def atualizar_categoria(self, categoria_id: int, novo_nome: str):
        try:
            categoria = self.db.query(CategoriaHabito).filter_by(id=categoria_id).first()
            if not categoria:
                raise Exception("Categoria não encontrada.")
            categoria.nome = novo_nome
            self.db.commit()
            return categoria
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao atualizar categoria de hábito: {str(e)}")

    def remover_categoria(self, categoria_id: int):
        try:
            categoria = self.db.query(CategoriaHabito).filter_by(id=categoria_id).first()
            if not categoria:
                raise Exception("Categoria não encontrada.")
            self.db.delete(categoria)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao remover categoria de hábito: {str(e)}")
