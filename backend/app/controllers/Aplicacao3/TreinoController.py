from flask import Blueprint, jsonify, request
from app.database.session import get_db
from app.services.Aplicacao3.TreinoService import TreinoService
from app.exceptions.service_exceptions import AuthError, ConflictError, ServiceError
from app.exceptions.repository_exceptions import NotFoundError
from datetime import datetime

treino_bp = Blueprint("treinos", __name__, url_prefix="/treinos")

@treino_bp.route("/ator/<int:ator_id>", methods=["GET"])
def listar_treinos_por_ator(ator_id):
    with get_db() as db:
        try:
            servico = TreinoService(db)
            treinos = db.query(servico.treino_repository.treino_model).filter_by(ator_id=ator_id).all() if hasattr(servico.treino_repository, 'treino_model') else []
            treinos_json = []
            for t in treinos:
                treino_json = {
                    "id": t.id,
                    "descricao": t.descricao,
                    "data_inicio": t.data_inicio.isoformat() if t.data_inicio else None,
                    "data_entrega": t.data_entrega.isoformat() if hasattr(t, 'data_entrega') and t.data_entrega else None,
                    "criador_id": t.ator_id,
                    "responsavel_id": getattr(t, 'id_aluno_responsavel', None)
                }
                treinos_json.append(treino_json)
            return jsonify(treinos_json), 200
        except (NotFoundError, AuthError, ConflictError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@treino_bp.route("/instrutor/<int:instrutor_id>", methods=["POST"])
def adicionar_treino(instrutor_id):
    with get_db() as db:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400
        try:
            servico = TreinoService(db)
            novo_treino = servico.criar_treino(
                descricao=dados.get("descricao"),
                data_inicio=datetime.fromisoformat(dados.get("data_inicio")) if dados.get("data_inicio") else None,
                criador_id=instrutor_id,
                responsavel_id=dados.get("id_aluno_responsavel"),
                data_entrega=datetime.fromisoformat(dados.get("data_entrega")) if dados.get("data_entrega") else None
            )
            return jsonify({
                "mensagem": "Treino adicionado com sucesso.",
                "treino": { "id": novo_treino.id, "descricao": novo_treino.descricao }
            }), 201
        except (NotFoundError, AuthError, ConflictError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@treino_bp.route("/<int:treino_id>", methods=["PUT"])
def atualizar_treino(treino_id):
    with get_db() as db:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400
        try:
            servico = TreinoService(db)
            treino_atualizado = servico.atualizar_treino(
                treino_id=treino_id,
                descricao=dados.get("descricao"),
                responsavel_id=dados.get("id_aluno_responsavel"),
                data_entrega=datetime.fromisoformat(dados.get("data_entrega")) if dados.get("data_entrega") else None
            )
            return jsonify({
                "mensagem": "Treino atualizado com sucesso.",
                "treino": { "id": treino_atualizado.id, "descricao": treino_atualizado.descricao }
            }), 200
        except (NotFoundError, AuthError, ConflictError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500
