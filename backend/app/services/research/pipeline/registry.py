class StageRegistry:

    def __init__(self):

        self._stages = {}

    # =============================

    def register(

        self,

        stage,

    ):

        self._stages[
            stage.name
        ] = stage

    # =============================

    def get(

        self,

        name,

    ):

        return self._stages.get(name)

    # =============================

    def all(self):

        return list(

            self._stages.values()

        )


registry = StageRegistry()