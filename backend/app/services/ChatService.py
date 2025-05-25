# services/chat_service.py
from app.repositories.UsuarioRepositories import UserRepository
from app.repositories.HabitoUsuarioRepository import HabitoUsuarioRepository
from app.services.GroqService import chamar_modelo_groq

class ChatService:
    def __init__(self, usuario_repo: UserRepository, habito_repo: HabitoUsuarioRepository):
        self.usuario_repo = usuario_repo
        self.habito_repo = habito_repo

    def montar_prompt(self, user_id: int, mensagem: str) -> str:
        usuario = self.usuario_repo.buscar_por_id(user_id)
        habitos = self.habito_repo.buscar_por_usuario(user_id)

        if not usuario:
            return "Usuário não encontrado."

        lista_habitos = []
        for h in habitos:
            lista_habitos.append(f"- {h.habito_base.nome} (descrição: {h.descricao}, frequência: {h.frequencia.name}, iniciado em {h.data_inicio})")

        prompt = (
            f"Usuário: {usuario.nome} (email: {usuario.email})\n"
            f"Hábito(s) cadastrado(s):\n"
            + ("\n".join(lista_habitos) if lista_habitos else "Nenhum hábito cadastrado.") +
            f"\n\nPergunta do usuário: {mensagem}\n"
            "Responda de forma amigável e útil."
        )
        return prompt

    def processar_mensagem(self, user_id: int, mensagem: str) -> str:
        prompt = self.montar_prompt(user_id, mensagem)

        resposta = chamar_modelo_groq(prompt) 

        return resposta
