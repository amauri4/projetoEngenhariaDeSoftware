from flask import Blueprint, request, jsonify
from app.services.Framework.ChatService import ChatService
from app.repositories.Framework.AtorRepository import AtorRepository
from app.repositories.Framework.ChatRepository import ChatRepository
from app.repositories.Framework.RegistroDeOcorrenciaRepository import RegistroDeOcorrenciaRepository
from app.clients.GroqClient import GroqClient
from app.database.session import get_db
from pathlib import Path
from dotenv import load_dotenv
import traceback
import os
from app.services.Aplicacao2.PromptGerenteStrategy import PromptGerenteStrategy
from app.services.Framework.ChatService import ChatService


chat2_bp = Blueprint("chat2", __name__, url_prefix="/chat2")


def build_chat_service(db):
    chat_repo = ChatRepository(db)

    load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".test.env")

    groq_api_key = os.getenv("GROQ_API_KEY")
    groq_client = GroqClient(api_key=groq_api_key)

    prompt_strategy = PromptGerenteStrategy(db)

    return ChatService(
        chat_repo=chat_repo,
        groq_client=groq_client,
        prompt_strategy=prompt_strategy 
    )


@chat2_bp.route("", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        mensagem = data.get("mensagem")

        if not user_id or not mensagem:
            return jsonify({"erro": "user_id e mensagem são obrigatórios"}), 400

        with get_db() as db:
            chat_service = build_chat_service(db)
            resposta = chat_service.processar_mensagem(user_id, mensagem)

        return jsonify({"resposta": resposta}), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "erro": "Erro interno no servidor",
            "detalhes": str(e)
        }), 500


@chat2_bp.route("/historico/<int:user_id>", methods=["GET"])
def historico(user_id):
    try:
        with get_db() as db:
            chat_service = build_chat_service(db)
            historico = chat_service.chat_repo.buscar_historico_por_usuario(user_id)

            historico_formatado = [
                {
                    "quem_enviou": msg.quem_enviou,
                    "mensagem": msg.mensagem,
                    "timestamp": msg.timestamp.isoformat()
                }
                for msg in historico
            ]

            return jsonify(historico_formatado), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "erro": "Erro ao buscar histórico",
            "detalhes": str(e)
        }), 500


@chat2_bp.route("/historico/<int:user_id>", methods=["DELETE"])
def limpar_historico(user_id):
    try:
        with get_db() as db:
            chat_service = build_chat_service(db)
            chat_service.chat_repo.deletar_historico(user_id)

            return jsonify({"mensagem": "Histórico apagado com sucesso."}), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "erro": "Erro ao apagar histórico",
            "detalhes": str(e)
        }), 500