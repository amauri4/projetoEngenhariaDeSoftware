from flask import Blueprint, request, jsonify
from app.services.ChatService import ChatService
from app.repositories.UsuarioRepositories import UserRepository
from app.repositories.HabitoUsuarioRepository import HabitoUsuarioRepository
from app.repositories.CategoriaRepository import CategoriaRepository
from app.database.session import get_db

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

@chat_bp.route("", methods=["POST"])
def chat():
    data = request.get_json()
    user_id = data.get("user_id")
    mensagem = data.get("mensagem")

    if not user_id or not mensagem:
        return jsonify({"erro": "user_id e mensagem são obrigatórios"}), 400

    try:
        with get_db() as db:
            usuario_repo = UserRepository(db)
            habito_repo = HabitoUsuarioRepository(db)
            categoria_repo = CategoriaRepository(db)

            chat_service = ChatService(
                usuario_repo=usuario_repo,
                habito_repo=habito_repo,
                categoria_repo=categoria_repo
            )

            resposta = chat_service.processar_mensagem(user_id, mensagem)

            return jsonify({"resposta": resposta}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
