from database.base import engine, Base
from database.session import get_db
from utils.sync import sync_categorias_from_json
from models.Usuario import Usuario
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Usado para criar tabela no bd (*ALTERAR FUTURAMENTE, POIS NÃO INCLUI MUDANÇAS NAS ESTRUTURA DAS TABELAS -> usar alembic*)
# Por hora, considerei uma boa alternativa inicializar hábitos e categorias de forma padrão num JSON (pode mudar no futuro)
def init_db():
    json_path = os.path.join(BASE_DIR, "data", "categorias_habitos.json")
    json_backup_path = os.path.join(BASE_DIR, "data", "categorias_habitos_backup.json")
    Base.metadata.create_all(bind=engine)
    
    with get_db() as db:
        sync_categorias_from_json(db=db, path=json_path, backup_path=json_backup_path)

if __name__ == "__main__":
    init_db()
    print("Banco de dados inicializado com sucesso!")
