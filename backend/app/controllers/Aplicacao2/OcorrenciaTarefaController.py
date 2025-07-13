from flask import Blueprint, jsonify, request
from app.database.session import get_db
from app.services.OcorrenciaService import ServicoDeOcorrencia
from app.services.TemplateMethodOcorrencia.OcorrenciaTarefaService import ServicoDeOcorrenciaDeTarefa
from app.exceptions.service_exceptions import ServiceError
from app.exceptions.repository_exceptions import NotFoundError

ocorrencia_tarefa_bp = Blueprint("ocorrencia_tarefa", __name__, url_prefix="/ocorrencias-tarefa")

def _serializar_ocorrencia(ocorrencia):
    return {
        "id": ocorrencia.id,
        "data_prevista": ocorrencia.data_prevista.isoformat() if ocorrencia.data_prevista else None,
        "status": ocorrencia.status,
        "tarefa_id": ocorrencia.item_rastreavel_id,
        "tarefa_descricao": ocorrencia.item.descricao if ocorrencia.item else "N/A"
    }

@ocorrencia_tarefa_bp.route("/ator/<int:ator_id>", methods=["GET"])
def listar_ocorrencias_por_ator(ator_id):
    with get_db() as db:
        try:
            servico = ServicoDeOcorrencia(db)
            ocorrencias = servico.buscar_por_ator(
                ator_id=ator_id,
                implementacao=ServicoDeOcorrenciaDeTarefa
            )
            return jsonify([_serializar_ocorrencia(o) for o in ocorrencias]), 200
        except (NotFoundError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@ocorrencia_tarefa_bp.route("/ator/<int:ator_id>/concluidas", methods=["GET"])
def listar_ocorrencias_concluidas_por_ator(ator_id):
    with get_db() as db:
        try:
            servico = ServicoDeOcorrencia(db)
            ocorrencias = servico.buscar_concluidas_por_ator(
                ator_id=ator_id,
                implementacao=ServicoDeOcorrenciaDeTarefa
            )
            return jsonify([_serializar_ocorrencia(o) for o in ocorrencias]), 200
        except (NotFoundError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@ocorrencia_tarefa_bp.route("/", methods=["POST"])
def criar_ocorrencia_de_tarefa():
    with get_db() as db:
        dados = request.get_json()
        tarefa_id = dados.get("tarefa_id")
        data_prevista = dados.get("data_prevista")
        status = dados.get("status", False) 

        if not all([tarefa_id, data_prevista]):
            return jsonify({"erro": "Os campos 'tarefa_id' e 'data_prevista' são obrigatórios."}), 400
        
        try:
            servico = ServicoDeOcorrencia(db)
            nova_ocorrencia = servico.criar_unica(
                item_id=tarefa_id, 
                data_str=data_prevista, 
                status=status,
                implementacao=ServicoDeOcorrenciaDeTarefa
            )
            return jsonify({
                "mensagem": "Ocorrência de tarefa criada com sucesso.",
                "ocorrencia": _serializar_ocorrencia(nova_ocorrencia)
            }), 201
        except (NotFoundError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@ocorrencia_tarefa_bp.route("/<int:ocorrencia_id>", methods=["PUT"])
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
                implementacao=ServicoDeOcorrenciaDeTarefa
            )
            return jsonify({
                "mensagem": "Ocorrência atualizada com sucesso.",
                "ocorrencia": _serializar_ocorrencia(ocorrencia_atualizada)
            }), 200
        except (NotFoundError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@ocorrencia_tarefa_bp.route("/<int:ocorrencia_id>", methods=["DELETE"])
def remover_ocorrencia(ocorrencia_id):
    with get_db() as db:
        try:
            servico = ServicoDeOcorrencia(db)
            servico.remover(
                ocorrencia_id=ocorrencia_id,
                implementacao=ServicoDeOcorrenciaDeTarefa
            )
            return '', 204
        except (NotFoundError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@ocorrencia_tarefa_bp.route("/ator/<int:ator_id>/data", methods=["GET"])
def listar_ocorrencias_por_data(ator_id):
    """
    Ex: /ator/1/data?data_inicio=2025-07-01&data_fim=2025-07-31
    """
    with get_db() as db:
        data_inicio = request.args.get("data_inicio")
        data_fim = request.args.get("data_fim")
        try:
            servico = ServicoDeOcorrencia(db)
            ocorrencias = servico.buscar_por_data(
                ator_id=ator_id, 
                data_inicio=data_inicio, 
                data_fim=data_fim,
                implementacao=ServicoDeOcorrenciaDeTarefa
            )
            return jsonify([_serializar_ocorrencia(o) for o in ocorrencias]), 200
        except (NotFoundError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@ocorrencia_tarefa_bp.route("/ator/<int:ator_id>/data_especifica", methods=["GET"])
def listar_ocorrencias_por_data_especifica(ator_id):
    """
    Ex: /ator/1/data_especifica?data=2025-07-15
    """
    with get_db() as db:
        data_especifica = request.args.get("data")
        if not data_especifica:
            return jsonify({"erro": "O parâmetro 'data' é obrigatório."}), 400
        try:
            servico = ServicoDeOcorrencia(db)
            ocorrencias = servico.buscar_por_data_especifica(
                ator_id=ator_id, 
                data_especifica=data_especifica,
                implementacao=ServicoDeOcorrenciaDeTarefa
            )
            return jsonify([_serializar_ocorrencia(o) for o in ocorrencias]), 200
        except (NotFoundError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

        
# O conteúdo abaixo não é um único arquivo JSON, mas sim uma
# coleção de exemplos de como chamar cada rota da sua API.

# --------------------------------------------------------------------
# 1. Listar todas as ocorrências de um ator
# --------------------------------------------------------------------
# Método: GET
# Rota:   /ocorrencias-tarefa/ator/1
#
# Descrição: Busca todas as ocorrências de tarefas associadas ao ator de ID 1.
# Corpo da Requisição: (Nenhum)


# --------------------------------------------------------------------
# 2. Listar apenas as ocorrências CONCLUÍDAS de um ator
# --------------------------------------------------------------------
# Método: GET
# Rota:   /ocorrencias-tarefa/ator/1/concluidas
#
# Descrição: Busca apenas as ocorrências de tarefas que já foram marcadas
# como concluídas (status: true) para o ator de ID 1.
# Corpo da Requisição: (Nenhum)


# --------------------------------------------------------------------
# 3. Criar uma nova ocorrência de tarefa
# --------------------------------------------------------------------
# Método: POST
# Rota:   /ocorrencias-tarefa/
#
# Descrição: Cria manualmente uma ocorrência para a tarefa de ID 5.
# O status é opcional e, se não for enviado, será 'false' por padrão.
#
# Corpo da Requisição (Body):
# {
#     "tarefa_id": 5,
#     "data_prevista": "2025-08-10",
#     "status": false
# }


# --------------------------------------------------------------------
# 4. Atualizar o status de uma ocorrência (Marcar como concluída)
# --------------------------------------------------------------------
# Método: PUT
# Rota:   /ocorrencias-tarefa/10
#
# Descrição: Atualiza o status da ocorrência de ID 10 para 'true',
# indicando que a tarefa foi concluída.
#
# Corpo da Requisição (Body):
# {
#     "status": true
# }


# --------------------------------------------------------------------
# 5. Remover uma ocorrência de tarefa
# --------------------------------------------------------------------
# Método: DELETE
# Rota:   /ocorrencias-tarefa/10
#
# Descrição: Remove a ocorrência de tarefa com ID 10.
# Corpo da Requisição: (Nenhum)


# --------------------------------------------------------------------
# 6. Listar ocorrências por intervalo de datas
# --------------------------------------------------------------------
# Método: GET
# Rota:   /ocorrencias-tarefa/ator/1/data?data_inicio=2025-08-01&data_fim=2025-08-31
#
# Descrição: Busca todas as ocorrências do ator 1 que têm data_prevista
# entre 01/08/2025 e 31/08/2025. Os parâmetros são enviados na URL.
# Corpo da Requisição: (Nenhum)


# --------------------------------------------------------------------
# 7. Listar ocorrências em uma data específica
# --------------------------------------------------------------------
# Método: GET
# Rota:   /ocorrencias-tarefa/ator/1/data_especifica?data=2025-08-10
#
# Descrição: Busca todas as ocorrências do ator 1 que têm data_prevista
# exatamente no dia 10/08/2025. O parâmetro é enviado na URL.
# Corpo da Requisição: (Nenhum)

