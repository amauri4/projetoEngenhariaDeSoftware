from collections import defaultdict
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from app.models.CategoriasHabito import CategoriaHabito
from ..models.HabitoBase import HabitoBase
from ..models.HabitoUsuario import HabitoUsuario
from sqlalchemy.orm import joinedload

class CategoriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_todas(self):
        try:
            categorias = self.db.query(CategoriaHabito).all()
            if not categorias:
                raise NoResultFound("Nenhuma categoria de hábito encontrada.")
            return categorias
        except NoResultFound as e:
            raise Exception(f"Erro ao buscar categorias de hábito: {str(e)}")
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
                raise NoResultFound("Categoria não encontrada.")
            categoria.nome = novo_nome
            self.db.commit()
            return categoria
        except NoResultFound as e:
            raise Exception(f"Erro ao atualizar categoria de hábito: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao atualizar categoria de hábito: {str(e)}")

    def remover_categoria(self, categoria_id: int):
        try:
            categoria = self.db.query(CategoriaHabito).filter_by(id=categoria_id).first()
            if not categoria:
                raise NoResultFound("Categoria não encontrada.")
            self.db.delete(categoria)
            self.db.commit()
        except NoResultFound as e:
            raise Exception(f"Erro ao remover categoria de hábito: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Erro ao remover categoria de hábito: {str(e)}")
            
    def buscar_categorias_por_usuario(self, usuario_id: int) -> dict:
        try:
            if not isinstance(usuario_id, int) or usuario_id <= 0:
                raise ValueError("ID do usuário inválido")

            resultados = (
                self.db.query(
                    CategoriaHabito.nome,
                    func.count(HabitoUsuario.id).label('quantidade')
                )
                .select_from(HabitoUsuario)
                .join(HabitoBase, HabitoUsuario.habito_base_id == HabitoBase.id)
                .join(CategoriaHabito, HabitoBase.categoria_id == CategoriaHabito.id)
                .filter(HabitoUsuario.usuario_id == usuario_id)
                .group_by(CategoriaHabito.nome)
                .all()
            )

            return dict(resultados)

        except SQLAlchemyError as e:
            self.db.rollback()
            error_msg = getattr(e, 'orig', str(e))
            if hasattr(error_msg, 'args') and error_msg.args:
                error_msg = error_msg.args[0]
            raise Exception(f"Erro de banco de dados: {error_msg}")
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Erro inesperado: {str(e)}")
