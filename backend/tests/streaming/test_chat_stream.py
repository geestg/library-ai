import json
import unittest

from unittest.mock import (
    MagicMock,
    patch,
)

from fastapi import FastAPI
from fastapi.testclient import (
    TestClient,
)

from app.api.routes.routes_chat_stream import (
    router,
    StreamRequest,
    stream_event,
    persist_stream_assistant,
    persist_stream_execution,
    run_research_pipeline,
)

from app.services.research.session.models import (
    WorkspaceSession,
    ConversationSession,
    DocumentSession,
    WorkspaceState,
    ExecutionSession,
)


# =====================================
# FASTAPI
# =====================================

app = FastAPI()

app.include_router(
    router
)

client = TestClient(
    app
)


# =====================================
# HELPERS
# =====================================

def parse_stream(
    response,
):

    events = []

    for line in response.text.splitlines():

        line = line.strip()

        if not line:

            continue

        events.append(
            json.loads(line)
        )

    return events


def build_context():

    context = MagicMock()

    context.session_id = (
        "session-001"
    )

    context.provider = (
        "openrouter"
    )

    context.model = (
        "gpt-test"
    )

    context.intent = (
        "research"
    )

    context.analysis = ""

    context.response = None

    return context


def build_session():

    return WorkspaceSession(

        session_id="session-001",

        conversation=(
            ConversationSession()
        ),

        documents=(
            DocumentSession()
        ),

        workspace=(
            WorkspaceState()
        ),

        execution=(
            ExecutionSession()
        ),

    )


# =====================================
# STREAM EVENT
# =====================================

class StreamEventTests(
    unittest.TestCase,
):

    def test_stream_event_builds_ndjson(
        self,
    ):

        payload = stream_event(

            "progress",

            {

                "phase":
                    "retrieval",

            },

        )

        self.assertTrue(
            payload.endswith("\n")
        )

        parsed = json.loads(
            payload
        )

        self.assertEqual(

            parsed,

            {

                "type":
                    "progress",

                "data": {

                    "phase":
                        "retrieval",

                },

            },

        )

    def test_stream_event_supports_string(
        self,
    ):

        payload = stream_event(

            "token",

            "Hello",

        )

        parsed = json.loads(
            payload
        )

        self.assertEqual(

            parsed["type"],

            "token",

        )

        self.assertEqual(

            parsed["data"],

            "Hello",

        )


# =====================================
# ASSISTANT PERSISTENCE
# =====================================

class PersistAssistantTests(
    unittest.TestCase,
):

    @patch(
        "app.api.routes.routes_chat_stream.persist_assistant_response"
    )
    @patch(
        "app.api.routes.routes_chat_stream.session_manager"
    )
    def test_persist_stream_assistant(

        self,

        mock_manager,

        mock_persist,

    ):

        session = build_session()

        mock_manager.get.return_value = (
            session
        )

        mock_persist.return_value = (
            "Persisted"
        )

        context = build_context()

        response = {

            "analysis":
                "Hello",

        }

        result = persist_stream_assistant(

            context,

            response,

        )

        self.assertEqual(

            result,

            "Persisted",

        )

        mock_persist.assert_called_once()

    @patch(
        "app.api.routes.routes_chat_stream.session_manager"
    )
    def test_persist_stream_assistant_without_session(

        self,

        mock_manager,

    ):

        mock_manager.get.return_value = (
            None
        )

        result = persist_stream_assistant(

            build_context(),

            {

                "analysis":
                    "Hello",

            },

        )

        self.assertEqual(

            result,

            "",

        )


# =====================================
# EXECUTION PERSISTENCE
# =====================================

class PersistExecutionTests(
    unittest.TestCase,
):

    @patch(
        "app.api.routes.routes_chat_stream.persist_execution_snapshot"
    )
    @patch(
        "app.api.routes.routes_chat_stream.session_manager"
    )
    def test_persist_stream_execution(

        self,

        mock_manager,

        mock_snapshot,

    ):

        session = build_session()

        mock_manager.get.return_value = (
            session
        )

        mock_snapshot.return_value = {

            "query":
                "AI",

        }

        result = persist_stream_execution(

            context=build_context(),

            response_content=(
                "Answer"
            ),

        )

        self.assertEqual(

            result,

            {

                "query":
                    "AI",

            },

        )

        mock_snapshot.assert_called_once()

    @patch(
        "app.api.routes.routes_chat_stream.session_manager"
    )
    def test_persist_stream_execution_without_session(

        self,

        mock_manager,

    ):

        mock_manager.get.return_value = (
            None
        )

        result = persist_stream_execution(

            context=build_context(),

            response_content="",

        )

        self.assertEqual(

            result,

            {},

        )

        # =====================================
