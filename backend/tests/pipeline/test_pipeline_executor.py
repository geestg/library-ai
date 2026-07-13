import unittest

from tests.helpers import build_context

from app.services.research.pipeline.executor import (
    PipelineExecutor,
)

from app.services.research.pipeline.base_stage import (
    BaseStage,
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
            self.name
        )

        return StageResult(

            success=True,

            message=self.name,

        )


class StopStage(BaseStage):

    name = "stop"

    def __init__(
        self,
        trace,
    ):
        self.trace = trace

    def execute(
        self,
        context,
    ):

        self.trace.append(
            "STOP"
        )

        return StageResult(

            success=True,

            stop_pipeline=True,

            message="stop",

        )


class SkipRemainingStage(BaseStage):

    name = "skip"

    def __init__(
        self,
        trace,
    ):
        self.trace = trace

    def execute(
        self,
        context,
    ):

        self.trace.append(
            "SKIP"
        )

        return StageResult(

            success=True,

            skip_remaining=True,

            message="skip",

        )


class ExplodingStage(BaseStage):

    name = "explode"

    def execute(
        self,
        context,
    ):

        raise RuntimeError(
            "boom"
        )


class PipelineExecutorBasicTests(
    unittest.TestCase,
):

    def test_executor_returns_same_context(
        self,
    ):

        context = build_context()

        executor = (
            PipelineExecutor(
                context
            )
        )

        result = executor.run()

        self.assertIs(

            result,

            context,

        )

    def test_empty_pipeline_is_valid(
        self,
    ):

        context = build_context()

        executor = (
            PipelineExecutor(
                context
            )
        )

        result = executor.run()

        self.assertEqual(

            result.stage_results,

            {},

        )

    def test_pipeline_executes_stages_in_order(
        self,
    ):

        trace = []

        context = build_context()

        executor = (

            PipelineExecutor(context)

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

            .add(
                RecordingStage(
                    "C",
                    trace,
                )
            )

        )

        executor.run()

        self.assertEqual(

            trace,

            [

                "A",

                "B",

                "C",

            ],

        )

    def test_stage_results_are_saved(
        self,
    ):

        context = build_context()

        executor = (

            PipelineExecutor(context)

            .add(
                RecordingStage(
                    "analysis",
                    [],
                )
            )

        )

        executor.run()

        self.assertIn(

            "analysis",

            context.stage_results,

        )

        result = (
            context.stage_results[
                "analysis"
            ]
        )

        self.assertTrue(
            result.success,
        )

        self.assertEqual(

            result.message,

            "analysis",

        )

    def test_stop_pipeline_prevents_next_stage(
        self,
    ):

        trace = []

        context = build_context()

        executor = (

            PipelineExecutor(context)

            .add(
                RecordingStage(
                    "A",
                    trace,
                )
            )

            .add(
                StopStage(
                    trace,
                )
            )

            .add(
                RecordingStage(
                    "C",
                    trace,
                )
            )

        )

        executor.run()

        self.assertEqual(

            trace,

            [

                "A",

                "STOP",

            ],

        )

    def test_skip_remaining_stops_pipeline(
        self,
    ):

        trace = []

        context = build_context()

        executor = (

            PipelineExecutor(context)

            .add(
                RecordingStage(
                    "A",
                    trace,
                )
            )

            .add(
                SkipRemainingStage(
                    trace,
                )
            )

            .add(
                RecordingStage(
                    "C",
                    trace,
                )
            )

        )

        executor.run()

        self.assertEqual(

            trace,

            [

                "A",

                "SKIP",

            ],

        )

    def test_exception_is_saved_then_reraised(
        self,
    ):

        context = build_context()

        executor = (

            PipelineExecutor(context)

            .add(
                ExplodingStage()
            )

        )

        with self.assertRaises(
            RuntimeError,
        ):

            executor.run()

        self.assertIn(

            "explode",

            context.stage_results,

        )

        result = (
            context.stage_results[
                "explode"
            ]
        )

        self.assertFalse(
            result.success,
        )

        self.assertTrue(
            result.stop_pipeline,
        )

        self.assertEqual(

            result.message,

            "boom",

        )

        self.assertEqual(

            result.metadata[
                "exception_type"
            ],

            "RuntimeError",

        )


if __name__ == "__main__":
    unittest.main()