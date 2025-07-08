from app.repositories.ChatRepository import ChatRepository
from app.models.HistoricoChat import HistoricoChat
from app.clients.GroqClient import GroqClient
from app.services.StrategyPrompt.PromptStrategy import PromptStrategy

class ChatService:
    def __init__(
        self,
        chat_repo: ChatRepository,
        groq_client: GroqClient,
        prompt_strategy: PromptStrategy
    ):
        self.chat_repo = chat_repo
        self.groq_client = groq_client
        self.prompt_strategy = prompt_strategy

    def processar_mensagem(self, user_id: int, mensagem: str) -> str:
        usuario = self.prompt_strategy.montar_prompt(user_id, mensagem)
        if "não encontrado" in usuario.lower():
            return usuario

        mensagem_usuario = HistoricoChat(
            ator_id=user_id,
            quem_enviou='user',
            mensagem=mensagem
        )
        self.chat_repo.salvar_mensagem(mensagem_usuario)

        prompt_usuario = self.prompt_strategy.montar_prompt(user_id, mensagem)
        system_prompt = self.prompt_strategy.criar_contexto_chat()

        historico = self.chat_repo.buscar_ultimas_mensagens(user_id, limite=10)

        if historico:
            contexto_conversa = "\n".join(
                [f"{msg.quem_enviou}: {msg.mensagem}" for msg in historico]
            )

        prompt_com_historico = f"{contexto_conversa}\n\n{prompt_usuario}".strip()

        resposta = self.groq_client.gerar_resposta_chat(system_prompt, prompt_com_historico)

        mensagem_bot = HistoricoChat(
            ator_id=user_id,
            quem_enviou='bot',
            mensagem=resposta
        )
        self.chat_repo.salvar_mensagem(mensagem_bot)

        return resposta
