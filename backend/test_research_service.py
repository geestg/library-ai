import json
import unittest

from unittest.mock import Mock
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

from app.services.research.models.research_context import (
    ResearchContext,
)

from app.services.research.pipeline.base_stage import (
    BaseStage,
)

from app.services.research.pipeline.executor import (
    PipelineExecutor,
)

from app.services.research.pipeline.stage_result import (
    StageResult,
)

from app.services.research.pipeline.stages.comparison_stage import (
    ComparisonStage,
)

from app.services.research.pipeline.stages.document_stage import (
    DocumentStage,
)

from app.services.research.pipeline.stages.literature_stage import (
    LiteratureStage,
)

from app.services.research.pipeline.stages.response_stage import (
    ResponseStage,
)

from app.services.research.pipeline.stages.thesis_idea_stage import (
    ThesisIdeaStage,
)

from app.services.research.session.session_manager import (
    SessionManager,
)

from app.services.research.session import (
    session_manager,
)

from app.services.research.session.models import (
    ExecutionSession,
    WorkspaceState,
)

from app.services.research.research_engine import (
    extract_assistant_content,
    persist_assistant_response,
)

# =====================================
# TEST HELPERS
# =====================================

def build_context(
    query: str = "analisis artificial intelligence",
    active_document_ids=None,
):

    return ResearchContext(

        query=query,

        session_id="test-session",

        top_k=5,

        mode="analysis",

        active_document_ids=(
            active_document_ids or []
        ),

    )


def parse_ndjson(
    content: str,
):

    return [

        json.loads(line)

        for line in content.splitlines()

        if line.strip()

    ]


# =====================================
# TEST STAGES
# =====================================

class SuccessfulStage(
    BaseStage
):

    name = "successful"

    def execute(
        self,
        context,
    ):

        context.analysis = (
            "Pipeline completed"
        )

        return StageResult(

            success=True,

            message="Successful stage completed",

        )


class FailingStage(
    BaseStage
):

    name = "failing"

    def execute(
        self,
        context,
    ):

        raise ValueError(
            "Synthetic pipeline failure"
        )


# =====================================
# ASSISTANT PERSISTENCE TESTS
# =====================================

class AssistantPersistenceTests(
    unittest.TestCase
):

    def setUp(
        self,
    ):

        self.manager = (
            SessionManager()
        )

        self.session = (
            self.manager.create(
                "assistant-persistence-session"
            )
        )

    def test_extract_assistant_content_uses_analysis_first(
        self,
    ):

        response = {

            "analysis":
                "Analysis response",

            "answer":
                "Answer response",

            "comparison":
                "Comparison response",

        }

        content = (
            extract_assistant_content(
                response
            )
        )

        self.assertEqual(

            content,

            "Analysis response",

        )

    def test_extract_assistant_content_falls_back_to_answer(
        self,
    ):

        response = {

            "analysis":
                "",

            "answer":
                "Answer response",

        }

        content = (
            extract_assistant_content(
                response
            )
        )

        self.assertEqual(

            content,

            "Answer response",

        )

    def test_extract_assistant_content_falls_back_to_comparison(
        self,
    ):

        response = {

            "comparison":
                "Comparison response",

        }

        content = (
            extract_assistant_content(
                response
            )
        )

        self.assertEqual(

            content,

            "Comparison response",

        )

    def test_persist_assistant_response_appends_message(
        self,
    ):

        persisted_content = (
            persist_assistant_response(

                session=self.session,

                response={

                    "analysis":
                        "Persisted assistant response",

                },

            )
        )

        last_message = (
            self.session.conversation.last_message()
        )

        self.assertEqual(

            persisted_content,

            "Persisted assistant response",

        )

        self.assertIsNotNone(
            last_message
        )

        self.assertEqual(
            last_message.role,
            "assistant",
        )

        self.assertEqual(

            last_message.content,

            "Persisted assistant response",

        )

        self.assertEqual(

            self.session.conversation.total_messages(),

            1,

        )

    def test_persist_assistant_response_skips_empty_content(
        self,
    ):

        persisted_content = (
            persist_assistant_response(

                session=self.session,

                response={

                    "analysis":
                        "   ",

                },

            )
        )

        self.assertEqual(
            persisted_content,
            "",
        )

        self.assertEqual(

            self.session.conversation.total_messages(),

            0,

        )

    def test_persist_assistant_response_skips_invalid_response(
        self,
    ):

        persisted_content = (
            persist_assistant_response(

                session=self.session,

                response=None,

            )
        )

        self.assertEqual(
            persisted_content,
            "",
        )

        self.assertEqual(

            self.session.conversation.total_messages(),

            0,

        )

