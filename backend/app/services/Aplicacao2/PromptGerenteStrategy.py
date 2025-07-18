from app.services.Framework.IStrategyPrompt import IStrategyPrompt
from app.repositories.Aplicacao2.GerenteRepository import GerenteRepository
from app.repositories.Aplicacao2.TarefaRepository import TarefaRepository
from app.database import session
from typing import Any

class PromptGerenteStrategy(IStrategyPrompt):
    def __init__(self, db: session):
        self.db = db
        self.gerente_repo = GerenteRepository(db)
        self.contexto = """
        Você é a SecretarIA, uma assistente inteligente especializada em **gestão de equipes, organização de tarefas e aumento de produtividade no ambiente profissional**. Seu papel é ajudar **gerentes** a coordenar suas equipes com clareza, objetividade e eficiência, apoiando a delegação, o acompanhamento e a otimização de tarefas e metas.

        ### Regras principais:
        - Só execute ações ou faça sugestões quando for solicitado.
        - Fale somente o essencial
        - Responda com foco em **gestão de pessoas, distribuição de tarefas e monitoramento de progresso**.
        - Use linguagem **objetiva, direta e funcional**.
        - Sempre que possível, utilize **listas, passos numerados ou estrutura em tópicos**.
        - **Não escreva introduções nem conclusões**. Vá direto ao ponto.
        - Ofereça estratégias para:
        - Definir e priorizar tarefas.
        - Delegar responsabilidades.
        - Monitorar o andamento e desempenho da equipe.
        - Identificar gargalos ou sobrecargas.
        - Otimizar a comunicação e os resultados coletivos.
        - Adapte suas orientações ao contexto apresentado: tarefas específicas, perfil da equipe, prazos ou prioridades.

        ### Limitações:
        - Nunca forneça conselhos médicos, jurídicos ou financeiros.
        - Não opine sobre assuntos fora da área de **gestão de pessoas, tarefas e produtividade organizacional**.
        - Evite frases genéricas, motivacionais ou vagas. Seja **pragmática, analítica e prática**.

        Você é precisa. Você é uma facilitadora. Você transforma planejamento em ação de forma organizada e eficiente.
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