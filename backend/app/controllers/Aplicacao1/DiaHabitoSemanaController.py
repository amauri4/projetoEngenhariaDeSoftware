from flask import Blueprint, jsonify, request
from app.database.session import get_db
from app.services.Aplicacao1.DiaHabitoSemanaService import DiaHabitoSemanaService

dia_habito_semana_bp = Blueprint("dia_habito_semana", __name__, url_prefix="/dias-habito-semana")

@dia_habito_semana_bp.route("/habito/<int:habito_id>", methods=["GET"])
def listar_dias_habito_semana(habito_id):
    try:
        with get_db() as db:
            service = DiaHabitoSemanaService(db)
            dias = service.buscar_por_habito(habito_id)
            
            dias_json = [{"id": d.id, "habito_id": d.habito_id, "dia": d.dia.value} for d in dias]
            return jsonify(dias_json), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@dia_habito_semana_bp.route("", methods=["POST"])
def adicionar_dia_habito_semana():
    try:
        habito_id = request.json.get("habito_id")
        dia = request.json.get("dia")
        
        if not habito_id or not dia:
            return jsonify({"erro": "habito_id e dia são obrigatórios"}), 400
            
        with get_db() as db:
            service = DiaHabitoSemanaService(db)
            novo_dia = service.adicionar_dia(habito_id, dia)
            
            return jsonify({
                "message": "Dia adicionado ao hábito semanal com sucesso",
                "dia": {"id": novo_dia.id, "habito_id": novo_dia.habito_id, "dia": novo_dia.dia.value}
            }), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@dia_habito_semana_bp.route("/habito/<int:habito_id>/adicionar-varios", methods=["POST"])
def adicionar_varios_dias_semana(habito_id: int):
    try:
        dias = request.json.get("dias")
        
        if not dias or not isinstance(dias, list):
            return jsonify({"erro": "A lista de dias é obrigatória"}), 400
            
        with get_db() as db:
            service = DiaHabitoSemanaService(db)
            dias_adicionados = service.adicionar_varios_dias(habito_id, dias)
            
            return jsonify({
                "message": "Dias adicionados ao hábito semanal com sucesso",
                "dias": [{"id": d.id, "habito_id": d.habito_id, "dia": d.dia.value} for d in dias_adicionados]
            }), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@dia_habito_semana_bp.route("/<int:dia_id>", methods=["DELETE"])
def remover_dia_por_id(dia_id):
    try:
        with get_db() as db:
            service = DiaHabitoSemanaService(db)
            service.remover_dia_por_id(dia_id)
            
            return jsonify({"message": "Dia removido do hábito semanal com sucesso"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@dia_habito_semana_bp.route("/habito/<int:habito_id>/dia/<int:dia>", methods=["DELETE"])
def remover_dia_por_habito_e_dia(habito_id, dia):
    try:
        with get_db() as db:
            service = DiaHabitoSemanaService(db)
            service.remover_dia_por_habito_e_dia(habito_id, dia)
            
            return jsonify({"message": "Dia removido do hábito semanal com sucesso"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@dia_habito_semana_bp.route("/habito/<int:habito_id>/remover-todos", methods=["DELETE"])
def remover_todos_dias_habito_semana(habito_id):
    try:
        with get_db() as db:
            service = DiaHabitoSemanaService(db)
            service.remover_todos_por_habito(habito_id)
            
            return jsonify({"message": "Todos os dias do hábito semanal foram removidos com sucesso"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400