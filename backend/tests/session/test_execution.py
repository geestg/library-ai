import unittest
from datetime import datetime

from tests.helpers import build_context

from app.services.research.session.models import (
    ExecutionSession,
)


class ExecutionSessionTests(
    unittest.TestCase,
):

    def test_default_state(
        self,
    ):

        execution = ExecutionSession()

        self.assertEqual(
            execution.last_query,
            "",
        )

        self.assertEqual(
            execution.mode,
            "",
        )

        self.assertEqual(
            execution.provider,
            "",
        )

        self.assertEqual(
            execution.model,
            "",
        )

        self.assertEqual(
            execution.intent,
            "",
        )

        self.assertEqual(
            execution.response,
            "",
        )

        self.assertEqual(
            execution.serialized_context,
            {},
        )

        self.assertIsNone(
            execution.updated_at,
        )

    def test_update_populates_all_fields(
        self,
    ):

        execution = ExecutionSession()

        context = build_context(
            "Artificial Intelligence",
        )

        context.provider = "openrouter"
        context.model = "gpt"
        context.intent = "analysis"
        context.analysis = "Generated analysis"

        snapshot = {
            "query": context.query,
        }

        execution.update(

            context=context,

            serialized_context=snapshot,

            response_content="Assistant Response",

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
            "openrouter",
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

        self.assertIsInstance(
            execution.updated_at,
            datetime,
        )

    def test_update_falls_back_to_context_analysis(
        self,
    ):

        execution = ExecutionSession()

        context = build_context()

        context.analysis = "Fallback Analysis"

        execution.update(

            context=context,

            serialized_context={},

        )

        self.assertEqual(
            execution.response,
            "Fallback Analysis",
        )

    def test_explicit_response_has_priority(
        self,
    ):

        execution = ExecutionSession()

        context = build_context()

        context.analysis = "Context Analysis"

        execution.update(

            context=context,

            serialized_context={},

            response_content="Explicit Response",

        )

        self.assertEqual(
            execution.response,
            "Explicit Response",
        )

    def test_blank_explicit_response_uses_analysis(
        self,
    ):

        execution = ExecutionSession()

        context = build_context()

        context.analysis = "Analysis"

        execution.update(

            context=context,

            serialized_context={},

            response_content="   ",

        )

        self.assertEqual(
            execution.response,
            "Analysis",
        )

    def test_clear_resets_state(
        self,
    ):

        execution = ExecutionSession()

        context = build_context()

        context.provider = "provider"
        context.model = "model"
        context.intent = "analysis"
        context.analysis = "analysis"

        execution.update(

            context=context,

            serialized_context={
                "a": 1,
            },

            response_content="answer",

        )

        execution.clear()

        self.assertEqual(
            execution.last_query,
            "",
        )

        self.assertEqual(
            execution.mode,
            "",
        )

        self.assertEqual(
            execution.provider,
            "",
        )

        self.assertEqual(
            execution.model,
            "",
        )

        self.assertEqual(
            execution.intent,
            "",
        )

        self.assertEqual(
            execution.response,
            "",
        )

        self.assertEqual(
            execution.serialized_context,
            {},
        )

        self.assertIsNone(
            execution.updated_at,
        )

    def test_to_dict_contains_all_fields(
        self,
    ):

        execution = ExecutionSession()

        context = build_context()

        context.provider = "provider"
        context.model = "model"
        context.intent = "analysis"
        context.analysis = "analysis"

        execution.update(

            context=context,

            serialized_context={
                "query": context.query,
            },

            response_content="assistant",

        )

        payload = execution.to_dict()

        self.assertEqual(
            payload["last_query"],
            context.query,
        )

        self.assertEqual(
            payload["mode"],
            context.mode,
        )

        self.assertEqual(
            payload["provider"],
            "provider",
        )

        self.assertEqual(
            payload["model"],
            "model",
        )

        self.assertEqual(
            payload["intent"],
            "analysis",
        )

        self.assertEqual(
            payload["response"],
            "assistant",
        )

        self.assertEqual(
            payload["serialized_context"],
            {
                "query": context.query,
            },
        )

        self.assertIsNotNone(
            payload["updated_at"],
        )

    def test_update_without_analysis_or_response_produces_empty_response(
        self,
    ):

        execution = ExecutionSession()

        context = build_context()

        context.analysis = ""

        execution.update(

            context=context,

            serialized_context={},

        )

        self.assertEqual(
            execution.response,
            "",
        )