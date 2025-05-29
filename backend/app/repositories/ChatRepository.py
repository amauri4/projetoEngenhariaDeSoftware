from sqlalchemy.orm import Session
from app.models.HistoricoChat import HistoricoChat


class ChatRepository:

    def __init__(self, db: Session):
        self.db = db

    def salvar_mensagem(self, mensagem: HistoricoChat):
        self.db.add(mensagem)
        self.db.commit()
        self.db.refresh(mensagem)
        return mensagem

    def buscar_historico_por_usuario(self, usuario_id: int):
        return (self.db.query(HistoricoChat)
                .filter(HistoricoChat.usuario_id == usuario_id)
                .order_by(HistoricoChat.timestamp.asc())
                .all())

    def buscar_ultimas_mensagens(self, usuario_id: int, limite: int = 10):
        return (self.db.query(HistoricoChat)
                .filter(HistoricoChat.usuario_id == usuario_id)
                .order_by(HistoricoChat.timestamp.desc())
                .limit(limite)
                .all()[::-1])

    def deletar_historico(self, usuario_id: int):
        (self.db.query(HistoricoChat)
         .filter(HistoricoChat.usuario_id == usuario_id)
         .delete())
        self.db.commit()