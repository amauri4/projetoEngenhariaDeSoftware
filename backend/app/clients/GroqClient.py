import requests

class GroqClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.groq.com/openai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def gerar_resposta_chat(self, system_prompt: str, user_prompt: str) -> str:
        url = f"{self.api_url}/chat/completions"

        body = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.5,
            "max_tokens": 500
        }
        return self._post(url, body)

    def _post(self, url: str, body: dict) -> str:
        try:
            response = requests.post(url, headers=self.headers, json=body, timeout=60)
            response.raise_for_status()
            resposta = response.json()

            mensagem = resposta["choices"][0]["message"]["content"]
            return mensagem
        except Exception as e:
            print(f"Erro na requisição para {url}: {e}")
            raise e
