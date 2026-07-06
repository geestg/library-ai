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

from app.services.research.engines.document_engine import (
    build_document_context,
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
    DocumentItem,
    ExecutionSession,
    WorkspaceState,
)

from app.services.research.session.models.conversation_session import (
    ConversationSession,
    MAX_HISTORY,
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
# CONVERSATION RETENTION TESTS
# =====================================

class ConversationRetentionTests(
    unittest.TestCase
):

    def setUp(
        self,
    ):

        self.conversation = (
            ConversationSession()
        )

    def test_conversation_retains_only_max_history_messages(
        self,
    ):

        total_messages = (
            MAX_HISTORY + 3
        )

        for index in range(
            total_messages
        ):

            self.conversation.append(

                role="user",

                content=(
                    f"message-{index}"
                ),

            )

        self.assertEqual(

            self.conversation.total_messages(),

            MAX_HISTORY,

        )

    def test_conversation_discards_oldest_messages_when_limit_is_exceeded(
        self,
    ):

        total_messages = (
            MAX_HISTORY + 3
        )

        for index in range(
            total_messages
        ):

            self.conversation.append(

                role="user",

                content=(
                    f"message-{index}"
                ),

            )

        retained_contents = [

            message.content

            for message in
            self.conversation.messages

        ]

        expected_contents = [

            f"message-{index}"

            for index in range(
                3,
                total_messages,
            )

        ]

        self.assertEqual(

            retained_contents,

            expected_contents,

        )

        self.assertNotIn(

            "message-0",

            retained_contents,

        )

        self.assertNotIn(

            "message-1",

            retained_contents,

        )

        self.assertNotIn(

            "message-2",

            retained_contents,

        )

    def test_conversation_preserves_message_order_after_retention(
        self,
    ):

        total_messages = (
            MAX_HISTORY + 2
        )

        for index in range(
            total_messages
        ):

            role = (

                "user"

                if index % 2 == 0

                else "assistant"

            )

            self.conversation.append(

                role=role,

                content=(
                    f"message-{index}"
                ),

            )

        retained_messages = [

            (
                message.role,
                message.content,
            )

            for message in
            self.conversation.messages

        ]

        expected_messages = [

            (

                (
                    "user"

                    if index % 2 == 0

                    else "assistant"
                ),

                f"message-{index}",

            )

            for index in range(
                2,
                total_messages,
            )

        ]

        self.assertEqual(

            retained_messages,

            expected_messages,

        )

    def test_build_history_uses_only_retained_messages(
        self,
    ):

        total_messages = (
            MAX_HISTORY + 2
        )

        for index in range(
            total_messages
        ):

            role = (

                "user"

                if index % 2 == 0

                else "assistant"

            )

            self.conversation.append(

                role=role,

                content=(
                    f"message-{index}"
                ),

            )

        history = (
            self.conversation.build_history()
        )

        history_lines = (
            history.splitlines()
        )

        expected_history = "\n".join(

            [

                (
                    f"{message.role}: "
                    f"{message.content}"
                )

                for message in
                self.conversation.messages

            ]

        )

        self.assertEqual(

            history,

            expected_history,

        )

        self.assertEqual(

            len(history_lines),

            MAX_HISTORY,

        )

        self.assertNotIn(

            "user: message-0",

            history_lines,

        )

        self.assertNotIn(

            "assistant: message-1",

            history_lines,

        )

        self.assertIn(

            "user: message-2",

            history_lines,

        )

        self.assertIn(

            (
                "assistant: "
                f"message-{total_messages - 1}"
            ),

            history_lines,

        )

# =====================================
# CONVERSATION INTEGRITY TESTS
# =====================================

class ConversationIntegrityTests(
    unittest.TestCase
):

    def setUp(
        self,
    ):

        self.conversation = (
            ConversationSession()
        )

    def test_conversation_preserves_user_assistant_order(
        self,
    ):

        self.conversation.append(

            role="user",

            content="Pertanyaan pertama",

        )

        self.conversation.append(

            role="assistant",

            content="Jawaban pertama",

        )

        self.conversation.append(

            role="user",

            content="Pertanyaan kedua",

        )

        self.conversation.append(

            role="assistant",

            content="Jawaban kedua",

        )

        message_pairs = [

            (
                message.role,
                message.content,
            )

            for message in
            self.conversation.messages

        ]

        self.assertEqual(

            message_pairs,

            [

                (
                    "user",
                    "Pertanyaan pertama",
                ),

                (
                    "assistant",
                    "Jawaban pertama",
                ),

                (
                    "user",
                    "Pertanyaan kedua",
                ),

                (
                    "assistant",
                    "Jawaban kedua",
                ),

            ],

        )

    def test_last_user_message_returns_latest_user_message(
        self,
    ):

        self.conversation.append(

            role="user",

            content="Pertanyaan pertama",

        )

        self.conversation.append(

            role="assistant",

            content="Jawaban pertama",

        )

        self.conversation.append(

            role="user",

            content="Pertanyaan terbaru",

        )

        self.conversation.append(

            role="assistant",

            content="Jawaban terbaru",

        )

        message = (
            self.conversation.last_user_message()
        )

        self.assertIsNotNone(
            message
        )

        self.assertEqual(

            message.role,

            "user",

        )

        self.assertEqual(

            message.content,

            "Pertanyaan terbaru",

        )

    def test_last_assistant_message_returns_latest_assistant_message(
        self,
    ):

        self.conversation.append(

            role="user",

            content="Pertanyaan pertama",

        )

        self.conversation.append(

            role="assistant",

            content="Jawaban pertama",

        )

        self.conversation.append(

            role="user",

            content="Pertanyaan terbaru",

        )

        self.conversation.append(

            role="assistant",

            content="Jawaban terbaru",

        )

        message = (
            self.conversation.last_assistant_message()
        )

        self.assertIsNotNone(
            message
        )

        self.assertEqual(

            message.role,

            "assistant",

        )

        self.assertEqual(

            message.content,

            "Jawaban terbaru",

        )

    def test_conversation_serialization_preserves_message_contract(
        self,
    ):

        self.conversation.append(

            role="user",

            content="Analisis artificial intelligence",

        )

        self.conversation.append(

            role="assistant",

            content="Hasil analisis akademik",

        )

        serialized = (
            self.conversation.to_dict()
        )

        self.assertEqual(

            serialized["messages"],

            [

                {

                    "role":
                        "user",

                    "content":
                        "Analisis artificial intelligence",

                },

                {

                    "role":
                        "assistant",

                    "content":
                        "Hasil analisis akademik",

                },

            ],

        )

        self.assertEqual(

            serialized["total_messages"],

            2,

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
# DOCUMENT CHAT OWNERSHIP TESTS
# =====================================

class DocumentChatOwnershipTests(
    unittest.TestCase
):

    @classmethod
    def setUpClass(
        cls,
    ):

        cls.client = TestClient(
            app
        )

    def setUp(
        self,
    ):

        session_manager.clear()

        self.owner_session = (
            session_manager.create(
                "document-chat-owner"
            )
        )

        self.other_session = (
            session_manager.create(
                "document-chat-other"
            )
        )

        self.owner_document = DocumentItem(

            document_id="owner-document",

            filename="owner.pdf",

            file_type="pdf",

            pages=2,

            chunks=4,

            content=(
                "Owner document content"
            ),

            pages_data=[

                {

                    "page":
                        1,

                    "text":
                        "Owner document content",

                }

            ],

        )

        self.other_document = DocumentItem(

            document_id="other-document",

            filename="other.pdf",

            file_type="pdf",

            pages=3,

            chunks=6,

            content=(
                "Other session document content"
            ),

            pages_data=[

                {

                    "page":
                        1,

                    "text":
                        "Other session document content",

                }

            ],

        )

        self.owner_session.documents.add_document(
            self.owner_document
        )

        self.other_session.documents.add_document(
            self.other_document
        )

    def tearDown(
        self,
    ):

        session_manager.clear()

    @patch(
        "app.api.routes.routes_document."
        "gateway.generate_response"
    )
    @patch(
        "app.api.routes.routes_document."
        "retrieve_relevant_chunks"
    )
    def test_document_chat_reads_document_from_owning_session(
        self,
        mock_retrieve_chunks,
        mock_generate_response,
    ):

        mock_retrieve_chunks.return_value = [

            {

                "page":
                    1,

                "text":
                    "Owner document content",

            }

        ]

        mock_generate_response.return_value = (
            "Owner document answer"
        )

        response = self.client.post(

            "/document/chat",

            json={

                "session_id":
                    self.owner_session.session_id,

                "document_id":
                    self.owner_document.document_id,

                "question":
                    "Apa isi dokumen?",

            },

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()

        self.assertEqual(

            data["answer"],

            "Owner document answer",

        )

        self.assertEqual(

            data["filename"],

            "owner.pdf",

        )

        mock_generate_response.assert_called_once()

    @patch(
        "app.api.routes.routes_document."
        "gateway.generate_response"
    )
    def test_document_chat_rejects_document_from_other_session(
        self,
        mock_generate_response,
    ):

        response = self.client.post(

            "/document/chat",

            json={

                "session_id":
                    self.owner_session.session_id,

                "document_id":
                    self.other_document.document_id,

                "question":
                    "Apa isi dokumen?",

            },

        )

        self.assertEqual(
            response.status_code,
            404,
        )

        mock_generate_response.assert_not_called()

    @patch(
        "app.api.routes.routes_document."
        "gateway.generate_response"
    )
    def test_document_chat_rejects_unknown_session(
        self,
        mock_generate_response,
    ):

        response = self.client.post(

            "/document/chat",

            json={

                "session_id":
                    "missing-session",

                "document_id":
                    self.owner_document.document_id,

                "question":
                    "Apa isi dokumen?",

            },

        )

        self.assertEqual(
            response.status_code,
            404,
        )

        mock_generate_response.assert_not_called()

    def test_document_chat_requires_session_id(
        self,
    ):

        response = self.client.post(

            "/document/chat",

            json={

                "document_id":
                    self.owner_document.document_id,

                "question":
                    "Apa isi dokumen?",

            },

        )

        self.assertEqual(
            response.status_code,
            422,
        )

# =====================================
# DOCUMENT ENGINE OWNERSHIP TESTS
# =====================================

class DocumentEngineOwnershipTests(
    unittest.TestCase
):

    def setUp(
        self,
    ):

        session_manager.clear()

        self.owner_session = (
            session_manager.create(
                "document-engine-owner"
            )
        )

        self.other_session = (
            session_manager.create(
                "document-engine-other"
            )
        )

        self.owner_document = DocumentItem(

            document_id="owner-document",

            filename="owner.pdf",

            file_type="pdf",

            pages=2,

            chunks=4,

            content=(
                "Owner session document content"
            ),

        )

        self.other_document = DocumentItem(

            document_id="other-document",

            filename="other.pdf",

            file_type="pdf",

            pages=3,

            chunks=6,

            content=(
                "Other session document content"
            ),

        )

        self.owner_session.documents.add_document(
            self.owner_document
        )

        self.other_session.documents.add_document(
            self.other_document
        )

    def tearDown(
        self,
    ):

        session_manager.clear()

    def test_build_document_context_includes_owned_document(
        self,
    ):

        result = build_document_context(

            session_id=(
                self.owner_session.session_id
            ),

            active_document_ids=[
                self.owner_document.document_id,
            ],

        )

        self.assertEqual(

            result["documents"],

            [

                {

                    "document_id":
                        "owner-document",

                    "filename":
                        "owner.pdf",

                }

            ],

        )

        self.assertIn(

            "Owner session document content",

            result["context"],

        )

    def test_build_document_context_excludes_document_from_other_session(
        self,
    ):

        result = build_document_context(

            session_id=(
                self.owner_session.session_id
            ),

            active_document_ids=[
                self.other_document.document_id,
            ],

        )

        self.assertEqual(

            result["documents"],

            [],

        )

        self.assertEqual(

            result["context"],

            "",

        )

        self.assertNotIn(

            "Other session document content",

            result["context"],

        )

    def test_build_document_context_includes_only_owned_documents_from_mixed_ids(
        self,
    ):

        result = build_document_context(

            session_id=(
                self.owner_session.session_id
            ),

            active_document_ids=[

                self.owner_document.document_id,

                self.other_document.document_id,

            ],

        )

        document_ids = [

            document["document_id"]

            for document in result["documents"]

        ]

        self.assertEqual(

            document_ids,

            [
                "owner-document",
            ],

        )

        self.assertIn(

            "Owner session document content",

            result["context"],

        )

        self.assertNotIn(

            "Other session document content",

            result["context"],

        )

    def test_build_document_context_returns_empty_for_missing_session(
        self,
    ):

        result = build_document_context(

            session_id="missing-session",

            active_document_ids=[
                self.owner_document.document_id,
            ],

        )

        self.assertEqual(

            result,

            {

                "documents":
                    [],

                "context":
                    "",

            },

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

        context.session_id = (
            "document-stage-session"
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

            session_id=(
                "document-stage-session"
            ),

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
# SESSION ROUTE TESTS
# =====================================

class SessionRouteTests(
    unittest.TestCase
):

    @classmethod
    def setUpClass(
        cls,
    ):

        cls.client = TestClient(
            app
        )

    def setUp(
        self,
    ):

        session_manager.clear()

    def tearDown(
        self,
    ):

        session_manager.clear()

    def test_create_session_returns_complete_workspace_session(
        self,
    ):

        response = self.client.post(
            "/session/create"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()

        self.assertTrue(
            data["session_id"]
        )

        self.assertIn(
            "conversation",
            data,
        )

        self.assertIn(
            "documents",
            data,
        )

        self.assertIn(
            "workspace",
            data,
        )

        self.assertIn(
            "execution",
            data,
        )

        self.assertEqual(

            data["conversation"][
                "total_messages"
            ],

            0,

        )

        self.assertEqual(

            data["documents"][
                "documents"
            ],

            [],

        )

        self.assertTrue(

            session_manager.exists(
                data["session_id"]
            )

        )

    def test_get_session_returns_existing_workspace_session(
        self,
    ):

        session = session_manager.create(
            "route-session"
        )

        session.conversation.append(

            role="user",

            content="jelaskan AI",

        )

        response = self.client.get(
            "/session/route-session"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()

        self.assertEqual(

            data["session_id"],

            "route-session",

        )

        self.assertEqual(

            data["conversation"][
                "total_messages"
            ],

            1,

        )

        self.assertEqual(

            data["conversation"][
                "messages"
            ][0],

            {

                "role":
                    "user",

                "content":
                    "jelaskan AI",

            },

        )

    def test_get_missing_session_returns_404(
        self,
    ):

        response = self.client.get(
            "/session/missing-session"
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_delete_session_removes_existing_session(
        self,
    ):

        session_manager.create(
            "delete-session"
        )

        response = self.client.delete(
            "/session/delete-session"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertFalse(

            session_manager.exists(
                "delete-session"
            )

        )

    def test_delete_missing_session_returns_404(
        self,
    ):

        response = self.client.delete(
            "/session/missing-session"
        )

        self.assertEqual(
            response.status_code,
            404,
        )

# =====================================
# DOCUMENT LIST OWNERSHIP TESTS
# =====================================

class DocumentListOwnershipTests(
    unittest.TestCase
):

    @classmethod
    def setUpClass(
        cls,
    ):

        cls.client = TestClient(
            app
        )

    def setUp(
        self,
    ):

        session_manager.clear()

        self.owner_session = (
            session_manager.create(
                "document-list-owner"
            )
        )

        self.other_session = (
            session_manager.create(
                "document-list-other"
            )
        )

        self.owner_document = DocumentItem(

            document_id="owner-document",

            filename="owner.pdf",

            file_type="pdf",

            pages=2,

            chunks=4,

            content=(
                "Owner private document content"
            ),

            pages_data=[

                {

                    "page":
                        1,

                    "text":
                        "Owner private page content",

                }

            ],

        )

        self.other_document = DocumentItem(

            document_id="other-document",

            filename="other.pdf",

            file_type="pdf",

            pages=3,

            chunks=6,

            content=(
                "Other session private content"
            ),

            pages_data=[

                {

                    "page":
                        1,

                    "text":
                        "Other session private page content",

                }

            ],

        )

        self.owner_session.documents.add_document(
            self.owner_document
        )

        self.other_session.documents.add_document(
            self.other_document
        )

    def tearDown(
        self,
    ):

        session_manager.clear()

    def test_document_list_returns_only_documents_owned_by_session(
        self,
    ):

        response = self.client.get(

            (
                "/session/"
                f"{self.owner_session.session_id}"
                "/documents"
            )

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()

        self.assertEqual(

            data["session_id"],

            self.owner_session.session_id,

        )

        self.assertEqual(

            data["total_documents"],

            1,

        )

        self.assertEqual(

            len(
                data["documents"]
            ),

            1,

        )

        document = (
            data["documents"][0]
        )

        self.assertEqual(

            document["document_id"],

            self.owner_document.document_id,

        )

        self.assertEqual(

            document["filename"],

            self.owner_document.filename,

        )

        self.assertEqual(

            document["file_type"],

            self.owner_document.file_type,

        )

        self.assertEqual(

            document["pages"],

            self.owner_document.pages,

        )

        self.assertEqual(

            document["chunks"],

            self.owner_document.chunks,

        )

        returned_document_ids = [

            item["document_id"]

            for item in data["documents"]

        ]

        self.assertNotIn(

            self.other_document.document_id,

            returned_document_ids,

        )

    def test_document_list_returns_empty_list_for_session_without_documents(
        self,
    ):

        empty_session = (
            session_manager.create(
                "document-list-empty"
            )
        )

        response = self.client.get(

            (
                "/session/"
                f"{empty_session.session_id}"
                "/documents"
            )

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()

        self.assertEqual(

            data["session_id"],

            empty_session.session_id,

        )

        self.assertEqual(

            data["total_documents"],

            0,

        )

        self.assertEqual(

            data["documents"],

            [],

        )

    def test_document_list_rejects_unknown_session(
        self,
    ):

        response = self.client.get(

            "/session/missing-session/documents"

        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_document_list_does_not_expose_document_content(
        self,
    ):

        response = self.client.get(

            (
                "/session/"
                f"{self.owner_session.session_id}"
                "/documents"
            )

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()

        self.assertEqual(

            len(
                data["documents"]
            ),

            1,

        )

        document = (
            data["documents"][0]
        )

        self.assertNotIn(
            "content",
            document,
        )

        self.assertNotIn(
            "pages_data",
            document,
        )

        serialized_response = (
            response.text
        )

        self.assertNotIn(

            "Owner private document content",

            serialized_response,

        )

        self.assertNotIn(

            "Owner private page content",

            serialized_response,

        )

# =====================================
# DOCUMENT OWNERSHIP CONTRACT TESTS
# =====================================

class DocumentOwnershipContractTests(
    unittest.TestCase
):

    @classmethod
    def setUpClass(
        cls,
    ):

        cls.client = TestClient(
            app
        )

    def setUp(
        self,
    ):

        session_manager.clear()

    def tearDown(
        self,
    ):

        session_manager.clear()

    def upload_document(
        self,
        session_id=None,
    ):

        data = {}

        if session_id is not None:

            data["session_id"] = (
                session_id
            )

        with patch(
            "app.api.routes.routes_upload."
            "classify_file",
            return_value="pdf",
        ), patch(
            "app.api.routes.routes_upload."
            "ingest_pdf",
            return_value={

                "full_text":
                    "Synthetic document content",

                "pages":
                    2,

                "chunks":
                    4,

                "pages_data": [

                    {

                        "page":
                            1,

                        "text":
                            "Synthetic page content",

                    }

                ],

            },
        ):

            return self.client.post(

                "/upload-pdf",

                data=data,

                files={

                    "file": (

                        "proposal.pdf",

                        b"%PDF-1.4 synthetic content",

                        "application/pdf",

                    )

                },

            )

    def test_upload_stores_document_in_owning_session(
        self,
    ):

        session = session_manager.create(
            "document-owner-session"
        )

        response = self.upload_document(
            session_id=session.session_id
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()

        document_id = (
            data["document_id"]
        )

        stored_document = (
            session.documents.get_document(
                document_id
            )
        )

        self.assertIsNotNone(
            stored_document
        )

        self.assertEqual(

            stored_document.document_id,

            document_id,

        )

        self.assertEqual(

            stored_document.filename,

            "proposal.pdf",

        )

        self.assertEqual(

            stored_document.file_type,

            "pdf",

        )

        self.assertEqual(

            stored_document.pages,

            2,

        )

        self.assertEqual(

            stored_document.chunks,

            4,

        )

        self.assertEqual(

            stored_document.content,

            "Synthetic document content",

        )

        self.assertEqual(

            stored_document.pages_data,

            [

                {

                    "page":
                        1,

                    "text":
                        "Synthetic page content",

                }

            ],

        )

        self.assertEqual(

            data["session_id"],

            session.session_id,

        )

    def test_upload_without_session_id_returns_422(
        self,
    ):

        response = self.upload_document()

        self.assertEqual(
            response.status_code,
            422,
        )

        self.assertEqual(
            session_manager.count(),
            0,
        )

    def test_upload_with_unknown_session_returns_404(
        self,
    ):

        response = self.upload_document(
            session_id="missing-document-session"
        )

        self.assertEqual(
            response.status_code,
            404,
        )

        self.assertFalse(

            session_manager.exists(
                "missing-document-session"
            )

        )

    def test_document_is_isolated_from_other_sessions(
        self,
    ):

        owner_session = (
            session_manager.create(
                "document-owner-session"
            )
        )

        other_session = (
            session_manager.create(
                "other-document-session"
            )
        )

        response = self.upload_document(
            session_id=(
                owner_session.session_id
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        document_id = (
            response.json()[
                "document_id"
            ]
        )

        owner_document = (
            owner_session.documents.get_document(
                document_id
            )
        )

        other_document = (
            other_session.documents.get_document(
                document_id
            )
        )

        self.assertIsNotNone(
            owner_document
        )

        self.assertIsNone(
            other_document
        )

        self.assertEqual(
            owner_session.documents.count(),
            1,
        )

        self.assertEqual(
            other_session.documents.count(),
            0,
        )

# =====================================
# ENTRYPOINT
# =====================================

if __name__ == "__main__":

    unittest.main(
        verbosity=2
    )