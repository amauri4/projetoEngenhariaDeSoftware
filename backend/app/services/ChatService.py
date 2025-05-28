# services/chat_service.py
from app.repositories.UsuarioRepositories import UserRepository
from app.repositories.HabitoUsuarioRepository import HabitoUsuarioRepository
from app.repositories.CategoriaRepository import CategoriaRepository
from app.services.GroqService import chamar_modelo_groq

class ChatService:
    def __init__(self, usuario_repo: UserRepository, habito_repo: HabitoUsuarioRepository, categoria_repo: CategoriaRepository):
        self.usuario_repo = usuario_repo
        self.habito_repo = habito_repo
        self.categoria_repo = categoria_repo

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
        prompt = self.montar_prompt(user_id, mensagem)
        resposta = chamar_modelo_groq(prompt)
        return resposta
