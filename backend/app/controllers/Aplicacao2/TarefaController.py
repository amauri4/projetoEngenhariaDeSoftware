from flask import Blueprint, jsonify, request
from app.database.session import get_db
from app.services.ItemService import ServicoDeItem 
from app.services.TemplateMethodItem.Tarefa import TarefaEstrategiaService
from app.exceptions.service_exceptions import AuthError, ConflictError, ServiceError
from app.exceptions.repository_exceptions import NotFoundError

tarefa_bp = Blueprint("tarefas", __name__, url_prefix="/tarefas")

@tarefa_bp.route("/ator/<int:ator_id>", methods=["GET"])
def listar_tarefas_por_ator(ator_id):
    with get_db() as db:
        try:
            servico = ServicoDeItem(db)
            tarefas = servico.buscar_por_ator(ator_id, TarefaEstrategiaService)
            tarefas_json = []
            for t in tarefas:
                tarefa_json = {
                    "id": t.id,
                    "descricao": t.descricao,
                    "data_inicio": t.data_inicio.isoformat() if t.data_inicio else None,
                    "prazo_final": t.prazo_final.isoformat() if t.prazo_final else None,
                    "criador_id": t.ator_id,
                    "criador_nome": t.criador.nome if t.criador else None,
                    "responsavel_id": t.id_funcionario_responsavel,
                    "responsavel_nome": t.responsavel.nome if t.responsavel else None
                }
                tarefas_json.append(tarefa_json)

            return jsonify(tarefas_json), 200
        except (NotFoundError, AuthError, ConflictError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@tarefa_bp.route("/gerente/<int:gerente_id>", methods=["POST"])
def adicionar_tarefa(gerente_id):
    with get_db() as db:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400

        try:
            servico = ServicoDeItem(db)
            nova_tarefa = servico.adicionar(
                ator_id=gerente_id, 
                dados=dados, 
                implementacao=TarefaEstrategiaService
            )

            return jsonify({
                "mensagem": "Tarefa adicionada com sucesso.",
                "tarefa": { "id": nova_tarefa.id, "descricao": nova_tarefa.descricao }
            }), 201
        except (NotFoundError, AuthError, ConflictError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@tarefa_bp.route("/<int:tarefa_id>", methods=["PUT"])
def atualizar_tarefa(tarefa_id):
    with get_db() as db:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400

        try:
            servico = ServicoDeItem(db)
            tarefa_atualizada = servico.atualizar(
                item_id=tarefa_id, 
                dados=dados, 
                implementacao=TarefaEstrategiaService
            )

            return jsonify({
                "mensagem": "Tarefa atualizada com sucesso.",
                "tarefa": { "id": tarefa_atualizada.id, "descricao": tarefa_atualizada.descricao }
            }), 200
        except (NotFoundError, AuthError, ConflictError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@tarefa_bp.route("/<int:tarefa_id>", methods=["DELETE"])
def remover_tarefa(tarefa_id):
    with get_db() as db:
        try:
            servico = ServicoDeItem(db)
            servico.remover(
                item_id=tarefa_id, 
                implementacao=TarefaEstrategiaService
            )

            return '', 204
        except (NotFoundError, AuthError, ConflictError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

#  --------------------------------------------------------------------
#  1. Adicionar uma nova tarefa
#  --------------------------------------------------------------------
#  Método: POST
#  Rota:   /tarefas/gerente/1
# 
#  Descrição: O Gerente com ID 1 está criando uma nova tarefa e
#  atribuindo-a ao Funcionário com ID 2.
# 
#  Corpo da Requisição (Body):
# {
#     "descricao": "Elaborar o relatório de performance do segundo trimestre",
#     "data_inicio": "2025-07-14",
#     "responsavel_id": 2,
#     "prazo_final": "2025-07-25"
# }


#  --------------------------------------------------------------------
#  2. Listar tarefas relacionadas a um ator
#  --------------------------------------------------------------------
# 
#  Exemplo A: Listar tarefas CRIADAS pelo Gerente de ID 1
#  Método: GET
#  Rota:   /tarefas/ator/1
#  Corpo da Requisição: (Nenhum)
# 
# 
#  Exemplo B: Listar tarefas ATRIBUÍDAS ao Funcionário de ID 2
#  Método: GET
#  Rota:   /tarefas/ator/2
#  Corpo da Requisição: (Nenhum)


#  --------------------------------------------------------------------
#  3. Atualizar uma tarefa existente
#  --------------------------------------------------------------------
#  Método: PUT
#  Rota:   /tarefas/3  (Assumindo que a tarefa criada no passo 1 recebeu o ID 3)
# 
#  Descrição: Atualiza a descrição e o prazo da tarefa.
#  Você pode enviar apenas os campos que deseja alterar.
# 
#  Corpo da Requisição (Body):
# {
#     "descricao": "Elaborar e apresentar o relatório de performance do Q2",
#     "prazo_final": "2025-07-28"
# }


#  --------------------------------------------------------------------
#  4. Remover uma tarefa
#  --------------------------------------------------------------------
#  Método: DELETE
#  Rota:   /tarefas/3
#  Corpo da Requisição: (Nenhum)
# 
#  Descrição: Remove permanentemente a tarefa com ID 3 do sistema.
#  Se a operação for bem-sucedida, a API retornará uma resposta vazia
#  com o status HTTP 204 No Content.