# PIPELINE WORKER
# =====================================

class PipelineWorkerTests(
    unittest.TestCase,
):

    @patch(
        "app.api.routes.routes_chat_stream.research_analysis"
    )
    def test_run_research_pipeline_returns_pipeline_result(
        self,
        mock_research,
    ):

        queue = MagicMock()

        context = build_context()

        llm_stream = iter([
            "Hello",
        ])

        mock_research.return_value = (
            context,
            llm_stream,
        )

        request = StreamRequest(

            session_id="session-001",

            message="Artificial Intelligence",

            active_document_ids=[
                "doc-1",
            ],

        )

        run_research_pipeline(

            request,

            queue,

        )

        self.assertGreaterEqual(

            queue.put.call_count,

            1,

        )

        last_event = (

            queue.put.call_args_list[-1]
            .args[0]

        )

        self.assertEqual(

            last_event["type"],

            "pipeline_result",

        )

        self.assertIs(

            last_event["data"]["context"],

            context,

        )

        self.assertIs(

            last_event["data"]["llm_stream"],

            llm_stream,

        )

    @patch(
        "app.api.routes.routes_chat_stream.research_analysis"
    )
    def test_run_research_pipeline_sends_progress(
        self,
        mock_research,
    ):

        queue = MagicMock()

        context = build_context()

        llm_stream = iter([])

        def fake_analysis(
            **kwargs,
        ):

            callback = kwargs[
                "progress_callback"
            ]

            callback({

                "phase":
                    "retrieval",

                "label":
                    "Retrieving",

            })

            return (

                context,

                llm_stream,

            )

        mock_research.side_effect = (
            fake_analysis
        )

        request = StreamRequest(

            session_id="session-001",

            message="AI",

        )

        run_research_pipeline(

            request,

            queue,

        )

        first_event = (

            queue.put.call_args_list[0]
            .args[0]

        )

        self.assertEqual(

            first_event["type"],

            "progress",

        )

        self.assertEqual(

            first_event["data"]["phase"],

            "retrieval",

        )

    @patch(
        "app.api.routes.routes_chat_stream.research_analysis"
    )
    def test_run_research_pipeline_returns_pipeline_error(
        self,
        mock_research,
    ):

        queue = MagicMock()

        mock_research.side_effect = RuntimeError(
            "Pipeline exploded"
        )

        request = StreamRequest(

            session_id="session-001",

            message="AI",

        )

        run_research_pipeline(

            request,

            queue,

        )

        event = (

            queue.put.call_args.args[0]

        )

        self.assertEqual(

            event["type"],

            "pipeline_error",

        )

        self.assertEqual(

            event["data"]["status"],

            "failed",

        )

        self.assertEqual(

            event["data"]["message"],

            "Pipeline exploded",

        )

        self.assertEqual(

            event["data"]["exception_type"],

            "RuntimeError",

        )


# =====================================
# CHAT STREAM
# =====================================

