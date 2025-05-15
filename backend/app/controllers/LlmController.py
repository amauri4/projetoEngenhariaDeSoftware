from flask import Blueprint, request, jsonify
import requests

llm_bp = Blueprint("llm", __name__, url_prefix="/llm")

OLLAMA_URL = "http://localhost:11434/api/generate"

@llm_bp.route("/chat", methods=["POST"])
def llm_chat():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Requisição sem JSON"}), 400

    user_name = data.get("user_name")
    message = data.get("message")
    habits = data.get("habits", [])

    if not user_name or not message:
        return jsonify({"error": "Faltando user_name ou message"}), 400

    prompt = f"Usuário: {user_name}\n"
    prompt += "Hábitos atuais:\n"
    for habito in habits:
        prompt += f"- {habito.get('nome')}: {habito.get('descricao')}\n"
    prompt += f"Pergunta do usuário: {message}\n"
    prompt += "Resposta da IA (dicas, sugestões):"

    
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "max_tokens": 300,
        "temperature": 0.7,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        answer = result.get("response", "").strip()

        return jsonify({"response": answer})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erro ao chamar Ollama: {str(e)}"}), 500