from flask import Blueprint, jsonify
from app.database.session import get_db
from app.services.Aplicacao3.InsightRendimentoDeAlunos import InsightRendimentoDeAlunos
from app.exceptions.service_exceptions import ServiceError
from sqlalchemy.orm.exc import NoResultFound

insight3_bp = Blueprint("insight3", __name__, url_prefix="/insight3")

@insight3_bp.route("/produtividade-equipe/<int:gerente_id>", methods=["GET"])
def buscar_insight_produtividade_equipe(gerente_id):
    try:
        with get_db() as db:
            service = InsightRendimentoDeAlunos(db)
            resultado = service.gerar_insight(gerente_id)
            
            return jsonify({
                "success": True,
                "data": resultado,
                "message": "Insight de rendimento dos alunos gerado com sucesso."
            }), 200
            
    except ServiceError as e:
        return jsonify({
            "success": False,
            "data": None,
            "message": str(e)
        }), 404 
        
    except Exception as e:
        return jsonify({
            "success": False,
            "data": None,
            "message": "Ocorreu um erro inesperado ao gerar o insight.",
            "detalhes": str(e)
        }), 500