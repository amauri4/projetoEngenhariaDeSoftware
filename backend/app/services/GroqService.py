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
            {"role": "system", "content": "Você é o IAbit um assistente especialista em hábitos e bem-estar do HabitTracker. Responda de forma breve, clara e prática. Não precisa informar a data de inicio dos hábitos"},
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
