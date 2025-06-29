from app.repositories.UsuarioRepositories import UserRepository
from app.repositories.HabitoUsuarioRepository import HabitoUsuarioRepository
from app.repositories.CategoriaRepository import CategoriaRepository
from app.repositories.ChatRepository import ChatRepository
from app.models.HistoricoChat import HistoricoChat
from app.clients.GroqClient import GroqClient

class ChatService:
    def __init__(
        self,
        usuario_repo: UserRepository,
        habito_repo: HabitoUsuarioRepository,
        categoria_repo: CategoriaRepository,
        chat_repo: ChatRepository,
        groq_client: GroqClient

    ):
        self.usuario_repo = usuario_repo
        self.habito_repo = habito_repo
        self.categoria_repo = categoria_repo
        self.chat_repo = chat_repo
        self.groq_client = groq_client

    def montar_prompt(self, user_id: int, mensagem: str) -> str:
        usuario = self.usuario_repo.buscar_por_id(user_id)
        habitos = self.habito_repo.buscar_por_usuario(user_id)
        categorias = self.categoria_repo.buscar_categorias_por_usuario(user_id)

        if not usuario:
            return "Usuário não encontrado."

        lista_habitos = []
        for h in habitos:
            nome_habito = h.habito_base.nome
            descricao = h.descricao
            frequencia = h.frequencia.name
            data_inicio = h.data_inicio
            categoria = h.habito_base.categoria.nome if h.habito_base.categoria else "Sem categoria"

            lista_habitos.append(
                f"- {nome_habito} (descrição: {descricao}, frequência: {frequencia}, categoria: {categoria}, iniciado em {data_inicio})"
            )

        prompt = (
            f"Usuário: {usuario.nome} (email: {usuario.email})\n"
            f"Hábito(s) cadastrado(s):\n"
            + ("\n".join(lista_habitos) if lista_habitos else "Nenhum hábito cadastrado.") +
            f"\n\nPergunta do usuário: {mensagem}\n"
        )
        return prompt

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

        prompt = self.montar_prompt(user_id, mensagem)

        historico = self.chat_repo.buscar_ultimas_mensagens(user_id, limite=10)
        if historico:
            contexto_conversa = "\n".join(
                [f"{msg.quem_enviou}: {msg.mensagem}" for msg in historico]
            )
            prompt = f"{contexto_conversa}\n\n{prompt}"

        resposta = self.groq_client.gerar_resposta_chat(prompt)

        mensagem_bot = HistoricoChat(
            ator_id=user_id,
            quem_enviou='bot',
            mensagem=resposta
        )
        self.chat_repo.salvar_mensagem(mensagem_bot)

        return resposta