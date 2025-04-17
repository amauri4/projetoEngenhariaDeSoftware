from sqlalchemy.orm import Session
from models.HabitoBase import HabitoBase  
from models.Usuario import Usuario
from models.RegistroDiario import RegistroDiario
from models.CategoriasHabito import CategoriaHabito
from datetime import date

class HabitoRepository:

    def __init__(self, db: Session):
        self.db = db

    def buscar_por_email(self, email: str):
        return (
            self.db.query(HabitoBase)
            .join(HabitoBase.usuario)
            .filter(Usuario.email == email)
            .all()
        )

    def buscar_por_categoria(self, categoria_nome: str):
        return (
            self.db.query(HabitoBase)
            .join(HabitoBase.categoria)
            .filter(CategoriaHabito.nome == categoria_nome)
            .all()
        )

    def buscar_por_data(self, data_alvo: date):
        return (
            self.db.query(HabitoBase)
            .join(HabitoBase.registros)
            .filter(RegistroDiario.data == data_alvo)
            .all()
        )

    def buscar_por_email_e_data(self, email: str, data_alvo: date):
        return (
            self.db.query(HabitoBase)
            .join(HabitoBase.usuario)
            .join(HabitoBase.registros)
            .filter(Usuario.email == email, RegistroDiario.data == data_alvo)
            .all()
        )

    def buscar_por_email_e_categoria(self, email: str, categoria_nome: str):
        return (
            self.db.query(HabitoBase)
            .join(HabitoBase.usuario)
            .join(HabitoBase.categoria)
            .filter(Usuario.email == email, CategoriaHabito.nome == categoria_nome)
            .all()
        )

    def buscar_completo(self, email: str, categoria_nome: str, data_alvo: date):
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