# =====================================
# RESPONSE PIPELINE TESTS
# =====================================

class ResponsePipelineTests(
    unittest.TestCase
):

    def test_normal_flow_builds_final_response(
        self,
    ):

        context = build_context()

        context.analysis = (
            "Normal research response"
        )

        executor = (

            PipelineExecutor(context)

            .add(
                ResponseStage()
            )

        )

        result_context = executor.run()

        self.assertIs(
            result_context,
            context,
        )

        self.assertIsNotNone(
            context.response
        )

        self.assertEqual(

            context.response["analysis"],

            "Normal research response",

        )

        self.assertIn(
            "response",
            context.stage_results,
        )

        self.assertTrue(

            context.stage_results[
                "response"
            ].success

        )

    def test_response_stage_preserves_existing_response(
        self,
    ):

        context = build_context()

        existing_response = {

            "mode":
                "comparison",

            "analysis":
                "Existing specialized response",

        }

        context.response = (
            existing_response
        )

        executor = (

            PipelineExecutor(context)

            .add(
                ResponseStage()
            )

        )

        executor.run()

        self.assertIs(

            context.response,

            existing_response,

        )


# =====================================
# SPECIALIZED STAGE TESTS
# =====================================

class SpecializedStageTests(
    unittest.TestCase
):

    @patch(
        "app.services.research.pipeline.stages."
        "comparison_stage.run_comparison_pipeline"
    )
    def test_comparison_stops_pipeline_with_response(
        self,
        mock_pipeline,
    ):

        expected_response = {

            "mode":
                "comparison",

            "analysis":
                "Comparison result",

        }

        mock_pipeline.return_value = (
            expected_response
        )

        context = build_context(
            "bandingkan metode A dan B"
        )

        executor = (

            PipelineExecutor(context)

            .add(
                ComparisonStage()
            )

            .add(
                SuccessfulStage()
            )

        )

        executor.run()

        self.assertEqual(

            context.response,

            expected_response,

        )

        self.assertTrue(

            context.stage_results[
                "comparison"
            ].stop_pipeline

        )

        self.assertNotIn(
            "successful",
            context.stage_results,
        )

    @patch(
        "app.services.research.pipeline.stages."
        "literature_stage."
        "run_literature_review_pipeline"
    )
    def test_literature_review_stops_pipeline_with_response(
        self,
        mock_pipeline,
    ):

        expected_response = {

            "mode":
                "literature_review",

            "analysis":
                "Literature review result",

        }

        mock_pipeline.return_value = (
            expected_response
        )

        context = build_context(
            "buat literature review AI"
        )

        executor = (

            PipelineExecutor(context)

            .add(
                LiteratureStage()
            )

            .add(
                SuccessfulStage()
            )

        )

        executor.run()

        self.assertEqual(

            context.response,

            expected_response,

        )

        self.assertTrue(

            context.stage_results[
                "literature"
            ].stop_pipeline

        )

        self.assertNotIn(
            "successful",
            context.stage_results,
        )

    @patch(
        "app.services.research.pipeline.stages."
        "thesis_idea_stage."
        "run_thesis_idea_pipeline"
    )
    def test_thesis_idea_stops_pipeline_with_response(
        self,
        mock_pipeline,
    ):

        expected_response = {

            "mode":
                "thesis_ideas",

            "analysis":
                "Thesis idea result",

        }

        mock_pipeline.return_value = (
            expected_response
        )

        context = build_context(
            "berikan ide skripsi AI"
        )

        executor = (

            PipelineExecutor(context)

            .add(
                ThesisIdeaStage()
            )

            .add(
                SuccessfulStage()
            )

        )

        executor.run()

        self.assertEqual(

            context.response,

            expected_response,

        )

        self.assertTrue(

            context.stage_results[
                "thesis_idea"
            ].stop_pipeline

        )

        self.assertNotIn(
            "successful",
            context.stage_results,
        )


