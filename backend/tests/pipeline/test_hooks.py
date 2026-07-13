import unittest

from tests.helpers import build_context

from app.services.research.pipeline.base_hook import (
    BasePipelineHook,
)

from app.services.research.pipeline.base_stage import (
    BaseStage,
)

from app.services.research.pipeline.executor import (
    PipelineExecutor,
)

from app.services.research.pipeline.hooks import (
    PipelineAction,
)

from app.services.research.pipeline.stage_result import (
    StageResult,
)


class RecordingStage(BaseStage):

    def __init__(
        self,
        name,
        trace,
    ):
        self.name = name
        self.trace = trace

    def execute(
        self,
        context,
    ):

        self.trace.append(
            f"execute:{self.name}"
        )

        return StageResult(
            success=True,
        )


class RecordingHook(
    BasePipelineHook,
):

    def __init__(
        self,
        trace,
    ):
        self.trace = trace

    def before_pipeline(
        self,
        context,
    ):

        self.trace.append(
            "before_pipeline"
        )

        return PipelineAction.CONTINUE

    def before_stage(
        self,
        stage,
        context,
    ):

        self.trace.append(
            f"before_stage:{stage.name}"
        )

        return PipelineAction.CONTINUE

    def after_stage(
        self,
        stage,
        context,
        result,
    ):

        self.trace.append(
            f"after_stage:{stage.name}"
        )

        return PipelineAction.CONTINUE

    def after_pipeline(
        self,
        context,
    ):

        self.trace.append(
            "after_pipeline"
        )

        return PipelineAction.CONTINUE


class StopBeforePipelineHook(
    RecordingHook,
):

    def before_pipeline(
        self,
        context,
    ):

        self.trace.append(
            "before_pipeline"
        )

        return PipelineAction.STOP


class SkipStageHook(
    RecordingHook,
):

    def before_stage(
        self,
        stage,
        context,
    ):

        self.trace.append(
            f"before_stage:{stage.name}"
        )

        return PipelineAction.SKIP


class StopAfterStageHook(
    RecordingHook,
):

    def after_stage(
        self,
        stage,
        context,
        result,
    ):

        self.trace.append(
            f"after_stage:{stage.name}"
        )

        return PipelineAction.STOP


class HookLifecycleTests(
    unittest.TestCase,
):

    def test_hook_lifecycle_order(
        self,
    ):

        trace = []

        context = build_context()

        (
            PipelineExecutor(context)
            .add_hook(
                RecordingHook(trace)
            )
            .add(
                RecordingStage(
                    "A",
                    trace,
                )
            )
            .add(
                RecordingStage(
                    "B",
                    trace,
                )
            )
            .run()
        )

        self.assertEqual(

            trace,

            [

                "before_pipeline",

                "before_stage:A",

                "execute:A",

                "after_stage:A",

                "before_stage:B",

                "execute:B",

                "after_stage:B",

                "after_pipeline",

            ],

        )

    def test_before_pipeline_stop_skips_all_stages(
        self,
    ):

        trace = []

        context = build_context()

        (
            PipelineExecutor(context)
            .add_hook(
                StopBeforePipelineHook(
                    trace
                )
            )
            .add(
                RecordingStage(
                    "A",
                    trace,
                )
            )
            .run()
        )

        self.assertEqual(

            trace,

            [

                "before_pipeline",

                "after_pipeline",

            ],

        )

    def test_before_stage_skip_skips_stage_execution(
        self,
    ):

        trace = []

        context = build_context()

        (
            PipelineExecutor(context)
            .add_hook(
                SkipStageHook(
                    trace
                )
            )
            .add(
                RecordingStage(
                    "A",
                    trace,
                )
            )
            .run()
        )

        self.assertEqual(

            trace,

            [

                "before_pipeline",

                "before_stage:A",

                "after_pipeline",

            ],

        )

    def test_after_stage_stop_stops_pipeline(
        self,
    ):

        trace = []

        context = build_context()

        (
            PipelineExecutor(context)
            .add_hook(
                StopAfterStageHook(
                    trace
                )
            )
            .add(
                RecordingStage(
                    "A",
                    trace,
                )
            )
            .add(
                RecordingStage(
                    "B",
                    trace,
                )
            )
            .run()
        )

        self.assertEqual(

            trace,

            [

                "before_pipeline",

                "before_stage:A",

                "execute:A",

                "after_stage:A",

                "after_pipeline",

            ],

        )


if __name__ == "__main__":
    unittest.main()