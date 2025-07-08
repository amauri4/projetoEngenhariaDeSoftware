from abc import ABC, abstractmethod

class PromptStrategy(ABC):
    @abstractmethod
    def montar_prompt(self, user_id: int, mensagem: str) -> str:
        pass

    @abstractmethod
    def criar_contexto_chat(self) -> str:
        pass