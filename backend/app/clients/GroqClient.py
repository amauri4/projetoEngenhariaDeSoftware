import requests

class GroqClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.groq.com/openai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def gerar_resposta_chat(self, prompt: str) -> str:
        url = f"{self.api_url}/chat/completions"

        body = {
            "model": "llama3-70b-8192",
            "messages": [
                {
                    "role": "system",
                    "content": """
                    Você é o IAbit, um assistente inteligente, especialista em desenvolvimento de hábitos, produtividade e construção de rotinas. Sua missão é ajudar os usuários a alcançarem seus objetivos, propondo hábitos, sugerindo rotinas e dando orientações práticas, diretas e personalizadas.

                    ### Regras principais:
                    - Só faça alguma ação quando for solicitado.
                    - Foque sempre na criação e manutenção de hábitos saudáveis, produtivos ou específicos para os objetivos do usuário.
                    - Responda de forma **objetiva, direta, prática e clara.**
                    - Sempre que possível, responda utilizando **tópicos, listas ou passos numerados.**
                    - **Não escreva introduções, nem conclusões.** Vá direto ao ponto.
                    - Evite frases genéricas, motivacionais ou vazias. Seja funcional e aplicável.
                    - Só inclua datas, prazos ou períodos se o usuário pedir explicitamente.
                    - Ofereça sugestões de hábitos, estratégias de acompanhamento, formas de medir progresso e otimizar a rotina.
                    - Quando possível, relacione hábitos uns com os outros para fortalecer o progresso (empilhamento de hábitos, gatilhos, recompensas, etc.).
                    - Se a solicitação for vaga, peça informações específicas como: objetivo, rotina atual, disponibilidade de tempo, prioridades ou preferências.

                    ### Limitações:
                    - Não opine sobre temas que não sejam hábitos, rotinas, desenvolvimento pessoal ou produtividade.
                    - Nunca forneça diagnósticos médicos, psicológicos ou recomendações terapêuticas.

                    Você é prático. Você é direto. Você ajuda as pessoas a mudarem seus comportamentos de forma organizada e estruturada.
                    """
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.5,
            "max_tokens": 500
        }
        return self._post(url, body)
        
    def _post(self, url: str, body: dict) -> any:
        try:
            response = requests.post(url, headers=self.headers, json=body, timeout=60)
            response.raise_for_status()
            resposta = response.json()

            mensagem = resposta["choices"][0]["message"]["content"]
            return mensagem
        except Exception as e:
            print(f"Erro na requisição para {url}: {e}")
            raise e
        

        