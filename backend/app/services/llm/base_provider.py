from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):

    @abstractmethod
    def generate(
        self,
        model: str,
        prompt: str,
        image_ref: str = None
    ):
        pass

    @abstractmethod
    def stream(
        self,
        model: str,
        prompt: str,
        image_ref: str = None
    ):
        pass