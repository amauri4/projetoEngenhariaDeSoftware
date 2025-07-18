from flask import Blueprint, jsonify
from app.database.session import get_db
from app.services.Aplicacao1.HabitoBaseService import HabitoBaseService

habito_bp = Blueprint("habito", __name__, url_prefix="/habitos")

@habito_bp.route("/", methods=["GET"])
def listar_habitos():
    try:
        with get_db() as db:
            service = HabitoBaseService(db)
            habitos = service.buscar_habitos_disponiveis()

            habitos_json = [
                {
                    "id": h.id,
                    "nome": h.nome,
                    "categoria_id": h.categoria_id
                } for h in habitos
            ]

            return jsonify(habitos_json), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
