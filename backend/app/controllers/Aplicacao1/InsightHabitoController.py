from flask import Blueprint, jsonify, request
from app.database.session import get_db
from app.services.Aplicacao1.InsightCorrelacaoDeHabitos import InsightCorrelacaoDeHabitos
from sqlalchemy.orm.exc import NoResultFound

insight1_bp = Blueprint("insight1", __name__, url_prefix="/insight1")

@insight1_bp.route("/correlacoes/<int:usuario_id>", methods=["GET"])
def buscar_correlacoes_habitos(usuario_id):
    try:
        with get_db() as db:
            service = InsightCorrelacaoDeHabitos(db)
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