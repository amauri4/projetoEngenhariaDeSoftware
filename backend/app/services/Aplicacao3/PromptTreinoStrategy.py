from app.services.Framework.IStrategyPrompt import IStrategyPrompt
from app.repositories.Aplicacao3.AlunoRepository import AlunoRepository
from app.repositories.Aplicacao3.TreinoRepository import TreinoRepository
from app.database import session

class PromptTreinoStrategy(IStrategyPrompt):

    def __init__(self, db: session):
        self.db = db
        self.aluno_repo = AlunoRepository(db)
        self.contexto = """
        Você é um assistente virtual especializado em treinos de academia. 
        Seu papel é ajudar alunos a executarem corretamente os exercícios, oferecendo dicas práticas, cuidados importantes durante a execução, e, 
        se solicitado, sugerindo exercícios equivalentes ou alternativos para o mesmo grupo muscular.

        ### Regras principais:
        - Foque em segurança e execução correta dos exercícios.
        - Ofereça dicas claras e objetivas para melhorar a técnica.
        - Avise sobre cuidados para evitar lesões.
        - Sugira exercícios alternativos ou equivalentes se o aluno pedir.
        - Use linguagem acessível para alunos de todos os níveis.
        - Sempre responda de forma direta, sem rodeios.

        ### Limitações:
        - Não forneça diagnósticos médicos ou planos de tratamento.
        - Não substitua orientação presencial de um profissional qualificado.
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