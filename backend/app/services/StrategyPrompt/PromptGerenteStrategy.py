from app.services.StrategyPrompt.PromptStrategy import PromptStrategy
from app.repositories.Aplicacao2.GerenteRepository import GerenteRepository
from app.repositories.Aplicacao2.TarefaRepository import TarefaRepository
from app.database import session
from typing import Any

class PromptGerenteStrategy(PromptStrategy):
    def __init__(self, db: session):
        self.db = db
        self.gerente_repo = GerenteRepository(db)
        self.tarefa_repo = TarefaRepository(db)
        self.contexto = """
        Você é um assistente especializado em ajudar gerentes a coordenarem suas equipes e tarefas de forma eficiente, clara e organizada. Seu papel é facilitar o gerenciamento de tarefas, delegação e acompanhamento de progresso.

        ### Regras principais:
        - Responda com foco em **produtividade, delegação e acompanhamento de equipe**.
        - Use **tópicos ou listas** sempre que possível para organizar a resposta.
        - Vá direto ao ponto: **sem introduções, sem conclusões**.
        - Forneça sugestões claras para melhorar a eficiência da equipe.
        - Ajude o gerente a identificar prioridades, redistribuir tarefas e acompanhar resultados.
        - Não seja genérico: adapte-se às tarefas e equipe apresentadas.

        ### Limitações:
        - Não forneça conselhos jurídicos, médicos ou financeiros.
        - Mantenha o foco em **gestão de pessoas e tarefas**.

        Seu objetivo é fornecer **respostas práticas e aplicáveis** que ajudem o gerente a agir imediatamente.
        """.strip()

    def montar_prompt(self, user_id: int, mensagem: str) -> str:
        try:
            gerente = self.gerente_repo.buscar_por_id(user_id)
            if not gerente:
                return "Gerente não encontrado."

            equipe = self.gerente_repo.buscar_equipe_por_gerente(user_id)
            tarefas = self.gerente_repo.buscar_tarefas_criadas_por_gerente(user_id)

            lista_funcionarios = [
                f"- {f.nome} (email: {f.email})" for f in equipe
            ]

            lista_tarefas = []
            for t in tarefas:
                funcionario_nome = t.responsavel.nome if t.responsavel else "Não atribuída"
                prazo = t.prazo_final if t.prazo_final else "Sem prazo"
                data_inicio = t.data_inicio if t.data_inicio else "Não informado"

                lista_tarefas.append(
                    f"- {t.descricao} (atribuída para: {funcionario_nome}, início: {data_inicio}, prazo: {prazo})"
                )

            prompt = (
                f"Gerente: {gerente.nome} (email: {gerente.email})\n"
                f"\nEquipe:\n" +
                ("\n".join(lista_funcionarios) if lista_funcionarios else "Nenhum funcionário na equipe.") +
                "\n\nTarefas criadas:\n" +
                ("\n".join(lista_tarefas) if lista_tarefas else "Nenhuma tarefa criada.") +
                f"\n\nPergunta do gerente: {mensagem}"
            )
            return prompt
        except Exception as e:
            return f"Ocorreu um erro ao montar o prompt: {str(e)}"
