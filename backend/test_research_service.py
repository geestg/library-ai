import json
import unittest

from unittest.mock import Mock
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

from app.services.research.models.research_context import (
    ResearchContext,
)

from app.services.research.prompts.analysis_prompt_builder import (
    build_conversation_section,
    build_research_prompt,
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
    persist_execution_snapshot,
    research_analysis,
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
# CONVERSATION PROMPT TESTS
# =====================================

class ConversationPromptTests(
    unittest.TestCase
):

    def test_empty_conversation_history_uses_explicit_fallback(
        self,
    ):

        context = build_context()

        section = (
            build_conversation_section(
                context
            )
        )

        self.assertEqual(

            section,

            "Belum ada percakapan sebelumnya.",

        )

    def test_existing_conversation_history_is_included_in_prompt(
        self,
    ):

        context = build_context(
            "lanjutkan analisis tersebut"
        )

        context.conversation_history = (

            "user: jelaskan artificial intelligence\n"
            "assistant: Artificial intelligence adalah "
            "bidang ilmu komputer."

        )

        prompt = (
            build_research_prompt(
                context
            )
        )

        self.assertIn(

            context.conversation_history,

            prompt,

        )

    def test_current_query_is_included_in_prompt(
        self,
    ):

        context = build_context(
            "apa research gap dari topik tersebut?"
        )

        context.conversation_history = (

            "user: analisis artificial intelligence\n"
            "assistant: Topik tersebut memiliki "
            "beberapa tren penelitian."

        )

        prompt = (
            build_research_prompt(
                context
            )
        )

        self.assertIn(

            context.query,

            prompt,

        )

    def test_previous_history_and_current_query_remain_separate(
        self,
    ):

        previous_query = (
            "jelaskan tren artificial intelligence"
        )

        current_query = (
            "apa research gap dari topik tersebut?"
        )

        context = build_context(
            current_query
        )

        context.conversation_history = (

            f"user: {previous_query}\n"
            "assistant: Tren penelitian berkembang "
            "pada beberapa pendekatan."

        )

        prompt = (
            build_research_prompt(
                context
            )
        )

        history_heading = (
            "RIWAYAT PERCAKAPAN"
        )

        current_query_heading = (
            "PERTANYAAN SAAT INI"
        )

        history_heading_index = (
            prompt.index(
                history_heading
            )
        )

        previous_query_index = (
            prompt.index(
                previous_query
            )
        )

        current_query_heading_index = (
            prompt.index(
                current_query_heading
            )
        )

        current_query_index = (
            prompt.index(
                current_query
            )
        )

        self.assertLess(

            history_heading_index,

            previous_query_index,

        )

        self.assertLess(

            previous_query_index,

            current_query_heading_index,

        )

        self.assertLess(

            current_query_heading_index,

            current_query_index,

        )


# =====================================
# RESEARCH ENGINE CONVERSATION TESTS
# =====================================

class ResearchEngineConversationTests(
    unittest.TestCase
):

    def setUp(
        self,
    ):

        self.session_id = (
            "research-engine-conversation-session"
        )

        session_manager.delete(
            self.session_id
        )

        self.session = (
            session_manager.create(
                self.session_id
            )
        )

    def tearDown(
        self,
    ):

        session_manager.delete(
            self.session_id
        )

    @patch(
        "app.services.research.research_engine."
        "ResearchPipelineBuilder.build"
    )
    @patch(
        "app.orchestration.task_router."
        "route_query"
    )
    def test_research_analysis_snapshots_history_before_current_user_message(
        self,
        mock_route_query,
        mock_pipeline_build,
    ):

        # =================================
        # PREVIOUS CONVERSATION
        # =================================

        self.session.conversation.append(

            role="user",

            content=(
                "jelaskan artificial intelligence"
            ),

        )

        self.session.conversation.append(

            role="assistant",

            content=(
                "Artificial intelligence adalah "
                "bidang ilmu komputer."
            ),

        )

        expected_history = (
            self.session.conversation.build_history()
        )

        # =================================
        # ROUTING
        # =================================

        mock_route_query.return_value = {

            "intent":
                "research",

            "provider":
                "test-provider",

            "model":
                "test-model",

        }

        # =================================
        # PIPELINE
        # =================================

        def build_pipeline(
            context,
            stream=False,
        ):

            executor = Mock()

            def run():

                context.analysis = (
                    "Generated follow-up analysis"
                )

                context.response = {

                    "analysis":
                        context.analysis,

                }

                return context

            executor.run.side_effect = run

            return executor

        mock_pipeline_build.side_effect = (
            build_pipeline
        )

        # =================================
        # CURRENT QUERY
        # =================================

        current_query = (
            "apa research gap dari topik tersebut?"
        )

        response = research_analysis(

            query=current_query,

            session_id=self.session_id,

        )

        # =================================
        # CAPTURE PIPELINE CONTEXT
        # =================================

        mock_pipeline_build.assert_called_once()

        context = (
            mock_pipeline_build.call_args.args[0]
        )

        # =================================
        # ASSERT PREVIOUS HISTORY SNAPSHOT
        # =================================

        self.assertEqual(

            context.conversation_history,

            expected_history,

        )

        self.assertIn(

            "user: jelaskan artificial intelligence",

            context.conversation_history,

        )

        self.assertIn(

            (
                "assistant: Artificial intelligence "
                "adalah bidang ilmu komputer."
            ),

            context.conversation_history,

        )

        # =================================
        # CURRENT QUERY MUST STAY SEPARATE
        # =================================

        self.assertEqual(

            context.query,

            current_query,

        )

        self.assertNotIn(

            current_query,

            context.conversation_history,

        )

        # =================================
        # CURRENT USER MESSAGE IS RECORDED
        # =================================

        messages = (
            self.session.conversation.messages
        )

        current_user_messages = [

            message

            for message in messages

            if (
                message.role == "user"
                and message.content == current_query
            )

        ]

        self.assertEqual(

            len(current_user_messages),

            1,

        )

        # =================================
        # ASSISTANT RESPONSE IS PERSISTED
        # =================================

        last_message = (
            self.session.conversation.last_message()
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

            "Generated follow-up analysis",

        )

        # =================================
        # RESPONSE
        # =================================

        self.assertEqual(

            response["analysis"],

            "Generated follow-up analysis",

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
# EXECUTION SNAPSHOT PERSISTENCE TESTS
# =====================================

class ExecutionSnapshotPersistenceTests(
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
                "execution-snapshot-session"
            )
        )

    def test_persist_execution_snapshot_updates_session_execution(
        self,
    ):

        context = build_context(
            "analisis artificial intelligence"
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

        context.analysis = (
            "Generated research analysis"
        )

        serialized_context = (
            persist_execution_snapshot(

                session=self.session,

                context=context,

                response_content=(
                    "Persisted response"
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

            "test-provider",

        )

        self.assertEqual(

            execution.model,

            "test-model",

        )

        self.assertEqual(

            execution.intent,

            "research",

        )

        self.assertEqual(

            execution.response,

            "Persisted response",

        )

        self.assertIs(

            execution.serialized_context,

            serialized_context,

        )

        self.assertEqual(

            serialized_context["query"],

            context.query,

        )

        self.assertEqual(

            serialized_context["analysis"],

            context.analysis,

        )

        self.assertIsNotNone(
            execution.updated_at
        )

    def test_persist_execution_snapshot_uses_analysis_fallback(
        self,
    ):

        context = build_context(
            "analisis machine learning"
        )

        context.analysis = (
            "Fallback analysis"
        )

        serialized_context = (
            persist_execution_snapshot(

                session=self.session,

                context=context,

            )
        )

        self.assertEqual(

            self.session.execution.response,

            "Fallback analysis",

        )

        self.assertIs(

            self.session.execution.serialized_context,

            serialized_context,

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

    def test_specialized_stream_updates_execution_snapshot(
        self,
        mock_research_analysis,
    ):

        session = session_manager.create(
            "specialized-execution-session"
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
                "Specialized execution response",

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

        execution = (
            session.execution
        )

        self.assertEqual(

            execution.last_query,

            context.query,

        )

        self.assertEqual(

            execution.provider,

            "test-provider",

        )

        self.assertEqual(

            execution.model,

            "test-model",

        )

        self.assertEqual(

            execution.intent,

            "literature_review",

        )

        self.assertEqual(

            execution.response,

            "Specialized execution response",

        )

        self.assertEqual(

            execution.serialized_context[
                "query"
            ],

            context.query,

        )

        self.assertIsNotNone(
            execution.updated_at
        )

        session_manager.delete(
            session.session_id
        )

    @patch(
        "app.api.routes.routes_chat_stream."
        "research_analysis"
    )
    def test_normal_stream_updates_execution_snapshot(
        self,
        mock_research_analysis,
    ):

        session = session_manager.create(
            "normal-execution-session"
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

        execution = (
            session.execution
        )

        self.assertEqual(

            execution.last_query,

            context.query,

        )

        self.assertEqual(

            execution.response,

            (
                "Bagian pertama. "
                "Bagian kedua."
            ),

        )

        self.assertEqual(

            execution.serialized_context[
                "analysis"
            ],

            (
                "Bagian pertama. "
                "Bagian kedua."
            ),

        )

        self.assertEqual(

            execution.serialized_context[
                "intent"
            ],

            "research",

        )

        self.assertIsNotNone(
            execution.updated_at
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


    def test_execution_session_update_uses_context_analysis_fallback(
        self,
    ):

        context = build_context(
            "analisis artificial intelligence"
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

        context.analysis = (
            "Generated research analysis"
        )

        serialized_context = {

            "query":
                context.query,

            "analysis":
                context.analysis,

        }

        execution = ExecutionSession()

        execution.update(

            context=context,

            serialized_context=(
                serialized_context
            ),

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

            "test-provider",

        )

        self.assertEqual(

            execution.model,

            "test-model",

        )

        self.assertEqual(

            execution.intent,

            "research",

        )

        self.assertEqual(

            execution.response,

            "Generated research analysis",

        )

        self.assertIs(

            execution.serialized_context,

            serialized_context,

        )

        self.assertIsNotNone(
            execution.updated_at
        )

    def test_execution_session_update_prioritizes_explicit_response(
        self,
    ):

        context = build_context(
            "buat literature review AI"
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

        context.analysis = (
            "Fallback context analysis"
        )

        serialized_context = {

            "query":
                context.query,

            "analysis":
                "Specialized analysis",

        }

        execution = ExecutionSession()

        execution.update(

            context=context,

            serialized_context=(
                serialized_context
            ),

            response_content=(
                "Specialized analysis"
            ),

        )

        self.assertEqual(

            execution.response,

            "Specialized analysis",

        )

        self.assertNotEqual(

            execution.response,

            context.analysis,

        )

        self.assertIs(

            execution.serialized_context,

            serialized_context,

        )

        self.assertIsNotNone(
            execution.updated_at
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