import unittest

from unittest.mock import MagicMock
from unittest.mock import patch

from app.services.research.models.research_context import (
    ResearchContext,
)

from app.services.research.research_engine import (
    research_analysis,
)

from app.services.research.session.session_manager import (
    SessionManager,
)


class ResearchAnalysisTests(
    unittest.TestCase,
):

    def setUp(
        self,
    ):

        repository = MagicMock()

        repository.get.return_value = None

        repository.save.return_value = None

        self.manager = (
            SessionManager(
                repository=repository,
            )
        )

    @patch(
        "app.services.research.research_engine.session_manager"
    )
    @patch(
        "app.services.research.research_engine.serialize_research_context"
    )
    @patch(
        "app.services.research.research_engine.ResearchPipelineBuilder.build"
    )
    @patch(
        "app.orchestration.task_router.route_query"
    )
    def test_research_analysis_updates_session_and_returns_response(
        self,
        mock_route,
        mock_build,
        mock_serializer,
        mock_session_manager,
    ):

        session = self.manager.create(
            "research-session"
        )

        mock_session_manager.get_or_create.return_value = (
            session
        )

        mock_route.return_value = {

            "intent": "analysis",

            "provider": "openai",

            "model": "gpt",

        }

        mock_serializer.return_value = {

            "serialized": True,

        }

        captured = {}

        executor = MagicMock()

        def fake_run():

            context = captured["context"]

            context.analysis = (
                "Analysis Result"
            )

            context.response = {

                "analysis":
                    "Analysis Result",

            }

        executor.run.side_effect = (
            fake_run
        )

        def fake_build(
            context,
            stream=False,
            progress_callback=None,
        ):

            captured["context"] = context

            return executor

        mock_build.side_effect = (
            fake_build
        )

        result = research_analysis(

            query="Explain AI",

            session_id="research-session",

        )

        self.assertEqual(

            result["analysis"],

            "Analysis Result",

        )

        context = captured["context"]

        self.assertEqual(

            context.query,

            "Explain AI",

        )

        self.assertEqual(

            context.intent,

            "analysis",

        )

        self.assertEqual(

            context.provider,

            "openai",

        )

        self.assertEqual(

            context.model,

            "gpt",

        )

        self.assertEqual(

            session.conversation.total_messages(),

            2,

        )

        self.assertEqual(

            session.execution.response,

            "Analysis Result",

        )

        self.assertIsInstance(

            session.execution.serialized_context,

            dict,

        )

    @patch(
        "app.services.research.research_engine.session_manager"
    )
    @patch(
        "app.services.research.research_engine.ResearchPipelineBuilder.build"
    )
    @patch(
        "app.orchestration.task_router.route_query"
    )
    def test_streaming_returns_context_and_stream(
        self,
        mock_route,
        mock_build,
        mock_session_manager,
    ):

        session = self.manager.create(
            "stream-session"
        )

        mock_session_manager.get_or_create.return_value = (
            session
        )

        mock_route.return_value = {

            "intent": "analysis",

            "provider": "mock",

            "model": "mock",

        }

        executor = MagicMock()

        def fake_run():

            context = executor.context

            context.llm_stream = iter(

                [

                    "a",

                    "b",

                ]

            )

        executor.run.side_effect = (
            fake_run
        )

        def fake_build(
            context,
            stream=False,
            progress_callback=None,
        ):

            executor.context = context

            return executor

        mock_build.side_effect = (
            fake_build
        )

        context, stream = (

            research_analysis(

                query="Streaming",

                session_id="stream-session",

                stream=True,

            )

        )

        self.assertIsInstance(

            context,

            ResearchContext,

        )

        self.assertIsNotNone(

            stream,

        )

    @patch(
        "app.services.research.research_engine.session_manager"
    )
    @patch(
        "app.services.research.research_engine.serialize_research_context"
    )
    @patch(
        "app.services.research.research_engine.ResearchPipelineBuilder.build"
    )
    @patch(
        "app.orchestration.task_router.route_query"
    )
    def test_active_document_ids_are_preserved(
        self,
        mock_route,
        mock_build,
        mock_serializer,
        mock_session_manager,
    ):

        session = self.manager.create(
            "document-session"
        )

        mock_session_manager.get_or_create.return_value = (
            session
        )

        mock_route.return_value = {}

        mock_serializer.return_value = {}

        executor = MagicMock()

        captured = {}

        def fake_run():

            context = captured["context"]

            context.response = {

                "analysis":
                    "OK",

            }

        executor.run.side_effect = (
            fake_run
        )

        def fake_build(
            context,
            stream=False,
            progress_callback=None,
        ):

            captured["context"] = context

            return executor

        mock_build.side_effect = (
            fake_build
        )

        research_analysis(

            query="Documents",

            session_id="document-session",

            active_document_ids=[

                "doc-1",

                "doc-2",

            ],

        )

        self.assertEqual(

            captured[
                "context"
            ].active_document_ids,

            [

                "doc-1",

                "doc-2",

            ],

        )


if __name__ == "__main__":

    unittest.main()