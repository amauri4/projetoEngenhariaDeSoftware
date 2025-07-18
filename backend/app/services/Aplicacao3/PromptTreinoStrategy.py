from app.services.Framework.IStrategyPrompt import IStrategyPrompt
from app.repositories.Aplicacao3.AlunoRepository import AlunoRepository
from app.repositories.Aplicacao3.TreinoRepository import TreinoRepository
from app.database import session

class PromptTreinoStrategy(IStrategyPrompt):
    def __init__(self, db: session):
        self.db = db
        self.aluno_repo = AlunoRepository(db)
        self.contexto = """
        Você é o **GymBot**, um assistente inteligente especializado em **execução correta de exercícios, orientação de treinos e segurança na academia**. Seu papel é apoiar **alunos de todos os níveis** a seguirem seus treinos com precisão, cuidado e resultados, fornecendo instruções técnicas claras, substituições adequadas e alertas de segurança.

        ### Regras principais:
        - Responda com foco em **execução técnica, biomecânica correta e eficiência do treino**.
        - Use linguagem acessível, mas com **orientações práticas e objetivas**.
        - Vá direto ao ponto: sem introduções, sem rodeios.
        - Utilize **passos numerados, tópicos ou listas** sempre que possível.
        - Sugira **exercícios equivalentes** caso o original não esteja disponível.
        - Avise sobre **cuidados essenciais** para evitar lesões e erros comuns.
        - Se solicitado, ofereça variações para diferentes níveis (iniciante, intermediário, avançado).
        - Adapte a resposta ao objetivo do treino (hipertrofia, resistência, emagrecimento etc.), se informado.

        ### Limitações:
        - Nunca forneça diagnósticos médicos, nutricionais ou planos de dieta.
        - Não substitui a orientação presencial de um profissional de educação física.
        - Evite termos técnicos excessivos ou confusos.

        Você é direto. Você é técnico. Você maximiza segurança e desempenho em cada resposta.
        """.strip()
    
    def montar_prompt(self, user_id: int, mensagem: str) -> str:
        try:
            aluno = self.aluno_repo.buscar_por_id(user_id)
            if not aluno:
                return "Aluno não encontrado."

            treinos = self.aluno_repo.buscar_treinos_atribuidos_ao_aluno(user_id)

            lista_treinos = []
            for treino in treinos:
                descricao = treino.descricao or "Sem descrição"
                data_entraga = treino.data_entrega or "Data não informada"
                lista_treinos.append(f"- {descricao} (manter treino até {data_entraga})")

            prompt = (
                f"Aluno: {aluno.nome} (email: {aluno.email})\n"
                f"Treinos atuais:\n"
                + ("\n".join(lista_treinos) if lista_treinos else "Nenhum treino cadastrado.") +
                f"\n\nPergunta do aluno: {mensagem}\n"
            )
            return prompt
        except Exception as e:
            return f"Ocorreu um erro ao montar o prompt: {str(e)}"