class ChatStreamTests(
    unittest.TestCase,
):

    @patch(
        "app.api.routes.routes_chat_stream.persist_stream_execution"
    )
    @patch(
        "app.api.routes.routes_chat_stream.persist_stream_assistant"
    )
    @patch(
        "app.api.routes.routes_chat_stream.serialize_research_context"
    )
    @patch(
        "app.api.routes.routes_chat_stream.research_analysis"
    )
    def test_stream_returns_complete_llm_stream(
        self,
        mock_research,
        mock_serializer,
        mock_persist_assistant,
        mock_persist_execution,
    ):

        context = build_context()

        mock_serializer.side_effect = (
            lambda ctx: {
                "query":
                    "AI",
            }
        )

        mock_persist_assistant.return_value = (
            "Hello World"
        )

        mock_persist_execution.return_value = (
            {}
        )

        llm_stream = iter([

            "Hel",

            "lo",

            " World",

        ])

        mock_research.return_value = (

            context,

            llm_stream,

        )

        response = client.post(

            "/chat-stream",

            json={

                "session_id":
                    "session-001",

                "message":
                    "AI",

                "active_document_ids":
                    [],

            },

        )

        self.assertEqual(

            response.status_code,

            200,

        )

        events = parse_stream(
            response
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

                "token",

                "token",

                "context_final",

                "end",

            ],

        )

        tokens = [

            event["data"]

            for event in events

            if event["type"] == "token"

        ]

        self.assertEqual(

            "".join(tokens),

            "Hello World",

        )

        self.assertEqual(

            context.analysis,

            "Hello World",

        )

    @patch(
        "app.api.routes.routes_chat_stream.persist_stream_execution"
    )
    @patch(
        "app.api.routes.routes_chat_stream.persist_stream_assistant"
    )
    @patch(
        "app.api.routes.routes_chat_stream.research_analysis"
    )
    def test_specialized_response_skips_llm_stream(

        self,

        mock_research,

        mock_persist_assistant,

        mock_persist_execution,

    ):

        context = build_context()

        context.response = {

            "analysis":
                "Static specialized answer",

        }

        mock_research.return_value = (

            context,

            None,

        )

        mock_persist_assistant.return_value = (

            "Static specialized answer"

        )

        mock_persist_execution.return_value = (
            {}
        )

        response = client.post(

            "/chat-stream",

            json={

                "session_id":
                    "session-001",

                "message":
                    "AI",

                "active_document_ids":
                    [],

            },

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        events = parse_stream(
            response
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

        self.assertEqual(

            events[3]["data"],

            "Static specialized answer",

        )

    @patch(
        "app.api.routes.routes_chat_stream.serialize_research_context"
    )
    @patch(
        "app.api.routes.routes_chat_stream.research_analysis"
    )
    def test_llm_stream_none_returns_error(

        self,

        mock_research,

        mock_serializer,

    ):

        context = build_context()

        mock_serializer.return_value = {}

        mock_research.return_value = (

            context,

            None,

        )

        response = client.post(

            "/chat-stream",

            json={

                "session_id":
                    "session-001",

                "message":
                    "AI",

            },

        )

        events = parse_stream(
            response
        )

        self.assertEqual(

            events[-1]["type"],

            "error",

        )

        self.assertEqual(

            events[-1]["data"]["status"],

            "failed",

        )

    @patch(
        "app.api.routes.routes_chat_stream.research_analysis"
    )
    def test_pipeline_exception_returns_error(

        self,

        mock_research,

    ):

        mock_research.side_effect = RuntimeError(
            "Pipeline failed"
        )

        response = client.post(

            "/chat-stream",

            json={

                "session_id":
                    "session-001",

                "message":
                    "AI",

            },

        )

        events = parse_stream(
            response
        )

        self.assertEqual(

            events[-1]["type"],

            "error",

        )

        self.assertEqual(

            events[-1]["data"]["message"],

            "Pipeline failed",

        )

    @patch(
        "app.api.routes.routes_chat_stream.persist_stream_execution"
    )
    @patch(
        "app.api.routes.routes_chat_stream.persist_stream_assistant"
    )
    @patch(
        "app.api.routes.routes_chat_stream.serialize_research_context"
    )
    @patch(
        "app.api.routes.routes_chat_stream.research_analysis"
    )
    def test_none_and_empty_tokens_are_ignored(

        self,

        mock_research,

        mock_serializer,

        mock_persist_assistant,

        mock_persist_execution,

    ):

        context = build_context()

        mock_serializer.return_value = {}

        mock_persist_assistant.return_value = (
            "ABC"
        )

        mock_persist_execution.return_value = (
            {}
        )

        llm_stream = iter([

            None,

            "",

            "A",

            None,

            "B",

            "",

            "C",

        ])

        mock_research.return_value = (

            context,

            llm_stream,

        )

        response = client.post(

            "/chat-stream",

            json={

                "session_id":
                    "session-001",

                "message":
                    "AI",

            },

        )

        events = parse_stream(
            response
        )

        tokens = [

            event["data"]

            for event in events

            if event["type"] == "token"

        ]

        self.assertEqual(

            tokens,

            [

                "A",

                "B",

                "C",

            ],

        )

        self.assertEqual(

            context.analysis,

            "ABC",

        )

    @patch(
        "app.api.routes.routes_chat_stream.persist_stream_execution"
    )
    @patch(
        "app.api.routes.routes_chat_stream.persist_stream_assistant"
    )
    @patch(
        "app.api.routes.routes_chat_stream.serialize_research_context"
    )
    @patch(
        "app.api.routes.routes_chat_stream.research_analysis"
    )
    def test_metadata_event_contains_provider_model_intent(
        self,
        mock_research,
        mock_serializer,
        mock_persist_assistant,
        mock_persist_execution,
    ):

        context = build_context()

        context.provider = "openrouter"

        context.model = "gpt-5"

        context.intent = "research"

        mock_serializer.return_value = {}

        mock_persist_assistant.return_value = ""

        mock_persist_execution.return_value = {}

        mock_research.return_value = (

            context,

            iter(["hello"]),

        )

        response = client.post(

            "/chat-stream",

            json={

                "session_id":
                    "session-001",

                "message":
                    "AI",

            },

        )

        events = parse_stream(
            response
        )

        metadata = next(

            event

            for event in events

            if event["type"] == "metadata"

        )

        self.assertEqual(

            metadata["data"],

            {

                "provider":
                    "openrouter",

                "model":
                    "gpt-5",

                "intent":
                    "research",

            },

        )

    @patch(
        "app.api.routes.routes_chat_stream.persist_stream_execution"
    )
    @patch(
        "app.api.routes.routes_chat_stream.persist_stream_assistant"
    )
    @patch(
        "app.api.routes.routes_chat_stream.serialize_research_context"
    )
    @patch(
        "app.api.routes.routes_chat_stream.research_analysis"
    )
    def test_context_final_is_before_end(
        self,
        mock_research,
        mock_serializer,
        mock_persist_assistant,
        mock_persist_execution,
    ):

        context = build_context()

        mock_serializer.return_value = {

            "analysis":
                "done",

        }

        mock_persist_assistant.return_value = (
            "done"
        )

        mock_persist_execution.return_value = (
            {}
        )

        mock_research.return_value = (

            context,

            iter([

                "A",

            ]),

        )

        response = client.post(

            "/chat-stream",

            json={

                "session_id":
                    "session-001",

                "message":
                    "AI",

            },

        )

        events = parse_stream(
            response
        )

        event_types = [

            event["type"]

            for event in events

        ]

        self.assertLess(

            event_types.index(
                "context_final"
            ),

            event_types.index(
                "end"
            ),

        )

    @patch(
        "app.api.routes.routes_chat_stream.persist_stream_execution"
    )
    @patch(
        "app.api.routes.routes_chat_stream.persist_stream_assistant"
    )
    @patch(
        "app.api.routes.routes_chat_stream.serialize_research_context"
    )
    @patch(
        "app.api.routes.routes_chat_stream.research_analysis"
    )
    def test_end_event_is_last_event(
        self,
        mock_research,
        mock_serializer,
        mock_persist_assistant,
        mock_persist_execution,
    ):

        context = build_context()

        mock_serializer.return_value = {}

        mock_persist_assistant.return_value = ""

        mock_persist_execution.return_value = {}

        mock_research.return_value = (

            context,

            iter([

                "ABC",

            ]),

        )

        response = client.post(

            "/chat-stream",

            json={

                "session_id":
                    "session-001",

                "message":
                    "AI",

            },

        )

        events = parse_stream(
            response
        )

        self.assertEqual(

            events[-1]["type"],

            "end",

        )

    @patch(
        "app.api.routes.routes_chat_stream.run_research_pipeline"
    )
    def test_pipeline_worker_without_result_returns_error(
        self,
        mock_worker,
    ):

        def fake_worker(
            req,
            queue,
        ):
            return

        mock_worker.side_effect = (
            fake_worker
        )

        response = client.post(

            "/chat-stream",

            json={

                "session_id":
                    "session-001",

                "message":
                    "AI",

            },

        )

        events = parse_stream(
            response
        )

        self.assertEqual(

            events[-1]["type"],

            "error",

        )

        self.assertEqual(

            events[-1]["data"]["exception_type"],

            "PipelineWorkerError",

        )

    @patch(
        "app.api.routes.routes_chat_stream.research_analysis"
    )
    def test_pipeline_returns_none_context(
        self,
        mock_research,
    ):

        mock_research.return_value = (

            None,

            iter([]),

        )

        response = client.post(

            "/chat-stream",

            json={

                "session_id":
                    "session-001",

                "message":
                    "AI",

            },

        )

        events = parse_stream(
            response
        )

        self.assertEqual(

            events[-1]["type"],

            "error",

        )

        self.assertEqual(

            events[-1]["data"]["exception_type"],

            "PipelineContextError",

        )


if __name__ == "__main__":

    unittest.main()