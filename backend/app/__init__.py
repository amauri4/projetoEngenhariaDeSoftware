from flask import Flask
from app.database.base import engine, Base
from app.database.session import get_db
from app.utils.sync import sync_categorias_from_json
from dotenv import load_dotenv
from app.models.CategoriasHabito import CategoriaHabito
from app.models.HabitoBase import HabitoBase
from app.models.HabitoUsuario import HabitoUsuario
from app.models.RegistroDiario import RegistroDiario
from app.models.Usuario import Usuario
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Usado para criar tabela no bd (*ALTERAR FUTURAMENTE, POIS NÃO INCLUI MUDANÇAS NAS ESTRUTURA DAS TABELAS -> usar alembic*)
# Por hora, considerei uma boa alternativa inicializar hábitos e categorias de forma padrão num JSON (pode mudar no futuro)
def init_db():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(BASE_DIR, "data", "categorias_habitos.json")
    json_backup_path = os.path.join(BASE_DIR, "data", "categorias_habitos_backup.json")
    
    Base.metadata.create_all(bind=engine)
    
    with get_db() as db_session:
        sync_categorias_from_json(db=db_session, path=json_path, backup_path=json_backup_path)
    
    print("Banco de dados inicializado com sucesso!")

def create_app():
    init_db()
    return app
