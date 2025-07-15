from flask import Blueprint, jsonify, request
from app.database.session import get_db
from app.services.TemplateMethodInsight.InsightCorrelacaoDeHabitos import EstrategiaCorrelacaoDeHabitos
from sqlalchemy.orm.exc import NoResultFound

operacoes_extra_bp = Blueprint("operacoes_extra", __name__, url_prefix="/operacoes-extra")

@operacoes_extra_bp.route("/correlacoes/<int:usuario_id>", methods=["GET"])
def buscar_correlacoes_habitos(usuario_id):
    try:
        with get_db() as db:
            service = EstrategiaCorrelacaoDeHabitos(db)
            resultado = service.gerar_insight(usuario_id)
            
            return jsonify({
                "success": True,
                "data": resultado,
                "message": "Correlações encontradas com sucesso"
            }), 200
            
    except NoResultFound as e:
        return jsonify({
            "success": False,
            "data": None,
            "message": str(e)
        }), 404
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "data": None,
            "message": str(e),
            "detalhes": "Verifique os parâmetros enviados"
        }), 400
        
    except Exception as e:
        print(f'\n\n{str(e)}\n\n')
        return jsonify({
            "success": False,
            "data": None,
            "message": "Erro ao buscar correlações entre hábitos",
            "detalhes": str(e)
        }), 500