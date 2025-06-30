from flask import Blueprint, jsonify, request
from app.database.session import get_db
from app.services.TemplateMethod.OcorrenciaHabitoService import ServicoDeOcorrenciasDeHabito

registro_diario_bp = Blueprint("registro_diario", __name__, url_prefix="/registros-diarios")

@registro_diario_bp.route("/<int:usuario_id>/registros", methods=["GET"])
def listar_registros_usuario(usuario_id):
    try:
        with get_db() as db:
            servico = ServicoDeOcorrenciasDeHabito(db)
            ocorrencias = servico.buscar_ocorrencias_por_ator(usuario_id)

            registros_json = [
                {
                    "id": r.id,
                    "data": r.data,
                    "habito_id": r.item_id,
                    "concluido": r.concluido
                } for r in ocorrencias
            ]

            return jsonify(registros_json), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@registro_diario_bp.route("/<int:usuario_id>/registros/concluidos", methods=["GET"])
def listar_registros_concluidos_usuario(usuario_id):
    try:
        with get_db() as db:
            servico = ServicoDeOcorrenciasDeHabito(db)
            ocorrencias = servico.buscar_ocorrencias_concluidas_por_ator(usuario_id)

            registros_json = [
                {
                    "id": r.id,
                    "data": r.data,
                    "habito_id": r.item_id,
                    "concluido": r.concluido
                } for r in ocorrencias
            ]

            return jsonify(registros_json), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@registro_diario_bp.route("/registros", methods=["POST"])
def criar_registro_diario():
    try:
        data = request.get_json()
        data_dia = data.get("data")
        habito_id = data.get("habito_id")
        concluido = data.get("concluido")
        if not habito_id or not data_dia:
            return jsonify({"erro": "O campo 'habito_id' e o campo 'data' são obrigatórios."}), 400

        with get_db() as db:
            service = ServicoDeOcorrenciasDeHabito(db)
            novo_registro = service.criar_ocorrencia_unica(item_id=habito_id, data_str=data_dia, status=concluido)

            return jsonify({
                "message": "Registro diário criado com sucesso.",
                "registro_diario": {
                    "id": novo_registro.id,
                    "data": novo_registro.data,
                    "habito_id": novo_registro.item_id,
                    "concluido": novo_registro.concluido
                }
            }), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@registro_diario_bp.route("/registros/<int:registro_id>", methods=["PUT"])
def atualizar_registro_diario(registro_id):
    try:
        concluido = request.json.get("concluido")

        with get_db() as db:
            service = ServicoDeOcorrenciasDeHabito(db)
            registro_atualizado = service.atualizar_status_ocorrencia(registro_id, concluido)

            return jsonify({
                "message": "Registro diário atualizado com sucesso.",
                "registro_diario": {
                    "id": registro_atualizado.id,
                    "data": registro_atualizado.data,
                    "habito_id": registro_atualizado.item_id,
                    "concluido": registro_atualizado.concluido
                }
            }), 200
    except Exception as e:
        print(f'\n\n{str(e)}\n\n')
        return jsonify({"erro": str(e)}), 400

@registro_diario_bp.route("/registros/<int:registro_id>", methods=["DELETE"])
def remover_registro_diario(registro_id):
    try:
        with get_db() as db:
            service = ServicoDeOcorrenciasDeHabito(db)
            service.remover_ocorrencia(registro_id)

            return jsonify({"message": "Registro diário removido com sucesso."}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@registro_diario_bp.route("/<int:usuario_id>/registros/data", methods=["GET"])
def listar_registros_por_data(usuario_id):
    try:
        data_inicio = request.args.get("data_inicio")
        data_fim = request.args.get("data_fim")
        
        with get_db() as db:
            service = ServicoDeOcorrenciasDeHabito(db)
            registros = service.buscar_ocorrencias_por_data(usuario_id, data_inicio, data_fim)

            registros_json = [
                {
                    "id": r.id,
                    "data": r.data,
                    "habito_id": r.item_id,
                    "concluido": r.concluido
                } for r in registros
            ]
            
            return jsonify(registros_json), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@registro_diario_bp.route("/<int:usuario_id>/registros/data_especifica", methods=["GET"])
def listar_registros_por_data_especifica(usuario_id):
    try:
        data_especifica = request.args.get("data")
        
        if not data_especifica:
            return jsonify({"erro": "A data específica é obrigatória."}), 400

        with get_db() as db:
            service = ServicoDeOcorrenciasDeHabito(db)
            registros = service.buscar_ocorrencias_por_data_especifica(usuario_id, data_especifica)

            registros_json = [
                {
                    "id": r.id,
                    "data": r.data,
                    "habito_id": r.item_id,
                    "concluido": r.concluido
                } for r in registros
            ]

            return jsonify(registros_json), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
