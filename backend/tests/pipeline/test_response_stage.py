import unittest
from unittest.mock import patch

from tests.helpers import build_context

from app.services.research.pipeline.stages.response_stage import (
    ResponseStage,
)


class ResponseStageTests(
    unittest.TestCase,
):

    @patch(
        "app.services.research.pipeline.stages.response_stage.build_research_response"
    )
    def test_builds_response_when_none(
        self,
        mock_builder,
    ):

        context = build_context()

        context.response = None

        mock_builder.return_value = {

            "analysis": "Generated response",

        }

        result = (
            ResponseStage().run(
                context
            )
        )

        self.assertTrue(
            result.success,
        )

        self.assertEqual(

            result.message,

            "Response built",

        )

        self.assertEqual(

            result.metadata[
                "response_source"
            ],

            "research",

        )

        self.assertEqual(

            context.response,

            {

                "analysis":
                    "Generated response",

            },

        )

        mock_builder.assert_called_once_with(
            context
        )

    @patch(
        "app.services.research.pipeline.stages.response_stage.build_research_response"
    )
    def test_existing_response_is_preserved(
        self,
        mock_builder,
    ):

        context = build_context()

        context.response = {

            "analysis":
                "Existing response",

        }

        result = (
            ResponseStage().run(
                context
            )
        )

        self.assertTrue(
            result.success,
        )

        self.assertEqual(

            result.message,

            "Existing response preserved",

        )

        self.assertEqual(

            result.metadata[
                "response_source"
            ],

            "specialized",

        )

        self.assertEqual(

            context.response,

            {

                "analysis":
                    "Existing response",

            },

        )

        mock_builder.assert_not_called()

    @patch(
        "app.services.research.pipeline.stages.response_stage.build_research_response"
    )
    def test_stream_response_is_deferred(
        self,
        mock_builder,
    ):

        context = build_context()

        context.response = None

        context.llm_stream = object()

        result = (
            ResponseStage().run(
                context
            )
        )

        self.assertTrue(
            result.success,
        )

        self.assertEqual(

            result.message,

            "Response deferred to stream consumer",

        )

        self.assertEqual(

            result.metadata[
                "response_source"
            ],

            "stream",

        )

        self.assertIsNone(
            context.response,
        )

        mock_builder.assert_not_called()

    @patch(
        "app.services.research.pipeline.stages.response_stage.build_research_response"
    )
    def test_stage_is_idempotent(
        self,
        mock_builder,
    ):

        context = build_context()

        context.response = None

        mock_builder.return_value = {

            "analysis":
                "Generated",

        }

        stage = ResponseStage()

        stage.run(
            context
        )

        stage.run(
            context
        )

        self.assertEqual(

            mock_builder.call_count,

            1,

        )

    @patch(
        "app.services.research.pipeline.stages.response_stage.build_research_response"
    )
    def test_stage_does_not_modify_provider_model_or_intent(
        self,
        mock_builder,
    ):

        context = build_context()

        context.provider = "provider"

        context.model = "model"

        context.intent = "intent"

        mock_builder.return_value = {

            "analysis":
                "Generated",

        }

        ResponseStage().run(
            context
        )

        self.assertEqual(
            context.provider,
            "provider",
        )

        self.assertEqual(
            context.model,
            "model",
        )

        self.assertEqual(
            context.intent,
            "intent",
        )


if __name__ == "__main__":
    unittest.main()