from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base


class HistoricoChat(Base):
    __tablename__ = 'historico_chat'

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    quem_enviou = Column(String(10), nullable=False) 
    mensagem = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="conversas")

    def __repr__(self):
        return (f"<HistoricoChat(usuario_id={self.usuario_id}, quem_enviou='{self.quem_enviou}', "
                f"mensagem='{self.mensagem}', timestamp='{self.timestamp}')>")