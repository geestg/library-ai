from app.services.research.pipeline.base_hook import (
    BasePipelineHook,
)

from app.services.research.pipeline.hooks import (
    PipelineAction,
)


class LoggingHook(
    BasePipelineHook
):

    def before_pipeline(
        self,
        context,
    ):

        print("=" * 60)
        print("PIPELINE START")
        print("=" * 60)

        return PipelineAction.CONTINUE

    def before_stage(
        self,
        stage,
        context,
    ):

        print(
            f">>> {stage.name}"
        )

        return PipelineAction.CONTINUE

    def after_stage(
        self,
        stage,
        context,
        result,
    ):

        print(

            f"<<< {stage.name} "

            f"({result.duration_ms:.2f} ms)"

        )

        return PipelineAction.CONTINUE

    def after_pipeline(
        self,
        context,
    ):

        print("=" * 60)
        print("PIPELINE END")
        print("=" * 60)

        return PipelineAction.CONTINUE
