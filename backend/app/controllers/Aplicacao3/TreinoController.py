from flask import Blueprint, jsonify, request
from app.database.session import get_db
from app.services.Framework.ItemService import ItemService
from app.services.Aplicacao3.ItemTreino import ItemTreino
from app.exceptions.service_exceptions import AuthError, ConflictError, ServiceError
from app.exceptions.repository_exceptions import NotFoundError

treino_bp = Blueprint("treinos", __name__, url_prefix="/treinos")

def _serializar_treino(treino):
    return {
        "id": treino.id,
        "descricao": treino.descricao,
        "data_inicio": treino.data_inicio.isoformat() if treino.data_inicio else None,
        "data_entrega": treino.data_entrega.isoformat() if hasattr(treino, 'data_entrega') and treino.data_entrega else None,
        "criador_id": treino.ator_id,
        "criador_nome": treino.criador.nome if treino.criador else None,
        "responsavel_id": getattr(treino, 'id_aluno_responsavel', None),
        "responsavel_nome": treino.responsavel.nome if treino.responsavel else None
    }

@treino_bp.route("/ator/<int:ator_id>", methods=["GET"])
def listar_treinos_por_ator(ator_id):
    with get_db() as db:
        try:
            servico = ItemService(db)
            treinos = servico.buscar_por_ator(ator_id, ItemTreino)
            return jsonify([_serializar_treino(t) for t in treinos]), 200
        except (NotFoundError, ServiceError) as e:
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
            servico = ItemService(db)
            novo_treino = servico.adicionar(
                ator_id=instrutor_id, 
                dados=dados, 
                implementacao=ItemTreino
            )
            return jsonify({
                "mensagem": "Treino adicionado com sucesso.",
                "treino": _serializar_treino(novo_treino)
            }), 201
        except (NotFoundError, ServiceError) as e:
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
            servico = ItemService(db)
            treino_atualizado = servico.atualizar(
                item_id=treino_id, 
                dados=dados, 
                implementacao=ItemTreino
            )
            return jsonify({
                "mensagem": "Treino atualizado com sucesso.",
                "treino": _serializar_treino(treino_atualizado)
            }), 200
        except (NotFoundError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@treino_bp.route("/<int:treino_id>", methods=["DELETE"])
def remover_treino(treino_id):
    with get_db() as db:
        try:
            servico = ItemService(db)
            servico.remover(
                item_id=treino_id, 
                implementacao=ItemTreino
            )
            return '', 204
        except NotFoundError as e:
            return jsonify({"erro": str(e)}), 404
        except ServiceError as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500