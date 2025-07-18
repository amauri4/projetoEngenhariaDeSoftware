from app.repositories.Framework.ChatRepository import ChatRepository
from app.clients.GroqClient import GroqClient
from app.services.Framework.IStrategyPrompt import IStrategyPrompt

class ChatService:
    def __init__(
        self,
        chat_repo: ChatRepository,
        groq_client: GroqClient,
        prompt_strategy: IStrategyPrompt
    ):
        self.chat_repo = chat_repo
        self.groq_client = groq_client
        self.prompt_strategy = prompt_strategy

    def processar_mensagem(self, user_id: int, mensagem: str) -> str:
        prompt_usuario = self.prompt_strategy.montar_prompt(user_id, mensagem)
        if "não encontrado" in prompt_usuario.lower():
            return prompt_usuario

        self.chat_repo.criar_historicochat(user_id, mensagem, 'user')

        system_prompt = self.prompt_strategy.contexto

        historico = self.chat_repo.buscar_ultimas_mensagens(user_id, limite=10)

        if historico:
            contexto_conversa = "\n".join(
                [f"{msg.quem_enviou}: {msg.mensagem}" for msg in historico]
            )

        prompt_com_historico = f"{contexto_conversa}\n\n{prompt_usuario}".strip()

        resposta = self.groq_client.gerar_resposta_chat(system_prompt, prompt_com_historico)

        self.chat_repo.criar_historicochat(user_id, resposta, 'bot')

        return resposta
