import requests
import os

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def chamar_modelo_groq(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "Você é o IAbit, um assistente ultra objetivo e prático sobre hábitos no HabitTracker. Responda apenas com informações claras, diretas e em tópicos sempre que possível. Não use frases longas, não faça introduções ou conclusões, nem comentários adicionais. Seja sucinto."},
            {"role": "system", "content": "Não precisa listar a data de início do hábito, apenas caso seja requisitado"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 300
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=body, timeout=60)
        response.raise_for_status()

        resposta = response.json()
        mensagem = resposta["choices"][0]["message"]["content"]
        return mensagem

    except Exception as e:
        print(f"Erro ao chamar Groq API: {e}")
        return "Ocorreu um erro ao processar sua solicitação com o assistente."
