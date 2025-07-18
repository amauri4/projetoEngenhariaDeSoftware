from collections import defaultdict
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload
from app.models.Aplicacao1.CategoriasHabito import CategoriasHabito
from app.models.Aplicacao1.HabitoBase import HabitoBase
from app.models.Aplicacao1.InstanciaDeHabito import InstanciaDeHabito
from app.exceptions.repository_exceptions  import RepositoryError, NotFoundError

class CategoriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_todas(self):
        try:
            categorias = self.db.query(CategoriasHabito).all()
            if not categorias:
                raise NotFoundError("Nenhuma categoria de hábito encontrada.")
            return categorias
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar categorias de hábito.") from e

    def criar_categoria(self, nome: str):
        try:
            nova_categoria = CategoriasHabito(nome=nome)
            self.db.add(nova_categoria)
            self.db.commit()
            return nova_categoria
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao atualizar categoria de hábito.") from e

    def atualizar_categoria(self, categoria_id: int, novo_nome: str):
        try:
            categoria = self.db.query(CategoriasHabito).filter_by(id=categoria_id).first()
            if not categoria:
                raise NotFoundError("Categoria não encontrada.")
            categoria.nome = novo_nome
            self.db.commit()
            return categoria
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao atualizar categoria de hábito.") from e
        
    def remover_categoria(self, categoria_id: int):
        try:
            categoria = self.db.query(CategoriasHabito).filter_by(id=categoria_id).first()
            if not categoria:
                raise NotFoundError("Categoria não encontrada.")
            self.db.delete(categoria)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao remover categoria de hábito.") from e
            
    def buscar_categorias_por_usuario(self, usuario_id: int) -> dict:
        try:
            if not isinstance(usuario_id, int) or usuario_id <= 0:
                raise ValueError("ID do usuário inválido")

            resultados = (
                self.db.query(
                    CategoriasHabito.nome,
                    func.count(InstanciaDeHabito.id).label('quantidade')
                )
                .select_from(InstanciaDeHabito)
                .join(HabitoBase, InstanciaDeHabito.habito_base_id == HabitoBase.id)
                .join(CategoriasHabito, HabitoBase.categoria_id == CategoriasHabito.id)
                .filter(InstanciaDeHabito.ator_id == usuario_id)
                .group_by(CategoriasHabito.nome)
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
