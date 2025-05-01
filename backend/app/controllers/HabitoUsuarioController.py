from flask import Blueprint, jsonify, request
from app.database.session import get_db
from app.services.HabitoUsuarioService import HabitoUsuarioService

habito_usuario_bp = Blueprint("habito_usuario", __name__, url_prefix="/habitos-usuario")

@habito_usuario_bp.route("/<usuario_email>/habitos", methods=["GET"])
def listar_habitos_usuario(usuario_email):
    try:
        with get_db() as db:
            service = HabitoUsuarioService(db)
            habitos = service.buscar_habitos_usuario(usuario_email)

            habitos_json = [
                {
                    "id": h.id,
                    "descricao": h.descricao,
                    "habito_base_id": h.habito_base_id,
                    "usuario_id": h.usuario_id
                } for h in habitos
            ]

            return jsonify(habitos_json), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@habito_usuario_bp.route("/<int:usuario_id>/habitos", methods=["POST"])
def adicionar_habito_usuario(usuario_id):
    try:
        descricao = request.json.get("descricao")
        habito_base_id = request.json.get("habito_base_id")

        with get_db() as db:
            service = HabitoUsuarioService(db)
            novo_habito = service.adicionar_habito_usuario(descricao, habito_base_id, usuario_id)

            return jsonify({
                "message": "Hábito adicionado com sucesso.",
                "habito_usuario": {
                    "id": novo_habito.id,
                    "descricao": novo_habito.descricao,
                    "habito_base_id": novo_habito.habito_base_id,
                    "usuario_id": novo_habito.usuario_id
                }
            }), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@habito_usuario_bp.route("/habitos/<int:habito_usuario_id>", methods=["PUT"])
def atualizar_habito_usuario(habito_usuario_id):
    try:
        nova_descricao = request.json.get("descricao")
        novo_habito_base_id = request.json.get("habito_base_id")
        novo_usuario_id = request.json.get("usuario_id")

        with get_db() as db:
            service = HabitoUsuarioService(db)
            habito_atualizado = service.atualizar_habito_usuario(habito_usuario_id, nova_descricao, novo_habito_base_id, novo_usuario_id)

            return jsonify({
                "message": "Hábito atualizado com sucesso.",
                "habito_usuario": {
                    "id": habito_atualizado.id,
                    "descricao": habito_atualizado.descricao,
                    "habito_base_id": habito_atualizado.habito_base_id,
                    "usuario_id": habito_atualizado.usuario_id
                }
            }), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@habito_usuario_bp.route("/habitos/<int:habito_usuario_id>", methods=["DELETE"])
def remover_habito_usuario(habito_usuario_id):
    try:
        with get_db() as db:
            service = HabitoUsuarioService(db)
            service.remover_habito_usuario(habito_usuario_id)

            return jsonify({"message": "Hábito removido com sucesso."}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

from flask import Blueprint, jsonify, request
from app.database.session import get_db
from app.services.HabitoUsuarioService import HabitoUsuarioService

habito_usuario_bp = Blueprint("habito_usuario", __name__, url_prefix="/habitos-usuario")

@habito_usuario_bp.route("/<usuario_email>/habitos", methods=["GET"])
def listar_habitos_usuario(usuario_email):
    try:
        with get_db() as db:
            service = HabitoUsuarioService(db)
            habitos = service.buscar_habitos_usuario(usuario_email)

            habitos_json = [
                {
                    "id": h.id,
                    "descricao": h.descricao,
                    "habito_base_id": h.habito_base_id,
                    "usuario_id": h.usuario_id,
                    "frequencia": h.frequencia,
                    "data_inicio": h.data_inicio.strftime("%Y-%m-%d %H:%M:%S") if h.data_inicio else None,
                    "vezes_na_semana": h.vezes_na_semana
                } for h in habitos
            ]

            return jsonify(habitos_json), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@habito_usuario_bp.route("/<int:usuario_id>/habitos", methods=["POST"])
def adicionar_habito_usuario(usuario_id):
    try:
        descricao = request.json.get("descricao")
        habito_base_id = request.json.get("habito_base_id")
        frequencia = request.json.get("frequencia")
        data_inicio = request.json.get("data_inicio")
        vezes_na_semana = request.json.get("vezes_na_semana")
        dias_da_semana = request.json.get("dias_da_semana", [])
        dias_do_mes = request.json.get("dias_do_mes", [])

        # Validar frequência (diário, semanal, mensal)
        if frequencia not in ["diario", "semanal", "mensal"]:
            return jsonify({"erro": "Frequência inválida. Deve ser 'diario', 'semanal' ou 'mensal'."}), 400
        
        with get_db() as db:
            service = HabitoUsuarioService(db)
            novo_habito = service.adicionar_habito_usuario(
                descricao, 
                habito_base_id, 
                usuario_id,
                frequencia, 
                data_inicio,
                vezes_na_semana,
                dias_da_semana,
                dias_do_mes
            )

            return jsonify({
                "message": "Hábito adicionado com sucesso.",
                "habito_usuario": {
                    "id": novo_habito.id,
                    "descricao": novo_habito.descricao,
                    "habito_base_id": novo_habito.habito_base_id,
                    "usuario_id": novo_habito.usuario_id,
                    "frequencia": novo_habito.frequencia,
                    "vezes_na_semana": novo_habito.vezes_na_semana
                }
            }), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@habito_usuario_bp.route("/habitos/<int:habito_usuario_id>", methods=["PUT"])
def atualizar_habito_usuario(habito_usuario_id):
    try:
        nova_descricao = request.json.get("descricao")
        novo_habito_base_id = request.json.get("habito_base_id")
        novo_usuario_id = request.json.get("usuario_id")
        nova_frequencia = request.json.get("frequencia")
        nova_data_inicio = request.json.get("data_inicio")
        nova_vezes_na_semana = request.json.get("vezes_na_semana")
        novos_dias_da_semana = request.json.get("dias_da_semana", [])
        novos_dias_do_mes = request.json.get("dias_do_mes", [])

        # Validar frequência
        if nova_frequencia not in ["diario", "semanal", "mensal"]:
            return jsonify({"erro": "Frequência inválida. Deve ser 'diario', 'semanal' ou 'mensal'."}), 400
        
        with get_db() as db:
            service = HabitoUsuarioService(db)
            habito_atualizado = service.atualizar_habito_usuario(
                habito_usuario_id, 
                nova_descricao, 
                novo_habito_base_id, 
                novo_usuario_id, 
                nova_frequencia, 
                nova_data_inicio,
                nova_vezes_na_semana,
                novos_dias_da_semana,
                novos_dias_do_mes
            )

            return jsonify({
                "message": "Hábito atualizado com sucesso.",
                "habito_usuario": {
                    "id": habito_atualizado.id,
                    "descricao": habito_atualizado.descricao,
                    "habito_base_id": habito_atualizado.habito_base_id,
                    "usuario_id": habito_atualizado.usuario_id,
                    "frequencia": habito_atualizado.frequencia,
                    "vezes_na_semana": habito_atualizado.vezes_na_semana
                }
            }), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@habito_usuario_bp.route("/habitos/<int:habito_usuario_id>", methods=["DELETE"])
def remover_habito_usuario(habito_usuario_id):
    try:
        with get_db() as db:
            service = HabitoUsuarioService(db)
            service.remover_habito_usuario(habito_usuario_id)

            return jsonify({"message": "Hábito removido com sucesso."}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

