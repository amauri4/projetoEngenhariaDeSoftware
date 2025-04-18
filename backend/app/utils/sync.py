import json
import logging
from models.CategoriasHabito import CategoriaHabito
from models.HabitoBase import HabitoBase
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def sync_categorias_from_json(db: Session, path="data/categorias_habitos.json", backup_path="data/categorias_habitos_backup.json"):
    def load_data(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def inserir_categorias(categorias):
        for cat in categorias:
            if not db.query(CategoriaHabito).filter_by(id=cat["id"]).first():
                nova_categoria = CategoriaHabito(id=cat["id"], nome=cat["nome"])
                db.add(nova_categoria)
                logger.info(f"Categoria '{cat['nome']}' (ID: {cat['id']}) adicionada com sucesso.")
        db.commit()

    def inserir_habitos(habitos):
        for habito_data in habitos:
            if not db.query(HabitoBase).filter_by(nome=habito_data["nome"]).first():
                categoria = db.query(CategoriaHabito).filter_by(id=habito_data["categoria_id"]).first()
                if categoria:
                    habito = HabitoBase(
                        nome=habito_data["nome"],
                        categoria_id=habito_data["categoria_id"]
                    )
                    db.add(habito)
                    logger.info(f"Hábito '{habito_data['nome']}' adicionado com sucesso.")
                else:
                    logger.warning(f"Categoria ID {habito_data['categoria_id']} não encontrada para o hábito '{habito_data['nome']}'.")
        db.commit()

    try:
        logger.info("Tentando sincronizar dados a partir do arquivo JSON...")
        data = load_data(path)
        inserir_categorias(data.get("categorias", []))
        inserir_habitos(data.get("habitos", []))
        logger.info("Sincronização concluída com sucesso.")

    except FileNotFoundError as e:
        logger.error(f"Arquivo JSON não encontrado: {str(e)}")
        try:
            logger.info("Tentando carregar dados do arquivo de backup...")
            data = load_data(backup_path)
            inserir_categorias(data.get("categorias", []))
            inserir_habitos(data.get("habitos", []))
            logger.info("Sincronização com backup concluída com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao carregar backup: {str(e)}")
            logger.error("Nenhuma sincronização realizada. O banco de dados não foi alterado.")

    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar o arquivo JSON: {str(e)}")
        logger.error("Tentando usar o arquivo de backup, se disponível...")

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Erro ao sincronizar com o banco de dados: {str(e)}")

    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
