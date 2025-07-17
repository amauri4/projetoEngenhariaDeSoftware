from flask import Blueprint, request, jsonify
from app.models.Aplicacao1.UsuarioPessoal import UsuarioPessoal
from app.database.session import get_db
from app.services.Framework.UsuarioService import UserService
from app.utils.jwt import criar_token

auth1_bp = Blueprint("auth1", __name__, url_prefix="/auth1")
@auth1_bp.route("/registrar", methods=["POST"])
def registrar_usuario():
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")

    try:
        with get_db() as db: 
            service = UserService(db)
            usuario = service.criar_usuario(UsuarioPessoal(nome=nome,email=email, senha_hash=senha))
            return jsonify({
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email
            }), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@auth1_bp.route("/login", methods=["POST"])
def login_usuario():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    try:
        with get_db() as db:
            service = UserService(db)
            usuario = service.autenticar_usuario(email=email, senha=senha)
            
            token = criar_token({"usuario_id": usuario.id, "email": usuario.email})

            return jsonify({
                "access_token": token,
                "usuario": {
                    "id": usuario.id,
                    "nome": usuario.nome,
                    "email": usuario.email
                }
            }), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 401