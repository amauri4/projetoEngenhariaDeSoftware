from abc import ABC, abstractmethod

class IStrategyPrompt(ABC):
    @abstractmethod
    def montar_prompt(self, user_id: int, mensagem: str) -> str:
        pass