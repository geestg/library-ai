from app.services.research.pipeline.hooks import (
    PipelineAction,
)


class BasePipelineHook:

    """
    Base hook untuk seluruh lifecycle pipeline.
    """

    def before_pipeline(
        self,
        context,
    ):
        return PipelineAction.CONTINUE

    def after_pipeline(
        self,
        context,
    ):
        return PipelineAction.CONTINUE

    def before_stage(
        self,
        stage,
        context,
    ):
        return PipelineAction.CONTINUE

    def after_stage(
        self,
        stage,
        context,
        result,
    ):
        return PipelineAction.CONTINUE