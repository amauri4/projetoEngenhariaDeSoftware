import json
import logging
from models.CategoriasHabito import CategoriaHabito
from models.HabitoBase import HabitoBase
from models.RegistroDiario import RegistroDiario
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def sync_categorias_from_json(db: Session, path="data/categorias_habitos.json", backup_path="data/categorias_habitos_backup.json"):
    try:
        logger.info("Tentando sincronizar dados a partir do arquivo JSON...")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for nome_categoria in data.get("categorias", []):
            if not db.query(CategoriaHabito).filter_by(nome=nome_categoria).first():
                db.add(CategoriaHabito(nome=nome_categoria))
                logger.info(f"Categoria '{nome_categoria}' adicionada com sucesso.")
        db.commit()

        for habito_data in data.get("habitos", []):
            categoria = db.query(CategoriaHabito).filter_by(nome=habito_data["categoria"]).first()
            if categoria:
                if not db.query(HabitoBase).filter_by(nome=habito_data["nome"]).first():
                    habito = HabitoBase(
                        nome=habito_data["nome"],
                        descricao=habito_data["descricao"],
                        categoria=categoria
                    )
                    db.add(habito)
                    logger.info(f"Hábito '{habito_data['nome']}' adicionado com sucesso.")
                else:
                    logger.warning(f"Hábito '{habito_data['nome']}' já existe no banco de dados.")
            else:
                logger.warning(f"Categoria '{habito_data['categoria']}' não encontrada para o hábito '{habito_data['nome']}'.")

        db.commit()
        logger.info("Sincronização concluída com sucesso.")

    except FileNotFoundError as e:
        logger.error(f"Arquivo JSON não encontrado: {str(e)}")
        try:
            logger.info("Tentando carregar dados do arquivo de backup...")
            with open(backup_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for nome_categoria in data.get("categorias", []):
                if not db.query(CategoriaHabito).filter_by(nome=nome_categoria).first():
                    db.add(CategoriaHabito(nome=nome_categoria))
                    logger.info(f"Categoria '{nome_categoria}' do backup adicionada com sucesso.")

            db.commit()

            for habito_data in data.get("habitos", []):
                categoria = db.query(CategoriaHabito).filter_by(nome=habito_data["categoria"]).first()
                if categoria:
                    if not db.query(HabitoBase).filter_by(nome=habito_data["nome"]).first():
                        habito = HabitoBase(
                            nome=habito_data["nome"],
                            descricao=habito_data["descricao"],
                            categoria=categoria
                        )
                        db.add(habito)
                        logger.info(f"Hábito '{habito_data['nome']}' do backup adicionado com sucesso.")
                    else:
                        logger.warning(f"Hábito '{habito_data['nome']}' do backup já existe.")
                else:
                    logger.warning(f"Categoria '{habito_data['categoria']}' do backup não encontrada.")

            db.commit()
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
