class PromptFactory:

    _registry = {}

    @classmethod
    def register(

        cls,

        name: str,

        builder,

    ):

        cls._registry[name] = builder

    @classmethod
    def get(

        cls,

        name: str,

    ):

        return cls._registry[name]

    @classmethod
    def available(cls):

        return sorted(
            cls._registry.keys()
        )

