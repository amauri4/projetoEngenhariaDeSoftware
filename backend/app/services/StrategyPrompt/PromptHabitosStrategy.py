from app.services.StrategyPrompt.PromptStrategy import PromptStrategy
from app.repositories.UsuarioRepositories import UserRepository
from app.repositories.HabitoUsuarioRepository import HabitoUsuarioRepository
from app.repositories.CategoriaRepository import CategoriaRepository
from app.database import session 
from typing import Any


class PromptHabitosStrategy(PromptStrategy):
    def __init__(self, db: session):
        self.db = db
        self.usuario_repo = UserRepository(db)
        self.habito_repo = HabitoUsuarioRepository(db)
        self.categoria_repo = CategoriaRepository(db)

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

    def get_system_prompt(self) -> str:
        return """
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
        """.strip()
