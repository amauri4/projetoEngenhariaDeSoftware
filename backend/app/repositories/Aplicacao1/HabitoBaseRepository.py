from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from app.models.Aplicacao1.HabitoBase import HabitoBase
from app.models.Aplicacao1.CategoriasHabito import CategoriasHabito
from app.exceptions.repository_exceptions  import RepositoryError, NotFoundError

class HabitoBaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_todos(self):
        try:
            habitos = self.db.query(HabitoBase).all()
            if not habitos:
                raise NotFoundError("Nenhum hábito encontrado.")
            return habitos
        
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError(f"Erro ao buscar hábitos: {str(e)}")

    def buscar_por_id(self, habito_id: int):
        try:
            habito = self.db.query(HabitoBase).filter_by(id=habito_id).first()
            if not habito:
                raise NotFoundError(f"Hábito com ID {habito_id} não encontrado.")
            return habito

        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError(f"Erro no banco ao buscar hábito por ID {habito_id}.") from e

    def criar_habito(self, nome: str, categoria_id: int):
        try:
            categoria = self.db.query(CategoriasHabito).filter_by(id=categoria_id).first()

            if not categoria:
                raise NotFoundError("Categoria não encontrada.")
            
            novo_habito = HabitoBase(nome=nome, categoria_id=categoria_id)
            self.db.add(novo_habito)
            self.db.commit()
            return novo_habito
        
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao criar hábito.") from e

    def atualizar_habito(self, habito_id: int, novo_nome: str, nova_categoria_id: int):
        try:
            habito = self.db.query(HabitoBase).filter_by(id=habito_id).first()

            if not habito:
                raise NotFoundError("Hábito não encontrado.")
            categoria = self.db.query(CategoriasHabito).filter_by(id=nova_categoria_id).first()

            if not categoria:
                raise NotFoundError("Categoria não encontrada.")
            
            habito.nome = novo_nome
            habito.categoria_id = nova_categoria_id
            self.db.commit()
            return habito
        
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao atualizar hábito.") from e

    def remover_habito(self, habito_id: int):
        try:
            habito = self.db.query(HabitoBase).filter_by(id=habito_id).first()
            if not habito:
                raise NotFoundError("Hábito não encontrado.")
            self.db.delete(habito)
            self.db.commit()

        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao remover hábito.") from e
