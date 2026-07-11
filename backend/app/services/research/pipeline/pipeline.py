from app.services.research.models.research_context import (
    ResearchContext,
)


class ResearchPipeline:

    def __init__(
        self,
        context: ResearchContext,
    ):

        self.context = context

        self.stages = []

    def add_stage(
        self,
        stage,
    ):

        self.stages.append(
            stage
        )

        return self
