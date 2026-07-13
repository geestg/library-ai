import unittest

from unittest.mock import MagicMock

from app.services.research.research_engine import (
    persist_execution_snapshot,
)

from app.services.research.session.session_manager import (
    SessionManager,
)

from tests.helpers import (
    build_context,
)


class ExecutionSnapshotTests(
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

        self.session = (
            self.manager.create(
                "execution-session"
            )
        )

    # =====================================
    # explicit response
    # =====================================

    def test_snapshot_updates_execution_session(
        self,
    ):

        context = build_context()

        context.provider = "openai"

        context.model = "gpt"

        context.intent = "analysis"

        context.analysis = (
            "Generated Analysis"
        )

        snapshot = (
            persist_execution_snapshot(

                session=self.session,

                context=context,

                response_content=(
                    "Assistant Response"
                ),

            )
        )

        execution = (
            self.session.execution
        )

        self.assertEqual(

            execution.last_query,

            context.query,

        )

        self.assertEqual(

            execution.mode,

            context.mode,

        )

        self.assertEqual(

            execution.provider,

            "openai",

        )

        self.assertEqual(

            execution.model,

            "gpt",

        )

        self.assertEqual(

            execution.intent,

            "analysis",

        )

        self.assertEqual(

            execution.response,

            "Assistant Response",

        )

        self.assertIs(

            execution.serialized_context,

            snapshot,

        )

        self.assertEqual(

            snapshot["query"],

            context.query,

        )

        self.assertEqual(

            snapshot["analysis"],

            context.analysis,

        )

        self.assertIsNotNone(

            execution.updated_at,

        )

    # =====================================
    # analysis fallback
    # =====================================

    def test_snapshot_uses_analysis_when_response_missing(
        self,
    ):

        context = build_context()

        context.analysis = (
            "Fallback Analysis"
        )

        snapshot = (
            persist_execution_snapshot(

                session=self.session,

                context=context,

            )
        )

        execution = (
            self.session.execution
        )

        self.assertEqual(

            execution.response,

            "Fallback Analysis",

        )

        self.assertIs(

            execution.serialized_context,

            snapshot,

        )

    # =====================================
    # blank response
    # =====================================

    def test_snapshot_ignores_blank_response(
        self,
    ):

        context = build_context()

        context.analysis = (
            "Analysis Result"
        )

        persist_execution_snapshot(

            session=self.session,

            context=context,

            response_content="     ",

        )

        self.assertEqual(

            self.session.execution.response,

            "Analysis Result",

        )


if __name__ == "__main__":

    unittest.main()