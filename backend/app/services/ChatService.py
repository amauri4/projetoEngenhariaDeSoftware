from app.repositories.UsuarioRepositories import UserRepository
from app.repositories.HabitoUsuarioRepository import HabitoUsuarioRepository
from app.repositories.CategoriaRepository import CategoriaRepository
from app.repositories.ChatRepository import ChatRepository
from app.models.HistoricoChat import HistoricoChat
from app.clients.GroqClient import GroqClient
from app.services.StrategyPrompt.PromptStrategy import PromptStrategy

class ChatService:
    def __init__(
        self,
        usuario_repo: UserRepository,
        habito_repo: HabitoUsuarioRepository,
        categoria_repo: CategoriaRepository,
        chat_repo: ChatRepository,
        groq_client: GroqClient,
        prompt_strategy: PromptStrategy
    ):
        self.usuario_repo = usuario_repo
        self.habito_repo = habito_repo
        self.categoria_repo = categoria_repo
        self.chat_repo = chat_repo
        self.groq_client = groq_client
        self.prompt_strategy = prompt_strategy

    def processar_mensagem(self, user_id: int, mensagem: str) -> str:
        usuario = self.usuario_repo.buscar_por_id(user_id)
        if not usuario:
            return "Usuário não encontrado."

        mensagem_usuario = HistoricoChat(
            ator_id=user_id,
            quem_enviou='user',
            mensagem=mensagem
        )
        self.chat_repo.salvar_mensagem(mensagem_usuario)

        prompt_usuario = self.prompt_strategy.montar_prompt(user_id, mensagem)
        system_prompt = self.prompt_strategy.get_system_prompt()

        historico = self.chat_repo.buscar_ultimas_mensagens(user_id, limite=10)

        if historico:
            contexto_conversa = "\n".join(
                [f"{msg.quem_enviou}: {msg.mensagem}" for msg in historico]
            )

        prompt_completo = f"{system_prompt}\n\n{contexto_conversa}\n\n{prompt_usuario}".strip()

        resposta = self.groq_client.gerar_resposta_chat(system_prompt, prompt_usuario)

        mensagem_bot = HistoricoChat(
            ator_id=user_id,
            quem_enviou='bot',
            mensagem=resposta
        )
        self.chat_repo.salvar_mensagem(mensagem_bot)

        return resposta
