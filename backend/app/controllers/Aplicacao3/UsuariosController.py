from flask import Blueprint, jsonify, request
from app.database.session import get_db
from app.services.Aplicacao3.InstrutorService import InstrutorService
from app.services.Aplicacao3.AlunoService import AlunoService
from app.exceptions.service_exceptions import AuthError, ConflictError, ServiceError
from app.exceptions.repository_exceptions import NotFoundError

auth3_bp = Blueprint("auth3", __name__, url_prefix="/auth3")


@auth3_bp.route("/instrutores/registrar", methods=["POST"])
def registrar_instrutor():
    with get_db() as db:
        dados = request.get_json()
        if not dados or not all(k in dados for k in ["nome", "email", "senha"]):
            return jsonify({"erro": "Os campos 'nome', 'email' e 'senha' são obrigatórios."}), 400
        try:
            servico = InstrutorService(db)
            novo_instrutor = servico.criar_instrutor(
                nome=dados["nome"],
                email=dados["email"],
                senha=dados["senha"]
            )
            return jsonify({
                "mensagem": "Instrutor registrado com sucesso.",
                "instrutor": {
                    "id": novo_instrutor.id,
                    "nome": novo_instrutor.nome,
                    "email": novo_instrutor.email
                }
            }), 201
        except (ConflictError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@auth3_bp.route("/instrutores/login", methods=["POST"])
def login_instrutor():
    with get_db() as db:
        dados = request.get_json()
        if not dados or not all(k in dados for k in ["email", "senha"]):
            return jsonify({"erro": "Os campos 'email' e 'senha' são obrigatórios."}), 400
        try:
            servico = InstrutorService(db)
            instrutor_autenticado = servico.autenticar_instrutor(
                email=dados["email"],
                senha=dados["senha"]
            )
            return jsonify({
                "id": instrutor_autenticado.id,
                "nome": instrutor_autenticado.nome,
                "email": instrutor_autenticado.email,
                "tipo_ator": instrutor_autenticado.tipo_ator
            }), 200
        except (AuthError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 401
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500


@auth3_bp.route("/alunos/registrar", methods=["POST"])
def registrar_aluno():
    with get_db() as db:
        dados = request.get_json()
        if not dados or not all(k in dados for k in ["nome", "email", "senha"]):
            return jsonify({"erro": "Os campos 'nome', 'email' e 'senha' são obrigatórios."}), 400
        try:
            servico = AlunoService(db)
            novo_aluno = servico.criar_aluno(
                nome=dados["nome"],
                email=dados["email"],
                senha=dados["senha"],
                instrutor_id=dados.get("instrutor_id")
            )
            return jsonify({
                "mensagem": "Aluno registrado com sucesso.",
                "aluno": {
                    "id": novo_aluno.id,
                    "nome": novo_aluno.nome,
                    "email": novo_aluno.email
                }
            }), 201
        except (ConflictError, NotFoundError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@auth3_bp.route("/alunos/login", methods=["POST"])
def login_aluno():
    with get_db() as db:
        dados = request.get_json()
        if not dados or not all(k in dados for k in ["email", "senha"]):
            return jsonify({"erro": "Os campos 'email' e 'senha' são obrigatórios."}), 400
        try:
            servico = AlunoService(db)
            aluno_autenticado = servico.autenticar_aluno(
                email=dados["email"],
                senha=dados["senha"]
            )
            return jsonify({
                "id": aluno_autenticado.id,
                "nome": aluno_autenticado.nome,
                "email": aluno_autenticado.email,
                "tipo_ator": aluno_autenticado.tipo_ator
            }), 200
        except (AuthError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 401
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500
        
@auth3_bp.route("/<int:instrutor_id>/alunos", methods=["GET"])
def listar_equipe_do_gerente(instrutor_id):
    with get_db() as db:
        try:
            servico = InstrutorService(db)
            alunos = servico.buscar_alunos(instrutor_id)

            alunos_json = [
                {
                    "id": aluno.id,
                    "nome": aluno.nome,
                    "email": aluno.email
                }
                for aluno in alunos
            ]

            return jsonify(alunos_json), 200
        except NotFoundError as e:
            return jsonify({"erro": str(e)}), 404
        except ServiceError as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500
