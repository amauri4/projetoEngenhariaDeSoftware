from flask import Blueprint, jsonify, request
from app.database.session import get_db
from app.services.Framework.OcorrenciaService import ServicoDeOcorrencia
from app.services.Aplicacao3.OcorrenciaTreino import OcorrenciaTreino
from app.exceptions.service_exceptions import ServiceError
from app.exceptions.repository_exceptions import NotFoundError

ocorrencia_treino_bp = Blueprint("ocorrencia_treino", __name__, url_prefix="/ocorrencias-treino")

def _serializar_ocorrencia(ocorrencia):
    return {
        "id": ocorrencia.id,
        "data": ocorrencia.data.isoformat() if ocorrencia.data else None,
        "status": ocorrencia.concluido,
        "treino_id": ocorrencia.item_id,
        "treino_descricao": ocorrencia.item.descricao if ocorrencia.item else "N/A"
    }

@ocorrencia_treino_bp.route("/ator/<int:ator_id>", methods=["GET"])
def listar_ocorrencias_por_ator(ator_id):
    with get_db() as db:
        try:
            servico = ServicoDeOcorrencia(db)
            ocorrencias = servico.buscar_por_ator(
                ator_id=ator_id,
                implementacao=OcorrenciaTreino
            )
            return jsonify([_serializar_ocorrencia(o) for o in ocorrencias]), 200
        except (NotFoundError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@ocorrencia_treino_bp.route("/<int:ocorrencia_id>", methods=["DELETE"])
def remover_ocorrencia(ocorrencia_id):
    with get_db() as db:
        try:
            servico = ServicoDeOcorrencia(db)
            servico.remover(
                ocorrencia_id=ocorrencia_id,
                implementacao=OcorrenciaTreino
            )
            return '', 204
        except (NotFoundError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@ocorrencia_treino_bp.route("/ator/<int:ator_id>/data", methods=["GET"])
def listar_ocorrencias_por_data(ator_id):
    with get_db() as db:
        data_inicio = request.args.get("data_inicio")
        data_fim = request.args.get("data_fim")
        try:
            servico = ServicoDeOcorrencia(db)
            ocorrencias = servico.buscar_por_data(
                ator_id=ator_id, 
                data_inicio=data_inicio, 
                data_fim=data_fim,
                implementacao=OcorrenciaTreino
            )
            return jsonify([_serializar_ocorrencia(o) for o in ocorrencias]), 200
        except (NotFoundError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500
        
@ocorrencia_treino_bp.route("/ator/<int:ator_id>/concluidas", methods=["GET"])
def listar_ocorrencias_concluidas_por_ator(ator_id):
    with get_db() as db:
        try:
            servico = ServicoDeOcorrencia(db)
            ocorrencias = servico.buscar_concluidas_por_ator(
                ator_id=ator_id,
                implementacao=OcorrenciaTreino
            )
            return jsonify([_serializar_ocorrencia(o) for o in ocorrencias]), 200
        except (NotFoundError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@ocorrencia_treino_bp.route("/ator/<int:ator_id>/data_especifica", methods=["GET"])
def listar_ocorrencias_por_data_especifica(ator_id):
    with get_db() as db:
        data_especifica = request.args.get("data")
        if not data_especifica:
            return jsonify({"erro": "O parâmetro 'data' é obrigatório."}), 400
        try:
            servico = ServicoDeOcorrencia(db)
            ocorrencias = servico.buscar_por_data_especifica(
                ator_id=ator_id, 
                data_especifica=data_especifica,
                implementacao=OcorrenciaTreino
            )
            return jsonify([_serializar_ocorrencia(o) for o in ocorrencias]), 200
        except (NotFoundError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500
        
@ocorrencia_treino_bp.route("/", methods=["POST"])
def criar_ocorrencia_de_treino():
    with get_db() as db:
        dados = request.get_json()
        treino_id = dados.get("treino_id")
        data_ocorrencia = dados.get("data")
        status = dados.get("status", False) 

        if not all([treino_id, data_ocorrencia]):
            return jsonify({"erro": "Os campos 'treino_id' e 'data' são obrigatórios."}), 400
        
        try:
            servico = ServicoDeOcorrencia(db)
            nova_ocorrencia = servico.criar_unica(
                item_id=treino_id, 
                data_str=data_ocorrencia, 
                status=status,
                implementacao=OcorrenciaTreino
            )
            return jsonify({
                "mensagem": "Ocorrência de treino criada com sucesso.",
                "ocorrencia": _serializar_ocorrencia(nova_ocorrencia)
            }), 201
        except (NotFoundError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@ocorrencia_treino_bp.route("/<int:ocorrencia_id>", methods=["PUT"])
def atualizar_status_ocorrencia(ocorrencia_id):
    with get_db() as db:
        dados = request.get_json()
        if "status" not in dados or not isinstance(dados["status"], bool):
            return jsonify({"erro": "O campo 'status' (booleano) é obrigatório."}), 400

        try:
            servico = ServicoDeOcorrencia(db)
            ocorrencia_atualizada = servico.atualizar_status(
                ocorrencia_id=ocorrencia_id, 
                novo_status=dados["status"],
                implementacao=OcorrenciaTreino
            )
            return jsonify({
                "mensagem": "Ocorrência atualizada com sucesso.",
                "ocorrencia": _serializar_ocorrencia(ocorrencia_atualizada)
            }), 200
        except (NotFoundError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500
