from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):

    @abstractmethod
    def generate(
        self,
        model: str,
        prompt: str
    ):
        pass

    @abstractmethod
    def stream(
        self,
        model: str,
        prompt: str
    ):
        pass