from abc import ABC, abstractmethod

class PromptStrategy(ABC):
    @abstractmethod
    def montar_prompt(self, user_id: int, mensagem: str) -> str:
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        pass