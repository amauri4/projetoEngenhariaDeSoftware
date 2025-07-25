from flask import Blueprint, jsonify, request
from app.database.session import get_db
from app.exceptions.service_exceptions import AuthError, ConflictError, ServiceError
from app.repositories.Framework.AtorRepository import AtorRepository
from app.services.Framework.ItemService import ItemService
from app.services.Aplicacao1.Habito import EstrategiaDeHabito
from app.services.Aplicacao1.InsightCorrelacaoDeHabitos import InsightCorrelacaoDeHabitos

habito_usuario_bp = Blueprint("habito_usuario", __name__, url_prefix="/habitos-usuario")

@habito_usuario_bp.route("/<usuario_email>/habitos", methods=["GET"])
def listar_habitos_por_ator(usuario_email):
    with get_db() as db:
        try:
            ator_repo = AtorRepository(db)
            servico = ItemService(db)

            ator = ator_repo.buscar_por_email(usuario_email)
            if not ator:
                raise AuthError("Ator não encontrado.")

            habitos = servico.buscar_por_ator(ator.id, EstrategiaDeHabito)

            habitos_json = []
            for h in habitos:
                habito_json = {
                    "id": h.id,
                    "descricao": h.descricao,
                    "frequencia": h.frequencia.value,
                    "data_inicio": h.data_inicio.isoformat() if h.data_inicio else None,
                    "vezes_na_semana": h.vezes_na_semana,
                    "dias_semana": [dia.dia.value for dia in h.dias_semana] if h.dias_semana else [],
                    "dias_mes": [dia.dia for dia in h.dias_mes] if h.dias_mes else [],
                    "ator_id": h.ator_id,
                    "habito_base_id": h.habito_base_id,
                    "habito_base_nome": h.habito_base.nome if h.habito_base else None
                }
                habitos_json.append(habito_json)

            return jsonify(habitos_json), 200
        except (AuthError, ConflictError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@habito_usuario_bp.route("/<int:usuario_id>/habitos", methods=["POST"])
def adicionar_habito(usuario_id):
    with get_db() as db:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400

        try:
            servico = ItemService(db)            
            novo_habito = servico.adicionar(ator_id=usuario_id, dados=dados, implementacao=EstrategiaDeHabito)

            return jsonify({
                "mensagem": "Hábito adicionado com sucesso.",
                "habito": { "id": novo_habito.id, "descricao": novo_habito.descricao }
            }), 201
        except (AuthError, ConflictError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@habito_usuario_bp.route("/habitos/<int:habito_usuario_id>", methods=["PUT"])
def atualizar_habito(habito_usuario_id):
    with get_db() as db:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400

        try:
            servico = ItemService(db)            
            habito_atualizado = servico.atualizar(habito_usuario_id, dados, EstrategiaDeHabito)

            return jsonify({
                "mensagem": "Hábito atualizado com sucesso.",
                "habito": { "id": habito_atualizado.id, "descricao": habito_atualizado.descricao }
            }), 200
        except (AuthError, ConflictError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@habito_usuario_bp.route("/habitos/<int:habito_usuario_id>", methods=["DELETE"])
def remover_habito(habito_usuario_id):
    with get_db() as db:
        try:
            servico = ItemService(db)            
            servico.remover(habito_usuario_id, EstrategiaDeHabito)

            return jsonify({"mensagem": "Hábito removido com sucesso."}), 204 
        except (AuthError, ConflictError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500
    
@habito_usuario_bp.route("/<int:usuario_id>/categorias-usuario", methods=["GET"])
def buscar_categorias_usuario(usuario_id):
    try:
        with get_db() as db:
            service = InsightCorrelacaoDeHabitos(db)
            habitos = service.buscar_categorias_usuario(usuario_id=usuario_id)
            
            return jsonify(habitos), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 400


