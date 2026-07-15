from delbot_platform.ai.runtime.state import RuntimeState


class RuntimeManager:

    def __init__(self):

        self.services: dict[str, RuntimeState] = {}

    def register(
        self,
        state: RuntimeState,
    ):

        self.services[state.name] = state

    def get(
        self,
        name: str,
    ) -> RuntimeState:

        return self.services[name]

    def list(self):

        return list(self.services.values())