from abc import ABC, abstractmethod


class BaseLLMProvider:
    def generate(

        self,

        model: str,

        prompt: str,

        temperature: float = 0,

        max_tokens: int | None = None,

    ):

        raise NotImplementedError

    def stream(

        self,

        model: str,

        prompt: str,

        temperature: float = 0,

        max_tokens: int | None = None,

    ):

        raise NotImplementedError

