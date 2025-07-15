from flask import Blueprint, jsonify
from app.database.session import get_db
from app.services.TemplateMethodInsight.InsightProdutividadeDeEquipe import EstrategiaProdutividadeDeEquipe
from app.exceptions.service_exceptions import ServiceError
from sqlalchemy.orm.exc import NoResultFound

insight_bp = Blueprint("insights", __name__, url_prefix="/insights")

@insight_bp.route("/produtividade-equipe/<int:gerente_id>", methods=["GET"])
def buscar_insight_produtividade_equipe(gerente_id):
    try:
        with get_db() as db:
            service = EstrategiaProdutividadeDeEquipe(db)
            resultado = service.gerar_insight(gerente_id)
            
            return jsonify({
                "success": True,
                "data": resultado,
                "message": "Insight de produtividade da equipe gerado com sucesso."
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
