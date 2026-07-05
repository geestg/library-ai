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

        self.stages.append(stage)

        return self

    def execute(self):

        for stage in self.stages:

            self.context = stage.run(

                self.context

            )

        return self.context