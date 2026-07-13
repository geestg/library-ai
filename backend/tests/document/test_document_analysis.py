import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from app.services.research.engines.document_engine import (
    ANSWERABLE,
    NOT_FOUND,
    run_document_analysis,
)


class DocumentAnalysisTests(
    unittest.TestCase,
):

    def setUp(
        self,
    ):

        self.document_result = {

            "documents": [

                {
                    "document_id": "doc-1",
                    "filename": "paper.pdf",
                }

            ],

            "chunks": [

                {
                    "document_id": "doc-1",
                    "page": 1,
                    "chunk_index": 0,
                    "score": 0.98,
                    "text": "Artificial Intelligence",
                }

            ],

            "context": "Context",

        }

        self.answerable_result = {

            "status": ANSWERABLE,

            "answerable_chunks": (
                self.document_result["chunks"]
            ),

            "verification_mode": "per_chunk",

        }

    @patch(
        "app.services.research.engines.document_engine.emit_progress"
    )
    @patch(
        "app.services.research.engines.document_engine.build_document_context"
    )
    def test_returns_none_when_no_chunks(
        self,
        mock_context,
        mock_progress,
    ):

        mock_context.return_value = {

            "documents": [],

            "chunks": [],

            "context": "",

        }

        result = run_document_analysis(

            query="AI",

            session_id="session",

            active_document_ids=[],

        )

        self.assertIsNone(
            result
        )

    @patch(
        "app.services.research.engines.document_engine.emit_progress"
    )
    @patch(
        "app.services.research.engines.document_engine.verify_answerability"
    )
    @patch(
        "app.services.research.engines.document_engine.build_document_context"
    )
    def test_returns_not_found_response(
        self,
        mock_context,
        mock_verify,
        mock_progress,
    ):

        mock_context.return_value = (
            self.document_result
        )

        mock_verify.return_value = {

            "status": NOT_FOUND,

            "answerable_chunks": [],

            "verification_mode": "none",

        }

        result = run_document_analysis(

            query="AI",

            session_id="session",

            active_document_ids=[],

        )

        self.assertEqual(

            result["answerability"],

            NOT_FOUND,

        )

    @patch(
        "app.services.research.engines.document_engine.emit_progress"
    )
    @patch(
        "app.services.research.engines.document_engine.LLMTask.execute"
    )
    @patch(
        "app.services.research.engines.document_engine.build_document_prompt"
    )
    @patch(
        "app.services.research.engines.document_engine.build_context_from_chunks"
    )
    @patch(
        "app.services.research.engines.document_engine.verify_answerability"
    )
    @patch(
        "app.services.research.engines.document_engine.build_document_context"
    )
    def test_normal_analysis_returns_answer(
        self,
        mock_context,
        mock_verify,
        mock_chunk_context,
        mock_prompt,
        mock_execute,
        mock_progress,
    ):

        mock_context.return_value = (
            self.document_result
        )

        mock_verify.return_value = (
            self.answerable_result
        )

        mock_chunk_context.return_value = (
            "Verified Context"
        )

        mock_prompt.return_value = (
            "Prompt"
        )

        mock_execute.return_value = (
            "Generated Answer"
        )

        result = run_document_analysis(

            query="AI",

            session_id="session",

            active_document_ids=[],

        )

        self.assertEqual(

            result["analysis"],

            "Generated Answer",

        )

        self.assertEqual(

            result["answerability"],

            ANSWERABLE,

        )

        self.assertEqual(

            result["verification_mode"],

            "per_chunk",

        )

    @patch(
        "app.services.research.engines.document_engine.emit_progress"
    )
    @patch(
        "app.services.research.engines.document_engine.LLMTask.stream"
    )
    @patch(
        "app.services.research.engines.document_engine.build_document_prompt"
    )
    @patch(
        "app.services.research.engines.document_engine.build_context_from_chunks"
    )
    @patch(
        "app.services.research.engines.document_engine.verify_answerability"
    )
    @patch(
        "app.services.research.engines.document_engine.build_document_context"
    )
    def test_stream_mode_returns_stream(
        self,
        mock_context,
        mock_verify,
        mock_chunk_context,
        mock_prompt,
        mock_stream,
        mock_progress,
    ):

        stream = MagicMock()

        mock_context.return_value = (
            self.document_result
        )

        mock_verify.return_value = (
            self.answerable_result
        )

        mock_chunk_context.return_value = (
            "Verified Context"
        )

        mock_prompt.return_value = (
            "Prompt"
        )

        mock_stream.return_value = stream

        result = run_document_analysis(

            query="AI",

            session_id="session",

            active_document_ids=[],

            stream=True,

        )

        self.assertEqual(

            result["response_type"],

            "stream",

        )

        self.assertIs(

            result["llm_stream"],

            stream,

        )

    @patch(
        "app.services.research.engines.document_engine.emit_progress"
    )
    @patch(
        "app.services.research.engines.document_engine.LLMTask.execute"
    )
    @patch(
        "app.services.research.engines.document_engine.build_document_prompt"
    )
    @patch(
        "app.services.research.engines.document_engine.build_context_from_chunks"
    )
    @patch(
        "app.services.research.engines.document_engine.verify_answerability"
    )
    @patch(
        "app.services.research.engines.document_engine.build_document_context"
    )
    def test_progress_events_are_emitted(
        self,
        mock_context,
        mock_verify,
        mock_chunk_context,
        mock_prompt,
        mock_execute,
        mock_progress,
    ):

        mock_context.return_value = (
            self.document_result
        )

        mock_verify.return_value = (
            self.answerable_result
        )

        mock_chunk_context.return_value = (
            "Verified Context"
        )

        mock_prompt.return_value = (
            "Prompt"
        )

        mock_execute.return_value = (
            "Answer"
        )

        run_document_analysis(

            query="AI",

            session_id="session",

            active_document_ids=[],

        )

        self.assertGreaterEqual(

            mock_progress.call_count,

            4,

        )