# =====================================
# DOCUMENT STAGE TESTS
# =====================================

class DocumentStageTests(
    unittest.TestCase
):

    @patch(
        "app.services.research.pipeline.stages."
        "document_stage.run_document_analysis"
    )
    def test_document_stage_uses_supported_engine_signature(
        self,
        mock_analysis,
    ):

        mock_analysis.return_value = {

            "mode":
                "multi_document",

            "analysis":
                "Document analysis result",

            "documents": [

                {

                    "document_id":
                        "document-1",

                    "filename":
                        "proposal.pdf",

                }

            ],

        }

        context = build_context(

            query="ringkas dokumen",

            active_document_ids=[
                "document-1",
            ],

        )

        executor = (

            PipelineExecutor(context)

            .add(
                DocumentStage()
            )

        )

        executor.run()

        mock_analysis.assert_called_once_with(

            query="ringkas dokumen",

            active_document_ids=[
                "document-1",
            ],

        )

        self.assertEqual(

            context.response["mode"],

            "multi_document",

        )

        self.assertTrue(

            context.stage_results[
                "document"
            ].stop_pipeline

        )


# =====================================
# PIPELINE FAILURE TESTS
# =====================================

class PipelineFailureTests(
    unittest.TestCase
):

    def test_stage_exception_is_recorded_and_reraised(
        self,
    ):

        context = build_context()

        executor = (

            PipelineExecutor(context)

            .add(
                FailingStage()
            )

        )

        with self.assertRaisesRegex(

            ValueError,

            "Synthetic pipeline failure",

        ):

            executor.run()

        self.assertIn(
            "failing",
            context.stage_results,
        )

        failure = (
            context.stage_results[
                "failing"
            ]
        )

        self.assertFalse(
            failure.success
        )

        self.assertTrue(
            failure.stop_pipeline
        )

        self.assertEqual(

            failure.message,

            "Synthetic pipeline failure",

        )

        self.assertEqual(

            failure.metadata[
                "exception_type"
            ],

            "ValueError",

        )


# =====================================
# STREAMING TESTS
# =====================================

