from flask import Blueprint, jsonify, request
from app.database.session import get_db
from app.services.Aplicacao2.GerenteService import GerenteService
from app.services.Aplicacao2.FuncionarioService import FuncionarioService
from app.exceptions.service_exceptions import AuthError, ConflictError, ServiceError
from app.exceptions.repository_exceptions import NotFoundError

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# --- ROTAS PARA CHEFES ---

@auth_bp.route("/gerentes/registrar", methods=["POST"])
def registrar_gerente():
    with get_db() as db:
        dados = request.get_json()
        if not dados or not all(k in dados for k in ["nome", "email", "senha"]):
            return jsonify({"erro": "Os campos 'nome', 'email' e 'senha' são obrigatórios."}), 400

        try:
            servico = GerenteService(db)
            novo_gerente = servico.criar_gerente(
                nome=dados["nome"],
                email=dados["email"],
                senha=dados["senha"]
            )
            return jsonify({
                "mensagem": "Gerente registrado com sucesso.",
                "gerente": {
                    "id": novo_gerente.id,
                    "nome": novo_gerente.nome,
                    "email": novo_gerente.email
                }
            }), 201
        except (ConflictError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@auth_bp.route("/gerentes/login", methods=["POST"])
def login_gerente():
    with get_db() as db:
        dados = request.get_json()
        if not dados or not all(k in dados for k in ["email", "senha"]):
            return jsonify({"erro": "Os campos 'email' e 'senha' são obrigatórios."}), 400

        try:
            servico = GerenteService(db)
            gerente_autenticado = servico.autenticar_gerente(
                email=dados["email"],
                senha=dados["senha"]
            )
            return jsonify({
                "id": gerente_autenticado.id,
                "nome": gerente_autenticado.nome,
                "email": gerente_autenticado.email,
                "tipo_ator": gerente_autenticado.tipo_ator
            }), 200
        except (AuthError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 401
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

# --- ROTAS PARA FUNCIONÁRIOS ---

@auth_bp.route("/funcionarios/registrar", methods=["POST"])
def registrar_funcionario():
    with get_db() as db:
        dados = request.get_json()
        if not dados or not all(k in dados for k in ["nome", "email", "senha"]):
            return jsonify({"erro": "Os campos 'nome', 'email' e 'senha' são obrigatórios."}), 400

        try:
            servico = FuncionarioService(db)
            novo_funcionario = servico.criar_funcionario(
                nome=dados["nome"],
                email=dados["email"],
                senha=dados["senha"],
                chefe_id=dados.get("chefe_id")  # chefe_id é opcional
            )
            return jsonify({
                "mensagem": "Funcionário registrado com sucesso.",
                "funcionario": {
                    "id": novo_funcionario.id,
                    "nome": novo_funcionario.nome,
                    "email": novo_funcionario.email,
                    "chefe_id": novo_funcionario.chefe_id
                }
            }), 201
        except (ConflictError, NotFoundError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

@auth_bp.route("/funcionarios/login", methods=["POST"])
def login_funcionario():
    with get_db() as db:
        dados = request.get_json()
        if not dados or not all(k in dados for k in ["email", "senha"]):
            return jsonify({"erro": "Os campos 'email' e 'senha' são obrigatórios."}), 400

        try:
            servico = FuncionarioService(db)
            funcionario_autenticado = servico.autenticar_funcionario(
                email=dados["email"],
                senha=dados["senha"]
            )
            return jsonify({
                "id": funcionario_autenticado.id,
                "nome": funcionario_autenticado.nome,
                "email": funcionario_autenticado.email,
                "tipo_ator": funcionario_autenticado.tipo_ator,
                "chefe_id": funcionario_autenticado.chefe_id
            }), 200
        except (AuthError, ServiceError) as e:
            return jsonify({"erro": str(e)}), 401
        except Exception as e:
            return jsonify({"erro": f"Ocorreu um erro inesperado: {e}"}), 500

# --- Exemplos de Requisições JSON para Testes ---

# 1. Registrar um novo Gerente
# POST /auth/gerentes/registrar
# {
#     "nome": "Ana Silva",
#     "email": "ana.silva@empresa.com",
#     "senha": "senhaForte123"
# }

# 2. Fazer login como Gerente
# POST /auth/gerentes/login
# {
#     "email": "ana.silva@empresa.com",
#     "senha": "senhaForte123"
# }

# 3. Registrar um novo Funcionário (sem chefe)
# POST /auth/funcionarios/registrar
# {
#     "nome": "Carlos Pereira",
#     "email": "carlos.pereira@empresa.com",
#     "senha": "outraSenha456"
# }

# 4. Registrar um novo Funcionário (com chefe)
# POST /auth/funcionarios/registrar
# {
#     "nome": "Beatriz Costa",
#     "email": "beatriz.costa@empresa.com",
#     "senha": "senhaDaBia789",
#     "chefe_id": 1 # ID do gerente 'Ana Silva' criado anteriormente
# }

# 5. Fazer login como Funcionário
# POST /auth/funcionarios/login
# {
#     "email": "carlos.pereira@empresa.com",
#     "senha": "outraSenha456"
# }

