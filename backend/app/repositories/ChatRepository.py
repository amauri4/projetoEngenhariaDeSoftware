from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from app.models.HistoricoChat import HistoricoChat
from app.exceptions.repository_exceptions  import RepositoryError, NotFoundError

class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar_historicochat(self, ator_id: int, mensagem: str, quem_enviou: str) -> HistoricoChat:
        try:
            nova_mensagem = HistoricoChat(
                ator_id=ator_id,
                mensagem=mensagem,
                quem_enviou=quem_enviou
            )
            self.db.add(nova_mensagem)
            self.db.commit()
            self.db.refresh(nova_mensagem)
            return nova_mensagem
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao criar e salvar mensagem no histórico.") from e

    def salvar_mensagem(self, mensagem: HistoricoChat) -> HistoricoChat:
        try:
            self.db.add(mensagem)
            self.db.commit()
            self.db.refresh(mensagem)
            return mensagem
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao salvar mensagem no histórico.") from e

    def buscar_historico_por_usuario(self, usuario_id: int) -> list[HistoricoChat]:
        try:
            historico = (self.db.query(HistoricoChat)
                         .filter(HistoricoChat.ator_id == usuario_id)
                         .order_by(HistoricoChat.timestamp.asc())
                         .all())
            
            if not historico:
                raise NotFoundError("Nenhum histórico encontrado para o usuário.")
            return historico
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar histórico por usuário.") from e

    def buscar_ultimas_mensagens(self, usuario_id: int, limite: int = 10) -> list[HistoricoChat]:
        try:
            mensagens = (self.db.query(HistoricoChat)
                        .filter(HistoricoChat.ator_id == usuario_id)
                        .order_by(HistoricoChat.timestamp.desc())
                        .limit(limite)
                        .all()[::-1])
            
            if not mensagens:
                raise NotFoundError("Nenhuma mensagem encontrada para o usuário.")
            return mensagens
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao buscar últimas mensagens.") from e

    def deletar_historico(self, usuario_id: int) -> None:
        try:
            result = (self.db.query(HistoricoChat)
                     .filter(HistoricoChat.ator_id == usuario_id)
                     .delete())
            
            if result == 0:
                raise NotFoundError("Nenhum histórico encontrado para deletar.")
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Erro ao deletar histórico.") from e