class StreamingRouteTests(
    unittest.TestCase
):

    @classmethod
    def setUpClass(
        cls,
    ):

        cls.client = TestClient(
            app
        )

    @patch(
        "app.api.routes.routes_chat_stream."
        "research_analysis"
    )
    def test_specialized_response_streams_without_llm_stream(
        self,
        mock_research_analysis,
    ):

        context = build_context(
            "buat literature review AI"
        )

        context.provider = "test-provider"

        context.model = "test-model"

        context.intent = (
            "literature_review"
        )

        context.response = {

            "query":
                context.query,

            "mode":
                "literature_review",

            "analysis":
                "Specialized analysis",

            "citations":
                [],

            "evidence":
                {},

            "evidence_matrix":
                {},

        }

        mock_research_analysis.return_value = (

            context,

            None,

        )

        response = self.client.post(

            "/chat-stream",

            json={

                "session_id":
                    "test-session",

                "message":
                    context.query,

                "active_document_ids":
                    [],

            },

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        events = parse_ndjson(
            response.text
        )

        event_types = [

            event["type"]

            for event in events

        ]

        self.assertEqual(

            event_types,

            [

                "start",

                "metadata",

                "context",

                "token",

                "context_final",

                "end",

            ],

        )

        token_event = next(

            event

            for event in events

            if event["type"] == "token"

        )

        self.assertEqual(

            token_event["data"],

            "Specialized analysis",

        )

        self.assertNotIn(
            "error",
            event_types,
        )

    @patch(
        "app.api.routes.routes_chat_stream."
        "research_analysis"
    )
    def test_specialized_response_persists_assistant_message(
        self,
        mock_research_analysis,
    ):

        session = session_manager.create(
            "specialized-stream-session"
        )

        context = build_context(
            "buat literature review AI"
        )

        context.session_id = (
            session.session_id
        )

        context.provider = (
            "test-provider"
        )

        context.model = (
            "test-model"
        )

        context.intent = (
            "literature_review"
        )

        context.response = {

            "mode":
                "literature_review",

            "analysis":
                "Persisted specialized response",

        }

        mock_research_analysis.return_value = (

            context,

            None,

        )

        response = self.client.post(

            "/chat-stream",

            json={

                "session_id":
                    session.session_id,

                "message":
                    context.query,

                "active_document_ids":
                    [],

            },

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        last_message = (
            session.conversation.last_message()
        )

        self.assertIsNotNone(
            last_message
        )

        self.assertEqual(
            last_message.role,
            "assistant",
        )

        self.assertEqual(

            last_message.content,

            "Persisted specialized response",

        )

        session_manager.delete(
            session.session_id
        )

    @patch(
        "app.api.routes.routes_chat_stream."
        "research_analysis"
    )
    def test_normal_stream_persists_complete_assistant_message(
        self,
        mock_research_analysis,
    ):

        session = session_manager.create(
            "normal-stream-session"
        )

        context = build_context(
            "analisis artificial intelligence"
        )

        context.session_id = (
            session.session_id
        )

        context.provider = (
            "test-provider"
        )

        context.model = (
            "test-model"
        )

        context.intent = (
            "research"
        )

        context.response = None

        llm_stream = iter([

            "Bagian pertama. ",

            "Bagian kedua.",

        ])

        mock_research_analysis.return_value = (

            context,

            llm_stream,

        )

        response = self.client.post(

            "/chat-stream",

            json={

                "session_id":
                    session.session_id,

                "message":
                    context.query,

                "active_document_ids":
                    [],

            },

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        last_message = (
            session.conversation.last_message()
        )

        self.assertIsNotNone(
            last_message
        )

        self.assertEqual(
            last_message.role,
            "assistant",
        )

        self.assertEqual(

            last_message.content,

            (
                "Bagian pertama. "
                "Bagian kedua."
            ),

        )

        session_manager.delete(
            session.session_id
        )

    @patch(
        "app.api.routes.routes_chat_stream."
        "research_analysis"
    )
    def test_pipeline_failure_returns_error_event(
        self,
        mock_research_analysis,
    ):

        mock_research_analysis.side_effect = (
            RuntimeError(
                "Synthetic stream failure"
            )
        )

        response = self.client.post(

            "/chat-stream",

            json={

                "session_id":
                    "test-session",

                "message":
                    "trigger failure",

                "active_document_ids":
                    [],

            },

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        events = parse_ndjson(
            response.text
        )

        self.assertEqual(

            events[0]["type"],

            "start",

        )

        self.assertEqual(

            events[-1]["type"],

            "error",

        )

        self.assertEqual(

            events[-1]["data"][
                "status"
            ],

            "failed",

        )

        self.assertEqual(

            events[-1]["data"][
                "message"
            ],

            "Synthetic stream failure",

        )

        self.assertEqual(

            events[-1]["data"][
                "exception_type"
            ],

            "RuntimeError",

        )


# =====================================
# SESSION MODEL TESTS
# =====================================

class SessionModelTests(
    unittest.TestCase
):

    def test_workspace_state_clear_resets_all_state(
        self,
    ):

        workspace = WorkspaceState(

            selected_citation={
                "source_id": 1,
            },

            selected_thesis={
                "title": "Test Thesis",
            },

            last_search=(
                "artificial intelligence"
            ),

            filters={
                "year": 2026,
            },

            ui_state={
                "drawer_open": True,
            },

        )

        workspace.clear()

        self.assertIsNone(
            workspace.selected_citation
        )

        self.assertIsNone(
            workspace.selected_thesis
        )

        self.assertEqual(
            workspace.last_search,
            "",
        )

        self.assertEqual(
            workspace.filters,
            {},
        )

        self.assertEqual(
            workspace.ui_state,
            {},
        )

    def test_execution_session_clear_resets_contract(
        self,
    ):

        execution = ExecutionSession(

            last_query="test query",

            mode="analysis",

            provider="test-provider",

            model="test-model",

            intent="test-intent",

            response="test response",

            serialized_context={
                "query": "test query",
            },

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
            execution.updated_at
        )


# =====================================
# SESSION MANAGER TESTS
# =====================================

class SessionManagerTests(
    unittest.TestCase
):

    def setUp(
        self,
    ):

        self.manager = (
            SessionManager()
        )

    def test_create_builds_complete_workspace_session(
        self,
    ):

        session = self.manager.create(
            "session-1"
        )

        self.assertEqual(
            session.session_id,
            "session-1",
        )

        self.assertEqual(
            session.conversation.total_messages(),
            0,
        )

        self.assertEqual(
            session.documents.count(),
            0,
        )

        self.assertEqual(
            session.execution.last_query,
            "",
        )

        self.assertEqual(
            self.manager.count(),
            1,
        )

    def test_get_or_create_returns_existing_session(
        self,
    ):

        first_session = (
            self.manager.get_or_create(
                "session-1"
            )
        )

        first_session.conversation.append(

            role="user",

            content="jelaskan AI",

        )

        second_session = (
            self.manager.get_or_create(
                "session-1"
            )
        )

        self.assertIs(
            first_session,
            second_session,
        )

        self.assertEqual(
            second_session.conversation.total_messages(),
            1,
        )

    def test_create_without_id_generates_session_id(
        self,
    ):

        session = self.manager.create()

        self.assertTrue(
            session.session_id
        )

        self.assertTrue(

            self.manager.exists(
                session.session_id
            )

        )

    def test_reset_preserves_session_identity(
        self,
    ):

        session = self.manager.create(
            "session-1"
        )

        session.conversation.append(

            role="user",

            content="jelaskan AI",

        )

        session.workspace.last_search = (
            "artificial intelligence"
        )

        session.execution.last_query = (
            "jelaskan AI"
        )

        reset_result = self.manager.reset(
            "session-1"
        )

        restored_session = self.manager.get(
            "session-1"
        )

        self.assertTrue(
            reset_result
        )

        self.assertIs(
            restored_session,
            session,
        )

        self.assertEqual(
            session.conversation.total_messages(),
            0,
        )

        self.assertEqual(
            session.workspace.last_search,
            "",
        )

        self.assertEqual(
            session.execution.last_query,
            "",
        )

    def test_delete_removes_session(
        self,
    ):

        self.manager.create(
            "session-1"
        )

        deleted = self.manager.delete(
            "session-1"
        )

        self.assertTrue(
            deleted
        )

        self.assertFalse(
            self.manager.exists(
                "session-1"
            )
        )

        self.assertEqual(
            self.manager.count(),
            0,
        )

# =====================================
# ENTRYPOINT
# =====================================

if __name__ == "__main__":

    unittest.main(
        verbosity=2
    )